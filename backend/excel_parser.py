import pandas as pd
from collections import defaultdict

def parse_excel_to_config(file_path):
    """
    Reads an Excel file and converts it into the JSON structure required by engine.py.
    
    The Excel file is expected to have columns:
    - 'Class': e.g., 'III_SEM_A'
    - 'Subject': e.g., 'DMS' or 'DSA_Lab'
    - 'Staff': e.g., 'Mr. T. Bhaskar'
    - 'Type': 'Lecture', 'Lab', 'Tutorial', or 'Special' (Optional)
    - 'Elective Group': e.g., 'Group_1' (Optional)
    """
    try:
        df = pd.read_excel(file_path)
        
        # Normalize column names
        df.columns = [c.strip() for c in df.columns]
        
        # Initialize structure
        data = {
            "classes": [],
            "staff": [],
            "subjects": [],
            "staff_expertise": defaultdict(list),
            "class_data": {}
        }
        
        # Extract unique lists
        data["classes"] = sorted(df['Class'].dropna().unique().tolist())
        data["staff"] = sorted(df['Staff'].dropna().unique().tolist())
        data["subjects"] = sorted(df['Subject'].dropna().unique().tolist())
        
        for _, row in df.iterrows():
            c_name = str(row['Class']).strip()
            s_name = str(row['Subject']).strip()
            st_name = str(row['Staff']).strip()
            
            # Determine Type
            sType = row.get('Type', 'Lecture')
            if pd.isna(sType): sType = 'Lecture'
            else: sType = str(sType).strip()
            
            # Determine Elective Group
            eGroup = row.get('Elective Group', None)
            if pd.isna(eGroup) or str(eGroup).strip() == "": eGroup = None
            else: eGroup = str(eGroup).strip()
            
            # 1. Build Staff Expertise
            if st_name not in data["staff_expertise"][s_name]:
                data["staff_expertise"][s_name].append(st_name)
                
            # 2. Build Class Data Structure
            if c_name not in data["class_data"]:
                data["class_data"][c_name] = {
                    "subjects": [],
                    "labs": [],
                    "tutorials": [],
                    "elective_groups": [],
                    "periods_per_subject": {} # Calculated by engine
                }
            
            class_entry = data["class_data"][c_name]
            
            # Categorize Subject based on Type column OR Name convention
            is_lab = "Lab" in s_name or sType == "Lab"
            is_tutorial = "Tutorial" in s_name or sType == "Tutorial"
            
            if is_lab:
                if s_name not in class_entry["labs"]:
                    class_entry["labs"].append(s_name)
            elif is_tutorial:
                if s_name not in class_entry["tutorials"]:
                    class_entry["tutorials"].append(s_name)
            else:
                if s_name not in class_entry["subjects"]:
                    class_entry["subjects"].append(s_name)
            
            # Handle Elective Groups
            if eGroup:
                if '_temp_groups' not in class_entry:
                    class_entry['_temp_groups'] = defaultdict(list)
                if s_name not in class_entry['_temp_groups'][eGroup]:
                    class_entry['_temp_groups'][eGroup].append(s_name)

        # Cleanup Elective Groups
        for c_name, c_data in data["class_data"].items():
            if '_temp_groups' in c_data:
                for group_subjects in c_data['_temp_groups'].values():
                    if len(group_subjects) > 1:
                        c_data['elective_groups'].append(group_subjects)
                del c_data['_temp_groups']
        
        data["staff_expertise"] = dict(data["staff_expertise"])
        
        return data

    except Exception as e:
        print(f"Error parsing Excel file: {e}")
        raise e