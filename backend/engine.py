from ortools.sat.python import cp_model
from collections import defaultdict

def solve_staff_assignment(all_classes, all_staff, all_subjects, staff_expertise, class_data):
    """
    Step 1: Assigns staff to subjects to balance workload.
    Ensures EXACTLY ONE staff member is assigned to each subject for a given class.
    """
    print("--- Step 1: Solving Staff Assignment ---")
    model = cp_model.CpModel()
    
    class_idx = {name: i for i, name in enumerate(all_classes)}
    staff_idx = {name: i for i, name in enumerate(all_staff)}
    subject_idx = {name: i for i, name in enumerate(all_subjects)}

    assigns = {}
    
    # Create assignment variables
    for c in all_classes:
        full_subject_list = (class_data[c]['subjects'] + 
                             class_data[c]['labs'] + 
                             class_data[c]['tutorials'])
        
        unique_subjects = set(full_subject_list)
        
        for s_name in unique_subjects:
            if s_name in staff_expertise:
                for st_name in staff_expertise[s_name]:
                    if st_name in staff_idx:
                        c_i, s_i, st_i = class_idx[c], subject_idx[s_name], staff_idx[st_name]
                        assigns[(c_i, s_i, st_i)] = model.NewBoolVar(f'assign_c{c_i}_s{s_i}_st{st_i}')

    # Constraint: Each subject in each class must have EXACTLY ONE qualified staff member assigned
    for c in all_classes:
        full_subject_list = (class_data[c]['subjects'] + 
                             class_data[c]['labs'] + 
                             class_data[c]['tutorials'])
        unique_subjects = set(full_subject_list)
        
        for s_name in unique_subjects:
            if s_name in staff_expertise:
                c_i, s_i = class_idx[c], subject_idx[s_name]
                qualified_staff_vars = [
                    assigns[(c_i, s_i, staff_idx[st_name])] 
                    for st_name in staff_expertise[s_name] 
                    if st_name in staff_idx
                ]
                
                if qualified_staff_vars:
                    # Determine required staff count
                    is_lab = s_name in class_data[c]['labs']
                    is_tutorial = s_name in class_data[c]['tutorials']
                    
                    target_count = 1
                    if is_lab or is_tutorial:
                        # Try to assign 2 staff for labs/tutorials
                        target_count = 2 if len(qualified_staff_vars) >= 2 else 1
                    
                    model.Add(sum(qualified_staff_vars) == target_count)

    # Objective: Balance workload
    workload = {}
    for st_name in all_staff:
        st_i = staff_idx[st_name]
        total_periods = []
        for c in all_classes:
            full_subject_list = (class_data[c]['subjects'] + 
                                 class_data[c]['labs'] + 
                                 class_data[c]['tutorials'])
            for s_name in set(full_subject_list):
                if s_name in staff_expertise and st_name in staff_expertise[s_name]:
                    c_i, s_i = class_idx[c], subject_idx[s_name]
                    periods = class_data[c]['periods_per_subject'].get(s_name, 0)
                    if (c_i, s_i, st_i) in assigns:
                        total_periods.append(assigns[(c_i, s_i, st_i)] * periods)
        workload[st_i] = sum(total_periods)
    
    max_workload = model.NewIntVar(0, 42, 'max_workload')
    for st_i in workload:
        model.Add(workload[st_i] <= max_workload)
    model.Minimize(max_workload)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        fixed_assignments = {}
        for c in all_classes:
            class_assignments = {}
            full_subject_list = (class_data[c]['subjects'] + 
                                 class_data[c]['labs'] + 
                                 class_data[c]['tutorials'])
            for s_name in set(full_subject_list):
                if s_name in staff_expertise:
                    c_i, s_i = class_idx[c], subject_idx[s_name]
                    assigned_staff_list = []
                    for st_name in staff_expertise[s_name]:
                        if st_name in staff_idx:
                            st_i = staff_idx[st_name]
                            if (c_i, s_i, st_i) in assigns and solver.Value(assigns[(c_i, s_i, st_i)]):
                                assigned_staff_list.append(st_name)
                    class_assignments[s_name] = assigned_staff_list
            
            fixed_assignments[c] = class_assignments
        return fixed_assignments
    return None

def solve_scheduling(all_classes, all_staff, all_subjects, fixed_assignments, class_data):
    print("--- Step 2: Solving Timetable Scheduling ---")
    num_days = 6
    num_periods = 7
    
    class_idx = {name: i for i, name in enumerate(all_classes)}
    staff_idx = {name: i for i, name in enumerate(all_staff)}
    subject_idx = {name: i for i, name in enumerate(all_subjects)}
    
    model = cp_model.CpModel()

    assign = {}
    for c_i in range(len(all_classes)):
        for d in range(num_days):
            for p in range(num_periods):
                for s_i in range(len(all_subjects)):
                    assign[(c_i, d, p, s_i)] = model.NewBoolVar(f'assign_c{c_i}_d{d}_p{p}_s{s_i}')
    
    # --- Lab Helpers ---
    lab_starts = {}
    valid_lab_starts = [1, 4] 
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['labs']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days - 1): 
                    for p in valid_lab_starts:
                        lab_starts[(c_i, d, p, s_i)] = model.NewBoolVar(f'lab_start_c{c_i}_d{d}_p{p}_s{s_i}')

    # --- Tutorial Helpers ---
    tutorial_starts = {}
    valid_tutorial_starts = [0, 1, 2, 4, 5] 
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['tutorials']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days - 1):
                    for p in valid_tutorial_starts:
                        tutorial_starts[(c_i, d, p, s_i)] = model.NewBoolVar(f'tut_start_c{c_i}_d{d}_p{p}_s{s_i}')

    # --- Constraints ---
    
    # Rule 1: Single Activity per Slot
    for c in all_classes:
        c_i = class_idx[c]
        for d in range(num_days):
            for p in range(num_periods):
                all_activities = []
                
                full_list = (class_data[c]['subjects'] + 
                             class_data[c]['labs'] + 
                             class_data[c]['tutorials'])
                
                non_electives = [s for s in full_list if not any(s in g for g in class_data[c]['elective_groups'])]
                
                for s_name in non_electives:
                    if s_name in subject_idx:
                        all_activities.append(assign[(c_i, d, p, subject_idx[s_name])])
                
                for group in class_data[c]['elective_groups']:
                    if group and group[0] in subject_idx:
                        all_activities.append(assign[(c_i, d, p, subject_idx[group[0]])])
                
                model.Add(sum(all_activities) <= 1)

        # Link electives
        for group in class_data[c]['elective_groups']:
            if group and group[0] in subject_idx:
                first_idx = subject_idx[group[0]]
                for other in group[1:]:
                    if other in subject_idx:
                        other_idx = subject_idx[other]
                        for d in range(num_days):
                            for p in range(num_periods):
                                model.Add(assign[(c_i, d, p, first_idx)] == assign[(c_i, d, p, other_idx)])

    # Rule 2: Period Counts
    for c in all_classes:
        c_i = class_idx[c]
        for s_name, count in class_data[c]['periods_per_subject'].items():
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(assign[(c_i, d, p, s_i)] for d in range(num_days) for p in range(num_periods)) == count)
    
    # Rule 3: Lab Logic
    for c_i, d, p, s_i in lab_starts:
        for i in range(3):
            model.Add(assign[(c_i, d, p + i, s_i)] == 1).OnlyEnforceIf(lab_starts[(c_i, d, p, s_i)])
    
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['labs']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(lab_starts.get((c_i, d, p, s_i), 0) for d in range(num_days - 1) for p in valid_lab_starts) == 1)

    # Rule 3.5: Tutorial Logic
    for c_i, d, p, s_i in tutorial_starts:
        for i in range(2):
            model.Add(assign[(c_i, d, p + i, s_i)] == 1).OnlyEnforceIf(tutorial_starts[(c_i, d, p, s_i)])

    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['tutorials']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(tutorial_starts.get((c_i, d, p, s_i), 0) for d in range(num_days - 1) for p in valid_tutorial_starts) == 1)

    # Rule 4: Staff Conflicts
    for st_name in all_staff:
        for d in range(num_days):
            for p in range(num_periods):
                active = []
                for c in all_classes:
                    c_i = class_idx[c]
                    if c in fixed_assignments:
                        for s_name, staff_list in fixed_assignments[c].items():
                            if st_name in staff_list and s_name in subject_idx:
                                s_i = subject_idx[s_name]
                                active.append(assign[(c_i, d, p, s_i)])
                if active:
                    model.Add(sum(active) <= 1)

    # Rule 5: Lab Limits (1 per class per day)
    for c in all_classes:
        c_i = class_idx[c]
        for d in range(num_days - 1):
            daily_labs = []
            for s_name in class_data[c]['labs']:
                if s_name in subject_idx:
                    s_i = subject_idx[s_name]
                    for p in valid_lab_starts:
                        daily_labs.append(lab_starts.get((c_i, d, p, s_i), 0))
            model.Add(sum(daily_labs) <= 1)

    # Rule 6: First Period Diversity (New)
    for c_i in range(len(all_classes)):
        for s_i in range(len(all_subjects)):
            # Sum of times this specific subject appears in Period 0 across all days
            first_period_appearances = sum(assign[(c_i, d, 0, s_i)] for d in range(num_days))
            # It can appear at most once in the first period slot for the entire week
            model.Add(first_period_appearances <= 1)

    # Rule 7: Library (Period 4 or 7)
    library_subjects = ['LIB_HH', 'Library']
    valid_library_periods = [3, 6]
    for c in all_classes:
        c_i = class_idx[c]
        full_list = class_data[c]['subjects']
        for s_name in full_list:
            if s_name in library_subjects and s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days):
                    for p in range(num_periods):
                        if p not in valid_library_periods:
                            model.Add(assign[(c_i, d, p, s_i)] == 0)

    # Optimization: Minimize Repetition
    core_subjects = [
        s for s in all_subjects 
        if '_Lab' not in s and '_Tutorial' not in s
        and s not in ['PW', 'T&P', 'DS-I', 'SSD-III', 'BC', 'CS', 'LIB_HH', 'MH'] 
        and not any(s in g for c_data in class_data.values() for g in c_data['elective_groups'])
    ]
    penalties = []
    for c in all_classes:
        c_i = class_idx[c]
        full_list = class_data[c]['subjects']
        for s_name in full_list:
            if s_name in core_subjects and s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days):
                    model.Add(sum(assign[(c_i, d, p, s_i)] for p in range(num_periods)) <= 2)
                    
                    is_repeated = model.NewBoolVar(f'rep_c{c_i}_d{d}_s{s_i}')
                    daily_sum = sum(assign[(c_i, d, p, s_i)] for p in range(num_periods))
                    model.Add(daily_sum > 1).OnlyEnforceIf(is_repeated)
                    model.Add(daily_sum <= 1).OnlyEnforceIf(is_repeated.Not())
                    penalties.append(is_repeated)
    
    model.Minimize(sum(penalties))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        final_schedule = {}
        for c in all_classes:
            c_i = class_idx[c]
            class_schedule = {}
            for d in range(num_days):
                day_schedule = []
                for p in range(num_periods):
                    slot_info = "--- FREE ---"
                    for s_name, staff_list in fixed_assignments[c].items():
                        if s_name in subject_idx:
                            s_i = subject_idx[s_name]
                            if solver.Value(assign[(c_i, d, p, s_i)]):
                                staff_str = " & ".join(staff_list)
                                slot_info = f"{s_name} ({staff_str})"
                                break 
                    day_schedule.append(slot_info)
                class_schedule[d] = day_schedule
            final_schedule[c] = class_schedule
        return final_schedule
    return None

def generate_timetable(data):
    all_classes = data['classes']
    all_staff = data['staff']
    all_subjects = data['subjects']
    staff_expertise = data['staff_expertise']
    class_data = data['class_data']

    # --- Dynamic Period Calculation ---
    for c in all_classes:
        ideal = {'lecture': 5, 'lab': 3, 'tutorial': 2, 'other': 1, 'pw': 4, 'tp': 4, 'ds': 3, 'ssd': 3, 'bc': 3, 'cs': 2, 'elective': 5}
        periods = defaultdict(int)
        
        for s_name in class_data[c]['labs']:
            periods[s_name] = ideal['lab']

        for s_name in class_data[c]['tutorials']:
            periods[s_name] = ideal['tutorial']
            
        for s_name in class_data[c]['subjects']:
            if s_name in ['PW', 'T&P']: periods[s_name] = ideal['pw']
            elif s_name in ['DS-I', 'SSD-III']: periods[s_name] = ideal['ssd']
            elif s_name in ['BC', 'CS']: periods[s_name] = ideal['bc']
            elif s_name in ['LIB_HH', 'MH']: periods[s_name] = ideal['other']
            
        for group in class_data[c]['elective_groups']:
            for s_name in group:
                periods[s_name] = ideal['elective']
        
        core_lectures = [s for s in class_data[c]['subjects'] if s not in periods and '_Lab' not in s and s in staff_expertise]
        
        elective_cost = sum(ideal['elective'] for g in class_data[c]['elective_groups'])
        fixed_sum = sum(v for k,v in periods.items() if not any(k in g for g in class_data[c]['elective_groups']))
        
        current_total = fixed_sum + elective_cost
        remaining = 42 - current_total
        
        if core_lectures:
            base = remaining // len(core_lectures)
            rem = remaining % len(core_lectures)
            for i, s_name in enumerate(core_lectures):
                periods[s_name] = base + (1 if i < rem else 0)
        
        class_data[c]['periods_per_subject'] = periods

    assignments = solve_staff_assignment(all_classes, all_staff, all_subjects, staff_expertise, class_data)
    
    if not assignments:
        return {"status": "error", "message": "Staff Assignment Failed"}
        
    schedule = solve_scheduling(all_classes, all_staff, all_subjects, assignments, class_data)
    
    if schedule:
        return {"status": "success", "schedule": schedule}
    else:
        return {"status": "error", "message": "Scheduling Failed (Over-constrained)"}