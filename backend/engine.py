from ortools.sat.python import cp_model
from collections import defaultdict

def solve_staff_assignment(all_classes, all_staff, all_subjects, staff_expertise, class_data):
    """
    Step 1: Assigns staff to subjects to balance workload.
    """
    print("--- Step 1: Solving Staff Assignment ---")
    model = cp_model.CpModel()
    
    class_idx = {name: i for i, name in enumerate(all_classes)}
    staff_idx = {name: i for i, name in enumerate(all_staff)}
    subject_idx = {name: i for i, name in enumerate(all_subjects)}

    assigns = {}
    
    # Create assignment variables
    for c in all_classes:
        # Combine subjects and labs for assignment
        full_subject_list = class_data[c]['subjects'] + class_data[c]['labs']
        
        for s_name in full_subject_list:
            if s_name in staff_expertise:
                for st_name in staff_expertise[s_name]:
                    if st_name in staff_idx:
                        c_i, s_i, st_i = class_idx[c], subject_idx[s_name], staff_idx[st_name]
                        assigns[(c_i, s_i, st_i)] = model.NewBoolVar(f'assign_c{c_i}_s{s_i}_st{st_i}')

    # Constraint: Each subject must have exactly one staff member assigned
    for c in all_classes:
        full_subject_list = class_data[c]['subjects'] + class_data[c]['labs']
        for s_name in full_subject_list:
            if s_name in staff_expertise:
                c_i, s_i = class_idx[c], subject_idx[s_name]
                qualified_staff_vars = [
                    assigns[(c_i, s_i, staff_idx[st_name])] 
                    for st_name in staff_expertise[s_name] 
                    if st_name in staff_idx
                ]
                if qualified_staff_vars:
                    model.AddExactlyOne(qualified_staff_vars)

    # Objective: Balance workload
    workload = {}
    for st_name in all_staff:
        st_i = staff_idx[st_name]
        total_periods = []
        for c in all_classes:
            full_subject_list = class_data[c]['subjects'] + class_data[c]['labs']
            for s_name in full_subject_list:
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
            full_subject_list = class_data[c]['subjects'] + class_data[c]['labs']
            for s_name in full_subject_list:
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

def get_schedulable_units(class_name, class_data, subject_idx):
    """
    Returns a list of subject indices that can be independently scheduled.
    Treats elective groups as single units (using first subject as representative).
    """
    schedulable = []
    elective_subjects = set()

    # Collect all subjects in elective groups
    for group in class_data[class_name]['elective_groups']:
        for s in group:
            elective_subjects.add(s)

    # Add non-elective subjects and labs
    full_list = class_data[class_name]['subjects'] + class_data[class_name]['labs']
    for s_name in full_list:
        if s_name not in elective_subjects and s_name in subject_idx:
            schedulable.append(subject_idx[s_name])

    # Add one representative from each elective group
    for group in class_data[class_name]['elective_groups']:
        if group and group[0] in subject_idx:
            schedulable.append(subject_idx[group[0]])

    return schedulable

def solve_scheduling(all_classes, all_staff, all_subjects, fixed_assignments, class_data):
    """
    Step 2: Solves the timing puzzle using fixed staff assignments.
    """
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
    
    lab_starts = {}
    valid_lab_starts = [1, 4] # Start at Period 2 or Period 5
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['labs']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days - 1): # No labs Saturday
                    for p in valid_lab_starts:
                        lab_starts[(c_i, d, p, s_i)] = model.NewBoolVar(f'lab_start_c{c_i}_d{d}_p{p}_s{s_i}')
    
    # --- Constraints ---
    
    # Rule 1: Single Activity per Slot (handling electives)
    for c in all_classes:
        c_i = class_idx[c]
        for d in range(num_days):
            for p in range(num_periods):
                all_activities = []
                
                # Non-elective subjects + labs
                full_list = class_data[c]['subjects'] + class_data[c]['labs']
                non_electives = [s for s in full_list if not any(s in g for g in class_data[c]['elective_groups'])]
                
                for s_name in non_electives:
                    if s_name in subject_idx:
                        all_activities.append(assign[(c_i, d, p, subject_idx[s_name])])
                
                # Elective groups (count 1 per group)
                for group in class_data[c]['elective_groups']:
                    if group and group[0] in subject_idx:
                        all_activities.append(assign[(c_i, d, p, subject_idx[group[0]])])
                
                model.Add(sum(all_activities) <= 1)

        # Link electives in a group
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

    # Rule 4: Staff Conflicts
    for st_name in all_staff:
        for d in range(num_days):
            for p in range(num_periods):
                active = []
                for c in all_classes:
                    c_i = class_idx[c]
                    if c in fixed_assignments:
                        for s_name, staff in fixed_assignments[c].items():
                            if staff == st_name and s_name in subject_idx:
                                s_i = subject_idx[s_name]
                                active.append(assign[(c_i, d, p, s_i)])
                if active:
                    model.Add(sum(active) <= 1)

    # Rule 5: One Lab per Class per Day
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

    # Rule 6: First Period Diversity (Different subject in Period 0 each day)
    for c in all_classes:
        c_i = class_idx[c]
        schedulable_units = get_schedulable_units(c, class_data, subject_idx)

        # For each pair of days, ensure different subjects in Period 0
        for d1 in range(num_days):
            for d2 in range(d1 + 1, num_days):
                # Collect which subjects are scheduled in Period 0 on each day
                for s_i in schedulable_units:
                    # If subject s_i is in Period 0 on day d1, it cannot be in Period 0 on day d2
                    both_scheduled = model.NewBoolVar(f'both_p0_c{c_i}_d{d1}_d{d2}_s{s_i}')
                    model.AddBoolAnd([assign[(c_i, d1, 0, s_i)], assign[(c_i, d2, 0, s_i)]]).OnlyEnforceIf(both_scheduled)
                    model.AddBoolOr([assign[(c_i, d1, 0, s_i)].Not(), assign[(c_i, d2, 0, s_i)].Not()]).OnlyEnforceIf(both_scheduled.Not())
                    model.Add(both_scheduled == 0)  # Ensure it's always false (no subject appears in Period 0 on two different days)

    # Optimization: Minimize Repetition
    core_subjects = [
        s for s in all_subjects 
        if '_Lab' not in s 
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
                    model.Add(sum(assign[(c_i, d, p, s_i)] for p in range(num_periods)) <= 2) # Hard limit
                    
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
    Main entry point.
    Data comes directly from excel_parser.py structure.
    """
    all_classes = data['classes']
    all_staff = data['staff']
    all_subjects = data['subjects']
    staff_expertise = data['staff_expertise']
    class_data = data['class_data']

    # --- Dynamic Period Calculation ---
    # We must calculate 'periods_per_subject' because the parser leaves it empty.
    for c in all_classes:
        # Heuristics for standard periods
        ideal = {'lecture': 5, 'lab': 3, 'other': 1, 'pw': 4, 'tp': 4, 'ds': 3, 'ssd': 3, 'bc': 3, 'cs': 2, 'elective': 5}
        periods = defaultdict(int)
        
        # 1. Assign Labs (Fixed 3 periods)
        for s_name in class_data[c]['labs']:
            periods[s_name] = ideal['lab']
            
        # 2. Assign Known Special Subjects (Heuristic matching)
        for s_name in class_data[c]['subjects']:
            if s_name in ['PW', 'T&P']: periods[s_name] = ideal['pw']
            elif s_name in ['DS-I', 'SSD-III']: periods[s_name] = ideal['ssd']
            elif s_name in ['BC', 'CS']: periods[s_name] = ideal['bc']
            elif s_name in ['LIB_HH', 'MH']: periods[s_name] = ideal['other']
            
        # 3. Assign Electives
        for group in class_data[c]['elective_groups']:
            for s_name in group:
                periods[s_name] = ideal['elective']
        
        # 4. Distribute Remaining to Core Lectures
        # Core = Subjects that are NOT labs and NOT already assigned a period count
        core_lectures = [
            s for s in class_data[c]['subjects'] 
            if s not in periods
        ]
        
        # Calculate used slots
        # Note: Elective groups only consume slots for ONE subject in the group
        elective_cost = sum(ideal['elective'] for g in class_data[c]['elective_groups'])
        
        # Sum of all fixed periods (excluding raw elective subjects, using group cost instead)
        fixed_sum = sum(v for k,v in periods.items() if not any(k in g for g in class_data[c]['elective_groups']))
        
        current_total = fixed_sum + elective_cost
        remaining = 42 - current_total
        
        if core_lectures:
            base = remaining // len(core_lectures)
            rem = remaining % len(core_lectures)
            for i, s_name in enumerate(core_lectures):
                periods[s_name] = base + (1 if i < rem else 0)
        
        # Save back to class_data so solvers can use it
        class_data[c]['periods_per_subject'] = periods

    # --- Run Optimization ---
    assignments = solve_staff_assignment(all_classes, all_staff, all_subjects, staff_expertise, class_data)
    
    if not assignments:
        return {"status": "error", "message": "Staff Assignment Failed (Workload/Qualification Imbalance)"}
        
    schedule = solve_scheduling(all_classes, all_staff, all_subjects, assignments, class_data)
    
    if schedule:
        return {"status": "success", "schedule": schedule}
    else:
        return {"status": "error", "message": "Scheduling Failed (Time/Room Conflict)"}