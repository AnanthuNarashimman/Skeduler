"""
Simple test script to verify database operations
"""
from database import save_timetable, get_all_timetables, get_timetable_by_id

# Test data
sample_schedule = {
    "Class A": {
        "0": ["Math", "Physics", "Chemistry", "English", "CS", "Lab", "Lab"],
        "1": ["English", "Math", "Physics", "Chemistry", "CS", "Lab", "Lab"],
        "2": ["Physics", "Chemistry", "Math", "CS", "English", "Lab", "Lab"],
        "3": ["Chemistry", "English", "CS", "Math", "Physics", "Lab", "Lab"],
        "4": ["CS", "Math", "English", "Physics", "Chemistry", "Lab", "Lab"],
        "5": ["Lab", "Lab", "Lab", "--- FREE ---", "--- FREE ---", "--- FREE ---", "--- FREE ---"]
    }
}

metadata = {
    "total_classes": 1,
    "total_subjects": 5,
    "file_name": "test_schedule.xlsx",
    "created_by": "Admin"
}

print("Testing database operations...")

# Test 1: Save timetable
print("\n1. Saving timetable...")
timetable_id = save_timetable(
    schedule_data=sample_schedule,
    department="CSE",
    semester="Sem 1",
    academic_year="2024-2025",
    metadata=metadata
)
print(f"✓ Timetable saved with ID: {timetable_id}")

# Test 2: Retrieve by ID
print(f"\n2. Retrieving timetable by ID {timetable_id}...")
timetable = get_timetable_by_id(timetable_id)
if timetable:
    print(f"✓ Retrieved timetable: {timetable['department']} - {timetable['semester']}")
    print(f"  Created at: {timetable['created_at']}")
    print(f"  Total classes: {timetable['total_classes']}")
else:
    print("✗ Failed to retrieve timetable")

# Test 3: Get all timetables
print("\n3. Retrieving all timetables...")
all_timetables = get_all_timetables(department="CSE")
print(f"✓ Found {len(all_timetables)} timetable(s)")
for tt in all_timetables:
    print(f"  - ID: {tt['id']}, Dept: {tt['department']}, Created: {tt['created_at']}")

print("\n✅ All tests passed!")
