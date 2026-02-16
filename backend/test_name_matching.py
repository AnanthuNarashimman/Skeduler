"""
Test script to verify staff name matching handles different spellings/spacing correctly
"""
import re


def extract_staff_from_period(period_entry):
    """Extract staff names from a period entry - same logic as app.py"""
    if period_entry and period_entry != '-- FREE --':
        match = re.search(r'\(([^)]+)\)$', period_entry)
        if match:
            staff_str = match.group(1)
            # Split by & or / for multiple staff
            staff_names = [s.strip() for s in re.split(r'\s*[&/]\s*', staff_str)]
            return staff_names
    return []


def test_name_matching():
    """Test various name formats"""
    test_cases = [
        {
            "period": "Data Structures (Mr. Ananthu)",
            "teacher": "Mr. Ananthu",
            "should_match": True,
            "description": "Exact match with space after period"
        },
        {
            "period": "Data Structures (Mr.Ananthu)",
            "teacher": "Mr. Ananthu",
            "should_match": False,
            "description": "Different spacing - should NOT match"
        },
        {
            "period": "Data Structures (Mr. Ananthu)",
            "teacher": "Mr.Ananthu",
            "should_match": False,
            "description": "Different spacing reverse - should NOT match"
        },
        {
            "period": "Algorithms (Anandha Kumaran)",
            "teacher": "Anandha Kumaran",
            "should_match": True,
            "description": "Exact match with space in name"
        },
        {
            "period": "Algorithms (Anandhakumaran)",
            "teacher": "Anandha Kumaran",
            "should_match": False,
            "description": "Different name spelling - should NOT match"
        },
        {
            "period": "Networks (Dr. Anand & Mr. Anandhakumaran)",
            "teacher": "Dr. Anand",
            "should_match": True,
            "description": "Multiple staff - first one matches"
        },
        {
            "period": "Networks (Dr. Anand & Mr. Anandhakumaran)",
            "teacher": "Anand",
            "should_match": False,
            "description": "Substring in staff name - should NOT match (no title)"
        },
        {
            "period": "Database (Mr. Ananthu Kumar)",
            "teacher": "Mr. Ananthu",
            "should_match": False,
            "description": "Teacher name is substring - should NOT match"
        },
    ]
    
    print("=" * 80)
    print("STAFF NAME MATCHING TEST")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        period = test["period"]
        teacher = test["teacher"]
        should_match = test["should_match"]
        description = test["description"]
        
        # Extract staff names using the same logic as the fixed app.py
        staff_in_period = extract_staff_from_period(period)
        actual_match = teacher in staff_in_period
        
        # Check if result matches expectation
        test_passed = actual_match == should_match
        status = "✓ PASS" if test_passed else "✗ FAIL"
        
        if test_passed:
            passed += 1
        else:
            failed += 1
        
        print(f"Test {i}: {status}")
        print(f"  Description: {description}")
        print(f"  Period: {period}")
        print(f"  Teacher: '{teacher}'")
        print(f"  Extracted Staff: {staff_in_period}")
        print(f"  Expected Match: {should_match}, Actual Match: {actual_match}")
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = test_name_matching()
    exit(0 if success else 1)
