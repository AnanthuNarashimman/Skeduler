import json
import pandas as pd

def json_to_excel(json_file_path, excel_file_path):
    """
    Converts the specific scheduler data.json structure into an Excel file.
    """
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return

    excel_rows = []
    
    staff_expertise = data.get('staff_expertise', {})
    class_data = data.get('class_data', {})

    # Helper function to get subject type
    def get_subject_type(subject_name):
        if "_Lab" in subject_name:
            return "Lab"
        if "_Tutorial" in subject_name:
            return "Tutorial"
        # Check against known special lists (you can expand this logic based on your specific lists)
        special_subjects = ["LIB_HH", "MH", "PW", "T&P", "DS-I", "SSD-III", "BC", "CS"]
        if subject_name in special_subjects:
            return "Special"
        return "Lecture"

    # Iterate through each class in class_data
    for class_name, class_info in class_data.items():
        
        # Combine all subject lists to process for this class
        all_class_subjects = (
            class_info.get('subjects', []) + 
            class_info.get('labs', []) + 
            class_info.get('tutorials', [])
        )
        
        # We use a set to track processed subjects for this class to handle duplicates 
        # if a subject appears in multiple lists (though structure suggests separation)
        processed_subjects = set()

        for subject in all_class_subjects:
            if subject in processed_subjects:
                continue
            
            processed_subjects.add(subject)
            
            # Determine Staff
            # Logic: Find staff from staff_expertise. 
            # Since staff_expertise maps Subject -> [List of Staff], and we don't have specific
            # class-to-staff mapping in the JSON structure provided in the prompt's data.json example 
            # (it just lists expertise), we will take the first staff member listed 
            # or join them if multiple are allowed. 
            # NOTE: In a real scenario, if specific staff are assigned to specific classes 
            # for the same subject, that logic would need to be in the input JSON or derived.
            # For this converter, we'll list all qualified staff comma-separated or just take the first.
            # Let's list all for clarity in the Excel, or you can pick the first one.
            staff_list = staff_expertise.get(subject, ["Unassigned"])
            staff_str = ", ".join(staff_list) 

            # Determine Type
            s_type = get_subject_type(subject)

            # Determine Elective Group
            elective_group = ""
            elective_groups = class_info.get('elective_groups', [])
            for idx, group in enumerate(elective_groups):
                if subject in group:
                    elective_group = f"Group_{idx + 1}"
                    break
            
            # Append row
            excel_rows.append({
                "Class": class_name,
                "Subject": subject,
                "Staff": staff_str,
                "Type": s_type,
                "Elective Group": elective_group
            })

    # Create DataFrame
    df = pd.DataFrame(excel_rows)

    # Save to Excel
    try:
        df.to_excel(excel_file_path, index=False)
        print(f"Successfully converted '{json_file_path}' to '{excel_file_path}'")
    except Exception as e:
        print(f"Error saving Excel file: {e}")

if __name__ == "__main__":
    # Example usage:
    # Ensure you have a 'data.json' file in the same directory or provide correct path
    # You can save the JSON content provided in your prompt to 'server/data.json' first.
    json_path = 'data.json' 
    excel_path = 'department_data.xlsx'
    
    # Create a dummy data.json for demonstration if it doesn't exist (Optional)
    import os
    if not os.path.exists(json_path):
        # Paste the JSON content from your prompt here to create the file on the fly for testing
        print(f"'{json_path}' not found. Please ensure the file exists.")
    else:
        json_to_excel(json_path, excel_path)