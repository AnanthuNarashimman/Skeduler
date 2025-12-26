from ortools.sat.python import cp_model
from collections import defaultdict

def generate_timetable(data):
    """
    FINAL ENGINE (VIII_SEM Half-Day Logic).
    - VIII_SEM_A/B: Strictly scheduled in Periods 1-4 (Indices 0-3).
      Periods 5-7 are left empty (Project Work).
    - Other Classes: Full day scheduling with Saturday restrictions.
    - Diversity & Matrix Dispersion active.
    """
    print("--- Starting Final Engine (VIII_SEM Half-Day) ---")
    
    model = cp_model.CpModel()
    
    # --- Configuration ---
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    num_days = 6
    num_periods = 7
    
    # Mappings
    classes = data['classes']
    all_subjects = data['subjects']
    staff_list = data['staff']
    
    c_map = {name: i for i, name in enumerate(classes)}
    s_map = {name: i for i, name in enumerate(all_subjects)}
    st_map = {name: i for i, name in enumerate(staff_list)}
    
    starts = {}
    assign = {}
    
    staff_slots = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    # Objective Terms
    obj_vars_allocation = []    # +100 per slot filled
    obj_vars_diversity = []     # +50 per unique subject/day
    obj_vars_h_penalty = []     # -20 per consecutive pair
    obj_vars_v_penalty = []     # -20 per vertical repetition

    merged_subjects = set()
    if "VI_SEM_A" in c_map and "VI_SEM_B" in c_map:
        merged_subjects = set(data['class_data']["VI_SEM_A"]['subjects']) & set(data['class_data']["VI_SEM_B"]['subjects'])

    print("Building Model...")

    for c_name in classes:
        c = c_map[c_name]
        c_data = data['class_data'][c_name]
        
        all_subs = (c_data['subjects'] + c_data['labs'] + c_data['tutorials'] + 
                   c_data.get('integrated', []) + c_data.get('special', []))
        unique_subs = list(set(all_subs))

        for s_name in unique_subs:
            s = s_map[s_name]
            staff_names = c_data['assignments'].get(s_name, [])
            staff_indices = [st_map[st] for st in staff_names if st in st_map]

            skip_staff_check = False
            if c_name == "VI_SEM_B" and s_name in merged_subjects:
                staff_A = data['class_data']["VI_SEM_A"]['assignments'].get(s_name, [])
                if set(staff_names) == set(staff_A):
                    skip_staff_check = True

            is_lab = s_name in c_data['labs']
            is_integrated = s_name in c_data.get('integrated', [])
            is_tutorial = s_name in c_data['tutorials']
            is_special = s_name in c_data.get('special', [])
            
            # --- Type Config ---
            duration = 1
            valid_starts = []
            freq_min, freq_max = 0, 0
            is_lecture = False
            
            # Default Allowed Days (Mon-Sat = 0-5)
            allowed_days = list(range(num_days)) 
            
            if is_lab:
                duration = 3
                valid_starts = [1, 4]
                freq_min, freq_max = 1, 1
                allowed_days = list(range(num_days - 1)) # Mon-Fri
            elif is_integrated:
                duration = 2
                valid_starts = [0, 2, 4, 5]
                freq_min, freq_max = 1, 1
                allowed_days = list(range(num_days - 1)) 
            elif is_tutorial:
                duration = 2
                valid_starts = [0, 2, 4, 5]
                freq_min, freq_max = 1, 1
                allowed_days = list(range(num_days - 1)) 
            else: 
                duration = 1
                is_lecture = True 
                if s_name == "MH":
                    valid_starts = [0]
                    freq_min, freq_max = 1, 1
                    is_lecture = False 
                elif "LIB" in s_name or "HH" in s_name:
                    valid_starts = [1, 3, 6]
                    freq_min, freq_max = 1, 1
                    is_lecture = False
                    allowed_days = list(range(num_days - 1)) 
                else:
                    valid_starts = list(range(7))
                    if is_special:
                        freq_min, freq_max = 1, 1
                        is_lecture = False
                        allowed_days = list(range(num_days - 1))
                    else:
                        freq_min, freq_max = 3, 6 

            # --- CONSTRAINT: VIII_SEM HALF-DAY LOGIC ---
            # If Class is VIII_SEM, strictly restrict valid starts to first half (Indices 0,1,2,3).
            # Also ensure the duration doesn't spill over.
            if "VIII_SEM" in c_name:
                # Filter valid_starts to ensure the block ENDS by index 3
                # End index = start + duration - 1. We need end <= 3.
                # So start <= 3 - duration + 1.
                max_start_index = 3 - duration + 1
                valid_starts = [p for p in valid_starts if p <= 3 and p <= max_start_index]

            # --- Start Variables ---
            subject_start_vars = []
            if s_name == "MH":
                v = model.NewBoolVar(f'start_{c}_{s}_Sat_0')
                starts[(c, s, 5, 0)] = v
                subject_start_vars.append(v)
                model.Add(v == 1)
            else:
                for d in allowed_days:
                    for p in valid_starts:
                        if d == 5 and p == 0: continue 
                        
                        v = model.NewBoolVar(f'start_{c}_{s}_{d}_{p}')
                        starts[(c, s, d, p)] = v
                        subject_start_vars.append(v)

            if freq_min == freq_max:
                model.Add(sum(subject_start_vars) == freq_min)
            else:
                model.Add(sum(subject_start_vars) >= freq_min)
                model.Add(sum(subject_start_vars) <= freq_max)

            # --- Link Starts to Grid ---
            daily_assignments = defaultdict(list)

            for d in range(num_days):
                for p in range(num_periods):
                    covering_starts = []
                    min_sp = max(0, p - duration + 1)
                    max_sp = p
                    for sp in range(min_sp, max_sp + 1):
                        if (c, s, d, sp) in starts:
                            covering_starts.append(starts[(c, s, d, sp)])
                    
                    if covering_starts:
                        gv = model.NewBoolVar(f'grid_{c}_{d}_{p}_{s}')
                        assign[(c, d, p, s)] = gv
                        model.Add(gv == sum(covering_starts))
                        
                        obj_vars_allocation.append(gv)
                        daily_assignments[d].append(gv)
                        
                        if not skip_staff_check:
                            for st_idx in staff_indices:
                                staff_slots[st_idx][d][p].append(gv)

                # Diversity Reward
                if daily_assignments[d]:
                    is_present = model.NewBoolVar(f'present_{c}_{s}_{d}')
                    model.AddMaxEquality(is_present, daily_assignments[d])
                    obj_vars_diversity.append(is_present)

            # --- LECTURE PENALTIES ---
            if is_lecture:
                # 1. Horizontal
                for d in range(num_days):
                    for p in range(num_periods - 2):
                        if (c, d, p, s) in assign and (c, d, p+1, s) in assign and (c, d, p+2, s) in assign:
                            model.Add(assign[(c, d, p, s)] + assign[(c, d, p+1, s)] + assign[(c, d, p+2, s)] <= 2)

                    for p in range(num_periods - 1):
                        if (c, d, p, s) in assign and (c, d, p+1, s) in assign:
                            penalty_var = model.NewBoolVar(f'h_pen_{c}_{s}_{d}_{p}')
                            model.Add(assign[(c, d, p, s)] + assign[(c, d, p+1, s)] == 2).OnlyEnforceIf(penalty_var)
                            model.Add(assign[(c, d, p, s)] + assign[(c, d, p+1, s)] < 2).OnlyEnforceIf(penalty_var.Not())
                            obj_vars_h_penalty.append(penalty_var)

                # 2. Vertical
                for d in range(num_days - 1):
                    for p in range(num_periods):
                        if (c, d, p, s) in assign and (c, d+1, p, s) in assign:
                            v_penalty_var = model.NewBoolVar(f'v_pen_{c}_{s}_{d}_{p}')
                            model.Add(assign[(c, d, p, s)] + assign[(c, d+1, p, s)] == 2).OnlyEnforceIf(v_penalty_var)
                            model.Add(assign[(c, d, p, s)] + assign[(c, d+1, p, s)] < 2).OnlyEnforceIf(v_penalty_var.Not())
                            obj_vars_v_penalty.append(v_penalty_var)

    print("Adding Constraints...")

    # 1. Elective Group Synchronization
    for c_name in classes:
        c = c_map[c_name]
        c_data = data['class_data'][c_name]
        for group in c_data.get('elective_groups', []):
            if not group: continue
            leader = group[0]
            leader_idx = s_map[leader]
            for follower in group[1:]:
                follower_idx = s_map[follower]
                for d in range(num_days):
                    for p in range(num_periods):
                        if (c, d, p, leader_idx) in assign and (c, d, p, follower_idx) in assign:
                            model.Add(assign[(c, d, p, leader_idx)] == assign[(c, d, p, follower_idx)])
                        elif (c, d, p, leader_idx) in assign:
                             model.Add(assign[(c, d, p, leader_idx)] == 0)
                        elif (c, d, p, follower_idx) in assign:
                             model.Add(assign[(c, d, p, follower_idx)] == 0)

    # 2. One Class, One Subject per Slot
    for c_name in classes:
        c = c_map[c_name]
        c_data = data['class_data'][c_name]
        followers = set()
        for group in c_data.get('elective_groups', []):
            for s in group[1:]: followers.add(s)
            
        for d in range(num_days):
            for p in range(num_periods):
                active_vars = []
                for s in range(len(all_subjects)):
                    s_name = all_subjects[s]
                    if s_name in followers: continue
                    if (c, d, p, s) in assign:
                        active_vars.append(assign[(c, d, p, s)])
                if active_vars:
                    model.Add(sum(active_vars) <= 1)

    # 3. Staff No-Overlap
    for st in range(len(staff_list)):
        for d in range(num_days):
            for p in range(num_periods):
                if staff_slots[st][d][p]:
                    model.Add(sum(staff_slots[st][d][p]) <= 1)

    # 4. Daily Limits
    for c_name in classes:
        c = c_map[c_name]
        c_data = data['class_data'][c_name]
        lab_indices = [s_map[s] for s in c_data['labs'] if s in s_map]
        int_indices = [s_map[s] for s in c_data.get('integrated', []) if s in s_map]
        tut_indices = [s_map[s] for s in c_data['tutorials'] if s in s_map]
        
        for d in range(num_days):
            daily_lab = [assign[(c, d, p, s_i)] for s_i in lab_indices for p in range(num_periods) if (c, d, p, s_i) in assign]
            if daily_lab: model.Add(sum(daily_lab) <= 3)
            
            daily_int = [assign[(c, d, p, s_i)] for s_i in int_indices for p in range(num_periods) if (c, d, p, s_i) in assign]
            if daily_int: model.Add(sum(daily_int) <= 2)

            daily_tut = [assign[(c, d, p, s_i)] for s_i in tut_indices for p in range(num_periods) if (c, d, p, s_i) in assign]
            if daily_tut: model.Add(sum(daily_tut) <= 2)

    # 5. Merged Classes Link
    if "VI_SEM_A" in c_map and "VI_SEM_B" in c_map:
        ca, cb = c_map["VI_SEM_A"], c_map["VI_SEM_B"]
        for s_name in merged_subjects:
            if "Lab" in s_name or "LAB" in s_name: continue
            s = s_map[s_name]
            for d in range(num_days):
                for p in range(num_periods):
                    if (ca, d, p, s) in assign and (cb, d, p, s) in assign:
                        model.Add(assign[(ca, d, p, s)] == assign[(cb, d, p, s)])

    # --- OBJECTIVE ---
    model.Maximize( 
        (100 * sum(obj_vars_allocation)) + 
        (50 * sum(obj_vars_diversity)) - 
        (20 * sum(obj_vars_h_penalty)) -
        (20 * sum(obj_vars_v_penalty))
    )

    # --- Solve ---
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 120.0
    status = solver.Solve(model)
    
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"Solution Found! (Status: {status})")
        final_schedule = {}
        for c_name in classes:
            c = c_map[c_name]
            c_data = data['class_data'][c_name]
            class_sched = {}
            for d in range(num_days):
                day_sched = []
                for p in range(num_periods):
                    slot_txt = "-- FREE --"
                    # For VIII_SEM, assume FREE slots in afternoon are PW
                    if "VIII_SEM" in c_name and p >= 4:
                        slot_txt = "Project Work (No Staff)"
                    
                    for s_name in all_subjects:
                        s = s_map[s_name]
                        if (c, d, p, s) in assign:
                            if solver.Value(assign[(c, d, p, s)]):
                                st_names = " & ".join(data['class_data'][c_name]['assignments'].get(s_name, []))
                                
                                # Add type markers for frontend styling
                                if s_name in c_data['labs']:
                                    slot_txt = f"[LAB] {s_name} ({st_names})"
                                elif s_name in c_data.get('integrated', []):
                                    slot_txt = f"[INT-LAB] {s_name} ({st_names})"
                                elif s_name in c_data['tutorials']:
                                    slot_txt = f"[TUT] {s_name} ({st_names})"
                                else:
                                    slot_txt = f"{s_name} ({st_names})"
                                break
                    day_sched.append(slot_txt)
                class_sched[days[d]] = day_sched
            final_schedule[c_name] = class_sched
        return {"status": "success", "schedule": final_schedule}
    
    else:
        print("No Solution.")
        return {"status": "failed"}