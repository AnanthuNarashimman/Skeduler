"""
Test script to verify Period 0 diversity constraint
"""
import json
from engine import generate_timetable

# Load sample data
with open('data.json', 'r') as f:
    data = json.load(f)

print("=" * 80)
print("Testing Period 0 Diversity Constraint")
print("=" * 80)

# Test with the data
print("\nGenerating timetable with Period 0 constraint...")
result = generate_timetable(data)

if result['status'] == 'success':
    print("\n✓ Timetable generated successfully!")

    # Verify Period 0 diversity for each class
    schedule = result['schedule']

    for class_name, class_schedule in schedule.items():
        print(f"\n{class_name}:")
        print("-" * 40)

        period_0_subjects = []
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

        for day_idx in range(6):
            day_schedule = class_schedule[day_idx]
            period_0 = day_schedule[0]  # First period
            period_0_subjects.append(period_0)
            print(f"  {days[day_idx]:12s} Period 0: {period_0}")

        # Check if all Period 0 subjects are different
        unique_subjects = set(period_0_subjects)
        if len(unique_subjects) == 6:
            print(f"  ✓ All 6 days have DIFFERENT subjects in Period 0")
        else:
            print(f"  ✗ WARNING: Only {len(unique_subjects)} unique subjects in Period 0")
            print(f"    Repeated: {[s for s in period_0_subjects if period_0_subjects.count(s) > 1]}")
else:
    print(f"\n✗ Failed to generate timetable: {result['message']}")

print("\n" + "=" * 80)
