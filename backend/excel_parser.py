import pandas as pd
from collections import defaultdict

def parse_excel_to_config(file_path):
    """
    Reads an Excel file and converts it into the JSON structure required by engine.py.
    
    The Excel file is expected to have columns:
    - 'Class': e.g., 'III_SEM_A'
    - 'Subject': e.g., 'DMS' or 'DSA_Lab'
    - 'Staff': e.g., 'Mr. T. Bhaskar'
    - 'Type': 'Lecture', 'Lab', 'Tutorial', or 'Special' (Optional, inferred if missing)
    - 'Elective Group': e.g., 'Group_1' (Optional, for electives happening simultaneously)
    """
    try:
        df = pd.read_excel(file_path)
        
        # Normalize column names to avoid case sensitivity issues
        df.columns = [c.strip() for c in df.columns]
        
        # Initialize empty structure
        data = {
            "classes": [],
            "staff": [],
            "subjects": [],
            "staff_expertise": defaultdict(list),
            "class_data": {}
        }
        
        # Extract unique lists using sets to avoid duplicates, then convert to sorted lists
        # 'dropna()' ensures we don't include empty rows
        data["classes"] = sorted(df['Class'].dropna().unique().tolist())
        data["staff"] = sorted(df['Staff'].dropna().unique().tolist())
        data["subjects"] = sorted(df['Subject'].dropna().unique().tolist())
        
        # Build mappings row by row
        for _, row in df.iterrows():
            c_name = str(row['Class']).strip()
            s_name = str(row['Subject']).strip()
            st_name = str(row['Staff']).strip()
            
            # Handle optional columns with defaults
            sType = row.get('Type', 'Lecture')
            if pd.isna(sType): sType = 'Lecture'
            else: sType = str(sType).strip()
                
            eGroup = row.get('Elective Group', None)
            if pd.isna(eGroup) or str(eGroup).strip() == "": eGroup = None
            else: eGroup = str(eGroup).strip()
            
            # 1. Build Staff Expertise Mapping
            # This maps a subject to ALL staff who can teach it across different classes
            if st_name not in data["staff_expertise"][s_name]:
                data["staff_expertise"][s_name].append(st_name)
                
            # 2. Build Class Data Structure
            if c_name not in data["class_data"]:
                data["class_data"][c_name] = {
                    "subjects": [],
                    "labs": [],
                    "elective_groups": [],
                    "periods_per_subject": {} # Will be populated by dynamic calc in engine
                }
            
            # Add subject to the appropriate list for this class
            # We check if it's already added to avoid duplicates
            class_entry = data["class_data"][c_name]
            
            is_lab = "Lab" in s_name or sType == "Lab"
            target_list = class_entry["labs"] if is_lab else class_entry["subjects"]
            
            if s_name not in target_list:
                target_list.append(s_name)
            
            # Handle Elective Groups
            # We build a temporary dictionary of groups for this class
            # Structure: class_entry['_temp_groups'] = {'Group_1': ['SubA', 'SubB']}
            if eGroup:
                if '_temp_groups' not in class_entry:
                    class_entry['_temp_groups'] = defaultdict(list)
                if s_name not in class_entry['_temp_groups'][eGroup]:
                    class_entry['_temp_groups'][eGroup].append(s_name)

        # Final cleanup pass for Elective Groups
        # Convert the temporary dictionary into the list of lists format required by engine: [['SubA', 'SubB'], ...]
        for c_name, c_data in data["class_data"].items():
            if '_temp_groups' in c_data:
                for group_subjects in c_data['_temp_groups'].values():
                    if len(group_subjects) > 1:
                        c_data['elective_groups'].append(group_subjects)
                del c_data['_temp_groups'] # Clean up temp key
        
        # Convert defaultdict to regular dict for JSON serialization
        data["staff_expertise"] = dict(data["staff_expertise"])
        
        return data

    except Exception as e:
        print(f"Error parsing Excel file: {e}")
        raise e