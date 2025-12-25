import pandas as pd
import excel_parser  # Make sure this is in the same folder
from collections import defaultdict

def run_diagnostics():
    print("--- 1. LOADING DATA ---")
    try:
        data = excel_parser.parse_excel_to_config('CSE_Staff_Allocations.xlsx')
        print(f"Loaded {len(data['classes'])} classes and {len(data['staff'])} staff members.")
    except Exception as e:
        print(f"CRITICAL: Could not load data. {e}")
        return

    print("\n--- 2. CLASS LOAD ANALYSIS (Max 42 Hours) ---")
    print(f"{'Class':<15} | {'Lab Hrs':<10} | {'Int. Hrs':<10} | {'Total Hrs':<10} | {'Status'}")
    print("-" * 65)
    
    class_loads = {}
    
    for c_name in data['classes']:
        c_data = data['class_data'][c_name]
        
        lab_hours = len(c_data['labs']) * 3
        # Integrated: 2 subjects * 2 sessions * 2 hours = ?
        # Logic: Each integrated subject appears ONCE in the list, but needs 2 sessions of 2 hours.
        int_hours = len(c_data.get('integrated', [])) * 4 
        
        # Tutorials: 2 hours
        tut_hours = len(c_data['tutorials']) * 2
        
        # Mentor + Library = 2 hours
        spec_hours = len(c_data.get('special', [])) # usually 1h each
        
        # Lectures: Estimate remaining subjects * 4 hours (standard load) or 5
        lectures = [s for s in c_data['subjects'] if s not in c_data['special']]
        lec_hours = len(lectures) * 4
        
        total = lab_hours + int_hours + tut_hours + spec_hours + lec_hours
        class_loads[c_name] = total
        
        status = "OK"
        if total > 42: status = "OVERLOAD!"
        elif total > 38: status = "TIGHT"
        
        print(f"{c_name:<15} | {lab_hours:<10} | {int_hours:<10} | {total:<10} | {status}")

    print("\n--- 3. STAFF LOAD ANALYSIS (Max ~20-25 Hours is healthy) ---")
    staff_hours = defaultdict(int)
    
    for c_name in data['classes']:
        c_data = data['class_data'][c_name]
        
        # Helper to add hours
        def add_hours(subject_list, hours_per_subject):
            for s in subject_list:
                staff_names = c_data['assignments'].get(s, [])
                # If merged class (VI_SEM_B), usually same staff, check dedup
                # simplified: just add load to everyone listed
                for st in staff_names:
                    staff_hours[st] += hours_per_subject

        add_hours(c_data['labs'], 3)
        add_hours(c_data.get('integrated', []), 4) # 2 sess * 2 hrs
        add_hours(c_data['tutorials'], 2)
        add_hours(c_data.get('special', []), 1)
        
        lectures = [s for s in c_data['subjects'] if s not in c_data['special']]
        add_hours(lectures, 4) # Assuming 4 hours/lecture

    # Sort by busiest
    sorted_staff = sorted(staff_hours.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Staff Name':<30} | {'Est. Hours':<10} | {'Status'}")
    print("-" * 55)
    for st, hours in sorted_staff[:10]: # Top 10 busiest
        status = "OK"
        if hours > 30: status = "CRITICAL"
        elif hours > 24: status = "HEAVY"
        print(f"{st:<30} | {hours:<10} | {status}")

if __name__ == "__main__":
    run_diagnostics()