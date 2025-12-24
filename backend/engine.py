from ortools.sat.python import cp_model
from collections import defaultdict

def generate_timetable(data):
    """
    Solves the timetable scheduling problem using pre-assigned staff from Excel.
    RELAXED VERSION: Uses soft constraints to guarantee a solution.
    """
    print("--- Starting Scheduler Engine (Relaxed Mode) ---")
    
    all_classes = data['classes']
    all_staff = data['staff']
    all_subjects = data['subjects']
    class_data = data['class_data']

    # --- 1. Dynamic Period Calculation ---
    for c in all_classes:
        ideal = {'lecture': 5, 'lab': 3, 'tutorial': 2, 'special': 1, 'pw': 4, 'tp': 4, 'ds': 3, 'ssd': 3, 'bc': 3, 'cs': 2, 'elective': 5}
        periods = defaultdict(int)

        for s_name in class_data[c]['labs']: periods[s_name] = ideal['lab']
        for s_name in class_data[c]['tutorials']: periods[s_name] = ideal['tutorial']
        for s_name in class_data[c].get('integrated', []): periods[s_name] = 4
        for s_name in class_data[c].get('special', []): periods[s_name] = ideal['special']

        for s_name in class_data[c]['subjects']:
            if s_name in ['PW', 'T&P']: periods[s_name] = ideal['pw']
            elif s_name in ['DS-I', 'SSD-III']: periods[s_name] = ideal['ssd']
            elif s_name in ['BC', 'CS']: periods[s_name] = ideal['bc']
            elif s_name in ['LIB_HH', 'LIB / HH', 'MH']: periods[s_name] = ideal['special']

        for group in class_data[c]['elective_groups']:
            for s_name in group: periods[s_name] = ideal['elective']

        core_lectures = [s for s in class_data[c]['subjects'] if s not in periods and '_Lab' not in s]

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

    # --- 2. Build Model ---
    model = cp_model.CpModel()
    num_days = 6
    num_periods = 7
    
    class_idx = {name: i for i, name in enumerate(all_classes)}
    staff_idx = {name: i for i, name in enumerate(all_staff)}
    subject_idx = {name: i for i, name in enumerate(all_subjects)}

    # Variables
    assign = {}
    for c_i in range(len(all_classes)):
        for d in range(num_days):
            for p in range(num_periods):
                for s_i in range(len(all_subjects)):
                    assign[(c_i, d, p, s_i)] = model.NewBoolVar(f'a_c{c_i}d{d}p{p}s{s_i}')

    # Helper Variables
    lab_starts = {}
    valid_lab_starts = [1, 4]
    tutorial_starts = {}
    valid_tutorial_starts = [0, 1, 2, 4, 5]
    integrated_starts = {}
    valid_integrated_starts = [0, 1, 2, 4, 5]

    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['labs']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days - 1):
                    for p in valid_lab_starts:
                        lab_starts[(c_i, d, p, s_i)] = model.NewBoolVar(f'ls_c{c_i}d{d}p{p}s{s_i}')
        for s_name in class_data[c]['tutorials']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days - 1):
                    for p in valid_tutorial_starts:
                        tutorial_starts[(c_i, d, p, s_i)] = model.NewBoolVar(f'ts_c{c_i}d{d}p{p}s{s_i}')
        for s_name in class_data[c].get('integrated', []):
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days - 1):
                    for p in valid_integrated_starts:
                        integrated_starts[(c_i, d, p, s_i)] = model.NewBoolVar(f'is_c{c_i}d{d}p{p}s{s_i}')

    # --- Constraints ---

    # 1. Single Activity Per Slot (HARD)
    for c in all_classes:
        c_i = class_idx[c]
        for d in range(num_days):
            for p in range(num_periods):
                active_vars = []
                full_list = class_data[c]['subjects'] + class_data[c]['labs'] + class_data[c]['tutorials'] + class_data[c].get('integrated', []) + class_data[c].get('special', [])
                normal_subjects = [s for s in full_list if not any(s in g for g in class_data[c]['elective_groups'])]
                for s_name in normal_subjects:
                    if s_name in subject_idx:
                        active_vars.append(assign[(c_i, d, p, subject_idx[s_name])])
                for group in class_data[c]['elective_groups']:
                    if group and group[0] in subject_idx:
                        active_vars.append(assign[(c_i, d, p, subject_idx[group[0]])])
                model.Add(sum(active_vars) <= 1)

        for group in class_data[c]['elective_groups']:
            if group and group[0] in subject_idx:
                first_s_i = subject_idx[group[0]]
                for other_s in group[1:]:
                    if other_s in subject_idx:
                        other_s_i = subject_idx[other_s]
                        for d in range(num_days):
                            for p in range(num_periods):
                                model.Add(assign[(c_i, d, p, first_s_i)] == assign[(c_i, d, p, other_s_i)])

    # 2. Total Periods (HARD)
    for c in all_classes:
        c_i = class_idx[c]
        for s_name, count in class_data[c]['periods_per_subject'].items():
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(assign[(c_i, d, p, s_i)] for d in range(num_days) for p in range(num_periods)) == count)

    # 3. Lab/Tutorial Logic (HARD)
    for c_i, d, p, s_i in lab_starts:
        for i in range(3):
            model.Add(assign[(c_i, d, p + i, s_i)] == 1).OnlyEnforceIf(lab_starts[(c_i, d, p, s_i)])
    
    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['labs']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(lab_starts.get((c_i, d, p, s_i), 0) for d in range(num_days-1) for p in valid_lab_starts) == 1)

    for c_i, d, p, s_i in tutorial_starts:
        for i in range(2):
            model.Add(assign[(c_i, d, p + i, s_i)] == 1).OnlyEnforceIf(tutorial_starts[(c_i, d, p, s_i)])

    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c]['tutorials']:
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(tutorial_starts.get((c_i, d, p, s_i), 0) for d in range(num_days-1) for p in valid_tutorial_starts) == 1)

    for c_i, d, p, s_i in integrated_starts:
        for i in range(2):
            model.Add(assign[(c_i, d, p + i, s_i)] == 1).OnlyEnforceIf(integrated_starts[(c_i, d, p, s_i)])

    for c in all_classes:
        c_i = class_idx[c]
        for s_name in class_data[c].get('integrated', []):
            if s_name in subject_idx:
                s_i = subject_idx[s_name]
                model.Add(sum(integrated_starts.get((c_i, d, p, s_i), 0) for d in range(num_days-1) for p in valid_integrated_starts) == 2)

    # 4. Staff Conflicts (SOFT CONSTRAINT)
    conflict_penalties = []
    for st_name in all_staff:
        for d in range(num_days):
            for p in range(num_periods):
                staff_is_busy = []
                for c in all_classes:
                    c_i = class_idx[c]
                    all_class_subjects = class_data[c]['subjects'] + class_data[c]['labs'] + class_data[c]['tutorials'] + class_data[c].get('integrated', []) + class_data[c].get('special', [])
                    for s_name in all_class_subjects:
                        if s_name in class_data[c]['assignments']:
                            assigned_staff_list = class_data[c]['assignments'][s_name]
                            if st_name in assigned_staff_list:
                                if s_name in subject_idx:
                                    s_i = subject_idx[s_name]
                                    staff_is_busy.append(assign[(c_i, d, p, s_i)])

                if len(staff_is_busy) > 1:
                    is_conflict = model.NewBoolVar(f'is_conflict_{st_name}_{d}_{p}')
                    model.Add(sum(staff_is_busy) > 1).OnlyEnforceIf(is_conflict)
                    model.Add(sum(staff_is_busy) <= 1).OnlyEnforceIf(is_conflict.Not())
                    conflict_penalties.append(is_conflict)

    # 5. Daily Lab/Integrated Limits (SOFT CONSTRAINT)
    daily_lab_penalties = []
    for c in all_classes:
        c_i = class_idx[c]
        for d in range(num_days - 1):
            daily_labs = []
            for s_name in class_data[c]['labs']:
                if s_name in subject_idx:
                    s_i = subject_idx[s_name]
                    for p in valid_lab_starts:
                        daily_labs.append(lab_starts.get((c_i, d, p, s_i), 0))
            for s_name in class_data[c].get('integrated', []):
                if s_name in subject_idx:
                    s_i = subject_idx[s_name]
                    for p in valid_integrated_starts:
                        daily_labs.append(integrated_starts.get((c_i, d, p, s_i), 0))
            
            is_overloaded = model.NewBoolVar(f'lab_overload_{c_i}_{d}')
            model.Add(sum(daily_labs) > 1).OnlyEnforceIf(is_overloaded)
            model.Add(sum(daily_labs) <= 1).OnlyEnforceIf(is_overloaded.Not())
            daily_lab_penalties.append(is_overloaded)

    # 6. Library Rule (Period 4 or 7) - SOFT
    lib_penalties = []
    library_subjects = ['LIB_HH', 'Library', 'LIB / HH', 'LIB/HH']
    for c in all_classes:
        c_i = class_idx[c]
        # Check both regular subjects and special subjects for library
        all_subj_for_lib = class_data[c]['subjects'] + class_data[c].get('special', [])
        for s_name in all_subj_for_lib:
            if s_name in library_subjects and s_name in subject_idx:
                s_i = subject_idx[s_name]
                for d in range(num_days):
                    for p in range(num_periods):
                        if p not in [3, 6]:
                            lib_penalties.append(assign[(c_i, d, p, s_i)])

    # 7. First Period Diversity - SOFT
    fp_penalties = []
    for c_i in range(len(all_classes)):
        for s_i in range(len(all_subjects)):
            first_period_appearances = sum(assign[(c_i, d, 0, s_i)] for d in range(num_days))
            is_repeated_fp = model.NewBoolVar(f'rep_fp_{c_i}_{s_i}')
            model.Add(first_period_appearances > 1).OnlyEnforceIf(is_repeated_fp)
            model.Add(first_period_appearances <= 1).OnlyEnforceIf(is_repeated_fp.Not())
            fp_penalties.append(is_repeated_fp)

    # Optimization: Minimize all penalties
    model.Minimize(
        sum(conflict_penalties) * 1000 + 
        sum(daily_lab_penalties) * 100 + 
        sum(lib_penalties) * 50 + 
        sum(fp_penalties) * 10
    )

    # Solve
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
                    for s_name in data['subjects']:
                        if s_name in subject_idx:
                            s_i = subject_idx[s_name]
                            if solver.Value(assign[(c_i, d, p, s_i)]):
                                staff_list = class_data[c]['assignments'].get(s_name, ["Unassigned"])
                                staff_str = " & ".join(staff_list)
                                slot_info = f"{s_name} ({staff_str})"
                                break
                    day_schedule.append(slot_info)
                class_schedule[d] = day_schedule
            final_schedule[c] = class_schedule
        return {"status": "success", "schedule": final_schedule}
    
    return {"status": "error", "message": "No solution found (Severe Constraints)"}