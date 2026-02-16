import pandas as pd
import re
from collections import defaultdict

def normalize_staff_name(name):
    """
    Normalize staff name for matching purposes.
    Removes ALL spaces and converts to lowercase.
    This way 'Mr. Rajiv Kannan', 'Mr.Rajivkannan', and 'mr. rajiv kannan' are all treated as same person.
    Only the spelling (letters and their order) matters for identification.
    """
    if not name or not isinstance(name, str):
        return ""
    # Convert to lowercase and remove ALL spaces
    import re
    # First add space after periods (Dr.A. -> Dr. A.)
    name = re.sub(r'\.(?=[A-Za-z])', '. ', name)
    # Then remove all spaces and lowercase
    normalized = name.lower().replace(' ', '')
    return normalized

def parse_excel_to_config(file_path):
    """
    Reads the 'CSE Staff Allocations' Excel/CSV.
    Handles complex staff strings, combined classes, and specific types.
    """
    try:
        # distinct logic for csv vs xlsx
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        # Normalize headers
        df.columns = [c.strip() for c in df.columns]
        
        data = {
            "classes": [],
            "staff": [],
            "subjects": [],
            "class_data": {},
            "staff_name_mapping": {}  # normalized -> original display name
        }
        
        classes_set = set()
        staff_dict = {}  # normalized -> original display name
        subjects_set = set()

        for _, row in df.iterrows():
            raw_class = str(row['Class']).strip()
            s_name = str(row['Subject']).strip()
            raw_staff = str(row['Staff']).strip() if pd.notna(row['Staff']) else "TBA"
            sType = str(row.get('Type', 'Lecture')).strip()
            eGroup = str(row.get('Elective Group', '')).strip()
            if eGroup == 'nan': eGroup = ""

            # 1. Handle Class Names (Split "VI_SEM_A & B" before normalization)
            class_names = []
            if '&' in raw_class:
                # Example: "VI_SEM_A & B" -> ["VI_SEM_A", "VI_SEM_B"]
                parts = raw_class.split('&')
                base_part = parts[0].strip()  # "VI_SEM_A" or "VI SEM A"
                suffix = parts[1].strip()     # "B"

                # Normalize the base part
                base_part = re.sub(r'\s+', '_', base_part)
                base_part = re.sub(r'_+', '_', base_part)

                class_names.append(base_part)

                # Construct the second class name by replacing the last character
                if base_part.endswith('_A'):
                    # "VI_SEM_A" -> "VI_SEM_B"
                    class_names.append(base_part[:-1] + suffix)
                elif base_part.endswith('A'):
                    # Less common case
                    class_names.append(base_part[:-1] + suffix)
                else:
                    # Fallback: just append the suffix
                    class_names.append(base_part + '_' + suffix)
            else:
                # Normalize class name - remove extra spaces and standardize format
                normalized = re.sub(r'\s+', '_', raw_class)
                normalized = re.sub(r'_+', '_', normalized)
                class_names.append(normalized)

            # 2. Handle Staff Names (Robust Split)
            # Split by comma, slash, newline, or when a new title appears (Mr., Dr., Mrs., Ms.)
            clean_staff = raw_staff.replace('\n', ',').replace('/', ',')
            for title in [' Mr.', ' Dr.', ' Mrs.', ' Ms.']:
                clean_staff = clean_staff.replace(title, ',' + title.strip())

            # Now split by comma and clean up
            staff_list = [s.strip() for s in clean_staff.split(',') if s.strip() and s.strip().lower() != 'nan']
            
            # 3. Process for EACH class found
            for c_name in class_names:
                classes_set.add(c_name)
                subjects_set.add(s_name)
                for s in staff_list:
                    normalized = normalize_staff_name(s)
                    # Keep the first occurrence's display name
                    if normalized not in staff_dict:
                        staff_dict[normalized] = s

                if c_name not in data["class_data"]:
                    data["class_data"][c_name] = {
                        "subjects": [], "labs": [], "tutorials": [],
                        "integrated": [], "special": [],
                        "elective_groups": [],
                        "assignments": {},
                        "periods_per_subject": {}
                    }
                
                c_data = data["class_data"][c_name]

                # Categorize Subject
                is_special = sType == "Special"
                is_integrated = ("Integrated" in sType or "Integrated" in s_name) and not is_special
                is_lab = ("Lab" in s_name or "LAB" in s_name or sType == "Lab") and not is_integrated and not is_special
                is_tutorial = "Tutorial" in sType and not is_special

                if is_special:
                    if s_name not in c_data["special"]: c_data["special"].append(s_name)
                elif is_integrated:
                    if s_name not in c_data["integrated"]: c_data["integrated"].append(s_name)
                elif is_lab:
                    if s_name not in c_data["labs"]: c_data["labs"].append(s_name)
                elif is_tutorial:
                    if s_name not in c_data["tutorials"]: c_data["tutorials"].append(s_name)
                else:
                    if s_name not in c_data["subjects"]: c_data["subjects"].append(s_name)

                c_data["assignments"][s_name] = staff_list

                if eGroup:
                    if '_temp_groups' not in c_data:
                        c_data['_temp_groups'] = defaultdict(list)
                    if s_name not in c_data['_temp_groups'][eGroup]:
                        c_data['_temp_groups'][eGroup].append(s_name)

        # Finalize Groups
        for c_name, c_data in data["class_data"].items():
            if '_temp_groups' in c_data:
                for group in c_data['_temp_groups'].values():
                    if len(group) > 1:
                        c_data['elective_groups'].append(group)
                del c_data['_temp_groups']

        data["classes"] = sorted(list(classes_set))
        # Use original display names for staff list
        data["staff"] = sorted(list(staff_dict.values()))
        data["staff_name_mapping"] = staff_dict  # Store mapping for lookups
        data["subjects"] = sorted(list(subjects_set))
        
        return data

    except Exception as e:
        print(f"Error parsing file: {e}")
        raise e