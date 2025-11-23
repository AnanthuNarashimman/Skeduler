from ortools.sat.python import cp_model
from collections import defaultdict

def solve_staff_assignment(all_classes, all_staff, all_subjects, staff_expertise, class_data):
    """
    Solves the first step: Assigning specific staff to each subject for each class
    to balance the overall workload.
    """
    print("--- Step 1: Solving Staff Assignment and Balancing Workload ---")
    
    model = cp_model.CpModel()
    
    # Create indices for easy lookup
    class_idx = {name: i for i, name in enumerate(all_classes)}
    staff_idx = {name: i for i, name in enumerate(all_staff)}
    subject_idx = {name: i for i, name in enumerate(all_subjects)}

    # --- Variables: Which staff is assigned to a class's subject? ---
    # assigns[(class_idx, subject_idx, staff_idx)] -> Boolean
    assigns = {}
    for c in all_classes:
        # We need to assign staff for both regular subjects and labs
        for s_name in class_data[c]['subjects'] + class_data[c]['labs']:
            if s_name in staff_expertise:
                for st_name in staff_expertise[s_name]:
                    if st_name in staff_idx:
                        c_i, s_i, st_i = class_idx[c], subject_idx[s_name], staff_idx[st_name]
                        assigns[(c_i, s_i, st_i)] = model.NewBoolVar(f'assign_c{c_i}_s{s_i}_st{st_i}')

    # --- Constraint: For each subject in a class, exactly one qualified staff must be assigned. ---
    for c in all_classes:
        for s_name in class_data[c]['subjects'] + class_data[c]['labs']:
            if s_name in staff_expertise:
                c_i, s_i = class_idx[c], subject_idx[s_name]
                # Gather all possible staff assignment variables for this specific subject & class
                qualified_staff_vars = [
                    assigns[(c_i, s_i, staff_idx[st_name])] 
                    for st_name in staff_expertise[s_name] 
                    if st_name in staff_idx
                ]
                if qualified_staff_vars:
                    model.AddExactlyOne(qualified_staff_vars)

    # --- Objective: Balance the workload ---
    # Calculate the total periods assigned to each staff member based on the assignment variables
    workload = {}
    for st_name in all_staff:
        st_i = staff_idx[st_name]
        total_periods = []
        for c in all_classes:
            for s_name in class_data[c]['subjects'] + class_data[c]['labs']:
                if s_name in staff_expertise and st_name in staff_expertise[s_name]:
                    c_i, s_i = class_idx[c], subject_idx[s_name]
                    # Get the number of periods this subject takes up for this class
                    periods = class_data[c]['periods_per_subject'].get(s_name, 0)
                    if (c_i, s_i, st_i) in assigns:
                        # Add (variable * periods) to the staff's workload sum
                        total_periods.append(assigns[(c_i, s_i, st_i)] * periods)
        workload[st_i] = sum(total_periods)
    
    # Minimize the maximum workload of any single staff member
    max_workload = model.NewIntVar(0, 42, 'max_workload')
    for st_i in workload:
        model.Add(workload[st_i] <= max_workload)
    model.Minimize(max_workload)
    
    # Solve the assignment model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("✅ Staff assignment found!\n")
        fixed_assignments = {}
        # Extract the chosen assignments to pass to Step 2
        for c in all_classes:
            class_assignments = {}
            for s_name in class_data[c]['subjects'] + class_data[c]['labs']:
                if s_name in staff_expertise:
                    c_i, s_i = class_idx[c], subject_idx[s_name]
                    for st_name in staff_expertise[s_name]:
                        if st_name in staff_idx:
                            st_i = staff_idx[st_name]
                            if (c_i, s_i, st_i) in assigns and solver.Value(assigns[(c_i, s_i, st_i)]):
                                class_assignments[s_name] = st_name
            fixed_assignments[c] = class_assignments
        return fixed_assignments
    return None

def solve_scheduling(all_classes, all_staff, all_subjects, fixed_assignments, class_data):
    """
    Solves the second step: Placing the periods into the grid (Time Scheduling)
    using the fixed staff assignments from Step 1.
    """
    print("--- Step 2: Solving Timetable Scheduling with Fixed Assignments ---")

    num_days = 6
    num_periods = 7
    
    class_idx = {name: i for i, name in enumerate(all_classes)}
    staff_idx = {name: i for i, name in enumerate(all_staff)}
    subject_idx = {name: i for i, name in enumerate(all_subjects)}
    
    model = cp_model.CpModel()

    # --- Variables: assign[(class, day, period, subject)] ---
    # assign_c0_d0_p0_s0 = True means Class 0 has Subject 0 on Day 0, Period 0
    assign = {}
    for c_i in range(len(all_classes)):
        for d in range(num_days):
            for p in range(num_periods):
                for s_i in range(len(all_subjects)):
                    assign[(c_i, d, p, s_i)] = model.NewBoolVar(f'assign_c{c_i}_d{d}_p{p}_s{s_i}')
    
    # --- Helper Variables: Lab Starts ---
    # Only created for valid lab start times to enforce consecutive periods
    lab_starts = {}
    valid_lab_starts = [1, 4] # Lab can start at period 2 (index 1) or period 5 (index 4)
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['labs']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days - 1): # No labs on Saturday (index 5)
                    for p in valid_lab_starts:
                        lab_starts[(c_i, d, p, s_i)] = model.NewBoolVar(f'lab_start_c{c_i}_d{d}_p{p}_s{s_i}')
    
    # --- Constraints ---
    
    # Rule 1 & 1.5: A class has one activity at a time, respecting electives
    for c in all_classes:
        c_i = class_idx[c]
        for d in range(num_days):
            for p in range(num_periods):
                all_activities_in_slot = []
                
                # 1. Add non-elective subjects
                non_elective_subjects = [
                    s for s in class_data[c]['subjects'] + class_data[c]['labs'] 
                    if not any(s in g for g in class_data[c]['elective_groups'])
                ]
                for s_name in non_elective_subjects:
                    if s_name in subject_idx:
                        all_activities_in_slot.append(assign[(c_i, d, p, subject_idx[s_name])])
                
                # 2. Add elective groups (only count one variable per group to represent the slot)
                for group in class_data[c]['elective_groups']:
                    if group and group[0] in subject_idx:
                        all_activities_in_slot.append(assign[(c_i, d, p, subject_idx[group[0]])])
                
                # Constraint: At most one activity per slot per class
                model.Add(sum(all_activities_in_slot) <= 1)

        # Elective Linkage: If one elective in a group is scheduled, ALL must be scheduled
        for group in class_data[c]['elective_groups']:
            if group and group[0] in subject_idx:
                first_subject_idx = subject_idx[group[0]]
                for other_subject in group[1:]:
                    if other_subject in subject_idx:
                        other_subject_idx = subject_idx[other_subject]
                        for d in range(num_days):
                            for p in range(num_periods):
                                model.Add(assign[(c_i, d, p, first_subject_idx)] == assign[(c_i, d, p, other_subject_idx)])

    # Rule 2: Enforce total weekly periods for each subject
    for c in all_classes:
        c_i = class_idx[c]
        for s_name, count in class_data[c]['periods_per_subject'].items():
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(assign[(c_i, d, p, s_i)] for d in range(num_days) for p in range(num_periods)) == count)
    
    # Rule 3: Lab constraints (Consecutive + Total Count)
    # Link start variable to 3 consecutive periods
    for c_i, d, p, s_i in lab_starts:
        for i in range(3):
            model.Add(assign[(c_i, d, p + i, s_i)] == 1).OnlyEnforceIf(lab_starts[(c_i, d, p, s_i)])
    
    # Ensure each lab happens exactly once per week
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['labs']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(lab_starts.get((c_i, d, p, s_i), 0) for d in range(num_days - 1) for p in valid_lab_starts) == 1)

    # Rule 4: Staff conflict constraint
    # This uses the FIXED assignments from Step 1 to check conflicts
    for st_name in all_staff:
        for d in range(num_days):
            for p in range(num_periods):
                active_assignments = []
                for c in all_classes:
                    c_i = class_idx[c]
                    if c in fixed_assignments:
                        # Check which subject this staff is assigned to for this class
                        for s_name, staff in fixed_assignments[c].items():
                            if staff == st_name and s_name in subject_idx:
                                s_i = subject_idx[s_name]
                                active_assignments.append(assign[(c_i, d, p, s_i)])
                if active_assignments:
                    # Staff can be in at most one place at a time
                    model.Add(sum(active_assignments) <= 1)

    # Rule 4.5: At most one lab session per CLASS per day
    for c in all_classes:
        c_i = class_idx[c]
        for d in range(num_days - 1):
            daily_labs_for_class = []
            for s_name in class_data[c]['labs']:
                if s_name in subject_idx:
                    s_i = subject_idx[s_name]
                    for p in valid_lab_starts:
                        daily_labs_for_class.append(lab_starts.get((c_i, d, p, s_i), 0))
            model.Add(sum(daily_labs_for_class) <= 1)

    # Optimization: Reduce Subject Repetition
    # Minimize having the same subject more than once a day (unless necessary)
    core_subjects = [
        s for s in all_subjects 
        if '_Lab' not in s 
        and s not in ['PW', 'T&P', 'DS-I', 'SSD-III', 'BC', 'CS', 'LIB_HH', 'MH'] 
        and not any(s in g for c_data in class_data.values() for g in c_data['elective_groups'])
    ]
    repetition_penalties = []
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in core_subjects:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days):
                    # Hard constraint: Max 2 periods per day for core subjects
                    model.Add(sum(assign[(c_i, d, p, s_i)] for p in range(num_periods)) <= 2)
                    
                    # Soft constraint: Penalty if > 1
                    is_repeated = model.NewBoolVar(f'is_repeated_c{c_i}_d{d}_s{s_i}')
                    daily_sum = sum(assign[(c_i, d, p, s_i)] for p in range(num_periods))
                    model.Add(daily_sum > 1).OnlyEnforceIf(is_repeated)
                    model.Add(daily_sum <= 1).OnlyEnforceIf(is_repeated.Not())
                    repetition_penalties.append(is_repeated)
    
    model.Minimize(sum(repetition_penalties))

    # Solve the scheduling model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0 # Timeout to prevent hanging
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        final_schedule = {}
        # Construct the final JSON-friendly schedule dictionary
        for c in all_classes:
            c_i = class_idx[c]
            class_schedule = {}
            for d in range(num_days):
                day_schedule = []
                for p in range(num_periods):
                    slot_info = "--- FREE ---"
                    for s_name, staff in fixed_assignments[c].items():
                        if s_name in subject_idx:
                            s_i = subject_idx[s_name]
                            if solver.Value(assign[(c_i, d, p, s_i)]):
                                slot_info = f"{s_name} ({staff})"
                                break
                    day_schedule.append(slot_info)
                class_schedule[d] = day_schedule
            final_schedule[c] = class_schedule
        return final_schedule
    return None

def generate_timetable(data):
    """
    The main entry point called by the Flask app.
    Orchestrates the two-step solving process.
    """
    all_classes = data['classes']
    all_staff = data['staff']
    all_subjects = data['subjects']
    staff_expertise = data['staff_expertise']
    class_data = data['class_data']

    # --- Dynamic Period Calculation Logic ---
    # This ensures the total periods per week sum exactly to 42 for every class
    for c in all_classes:
        ideal_hours = {'lecture': 6, 'lab': 3, 'other': 1, 'pw': 4, 'tp': 4, 'ds': 3, 'ssd': 3, 'bc': 3, 'cs': 2, 'elective': 6} 
        periods = defaultdict(int)
        
        # 1. Assign Fixed Periods
        for s_name in class_data[c]['subjects'] + class_data[c]['labs']:
            if s_name in staff_expertise:
                if '_Lab' in s_name: periods[s_name] = ideal_hours['lab']
                elif s_name in ['PW', 'T&P']: periods[s_name] = ideal_hours['pw']
                elif s_name in ['DS-I', 'SSD-III']: periods[s_name] = ideal_hours['ssd']
                elif s_name in ['BC', 'CS']: periods[s_name] = ideal_hours['cs']
                elif s_name in ['LIB_HH', 'MH']: periods[s_name] = ideal_hours['other']
        
        for group in class_data[c]['elective_groups']:
            for s_name in group:
                if s_name in staff_expertise:
                    periods[s_name] = ideal_hours['elective']
        
        # 2. Distribute Remaining Periods
        core_lectures = [s for s in class_data[c]['subjects'] if s not in periods and '_Lab' not in s and s in staff_expertise]
        
        # Calculate used slots (counting electives as 1 slot per group)
        current_total = sum(v for k,v in periods.items() if not any(k in g[1:] for g in class_data[c]['elective_groups']))
        remaining_slots = 42 - current_total
        
        if core_lectures:
            base_periods = remaining_slots // len(core_lectures)
            remainder = remaining_slots % len(core_lectures)
            for s_name in core_lectures: periods[s_name] = base_periods
            for i in range(remainder): periods[core_lectures[i]] += 1
        
        class_data[c]['periods_per_subject'] = periods

    # --- Execute Two-Step Process ---
    
    # Step 1: Assign Staff
    fixed_assignments = solve_staff_assignment(all_classes, all_staff, all_subjects, staff_expertise, class_data)
    if not fixed_assignments:
        return {"status": "error", "message": "Staff Assignment Failed (Workload Imbalance)"}

    # Step 2: Create Schedule
    final_schedule = solve_scheduling(all_classes, all_staff, all_subjects, fixed_assignments, class_data)
    if final_schedule:
        return {"status": "success", "schedule": final_schedule}
    else:
        return {"status": "error", "message": "Scheduling Failed (Over-constrained)"}