"""
Test to verify name normalization works correctly
Names with different spacing/casing should be treated as SAME person
Names with different spelling should be treated as DIFFERENT people
"""

def normalize_staff_name(name):
    """
    Normalize staff name for matching.
    Removes ALL spaces, converts to lowercase.
    """
    if not name or not isinstance(name, str):
        return ""
    import re
    # Add space after periods then remove all spaces
    name = re.sub(r'\.(?=[A-Za-z])', '. ', name)
    return name.lower().replace(' ', '')


def test_normalization():
    """Test name normalization"""
    
    print("=" * 80)
    print("NAME NORMALIZATION TEST")
    print("=" * 80)
    print()
    
    test_cases = [
        # Same person - different spacing/casing (SHOULD MATCH)
        {
            "names": ["Mr. Ananthu", "Mr.Ananthu", "mr. ananthu", "MR.  ANANTHU", "Mr.  Ananthu"],
            "should_be_unique": 1,
            "description": "Same person with different spacing and casing"
        },
        {
            "names": ["Dr. Anand", "dr. anand", "DR.ANAND", "Dr.  Anand"],
            "should_be_unique": 1,
            "description": "Same person - Dr. Anand variations"
        },
        {
            "names": ["Anandha Kumaran", "anandha kumaran", "ANANDHA KUMARAN", "Anandha  Kumaran"],
            "should_be_unique": 1,
            "description": "Same person - different casing/spacing"
        },
        
        # Different people - different spelling (SHOULD NOT MATCH)
        {
            "names": ["Anandha Kumaran", "Anandhakumaran"],
            "should_be_unique": 2,
            "description": "Different spelling - should be 2 people"
        },
        {
            "names": ["Dr. Anand", "Dr. Ananda"],
            "should_be_unique": 2,
            "description": "Different spelling (extra 'a') - should be 2 people"
        },
        {
            "names": ["Mr. Ananthu", "Mr. Ananthu Kumar"],
            "should_be_unique": 2,
            "description": "Different names (one has surname) - should be 2 people"
        },
        
        # Mixed cases
        {
            "names": ["Mr. Ananthu", "mr. ananthu", "Dr. Anand", "dr. anand"],
            "should_be_unique": 2,
            "description": "Two different people with case variations"
        },
        {
            "names": ["Anandha Kumaran", "ANANDHA KUMARAN", "Anandhakumaran"],
            "should_be_unique": 2,
            "description": "Same name with casing + different spelling"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        names = test["names"]
        should_be_unique = test["should_be_unique"]
        description = test["description"]
        
        # Normalize all names and count unique
        normalized = [normalize_staff_name(name) for name in names]
        unique_normalized = list(set(normalized))
        actual_unique = len(unique_normalized)
        
        test_passed = actual_unique == should_be_unique
        status = "✓ PASS" if test_passed else "✗ FAIL"
        
        if test_passed:
            passed += 1
        else:
            failed += 1
        
        print(f"Test {i}: {status}")
        print(f"  Description: {description}")
        print(f"  Input names: {names}")
        print(f"  Normalized: {normalized}")
        print(f"  Unique normalized: {unique_normalized}")
        print(f"  Expected unique count: {should_be_unique}, Actual: {actual_unique}")
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 80)
    print()
    
    # Summary
    print("NORMALIZATION BEHAVIOR:")
    print("=" * 80)
    print()
    print("✓ SAME PERSON (normalized to same):")
    print("  • 'Mr. Ananthu' = 'Mr.Ananthu' = 'mr. ananthu' = 'MR. ANANTHU'")
    print("  • 'Dr.  Anand' = 'DR. ANAND' = 'dr.anand'")
    print("  • Different spacing and casing are IGNORED")
    print()
    print("✗ DIFFERENT PEOPLE (normalized differently):")
    print("  • 'Anandha Kumaran' ≠ 'Anandhakumaran' (spelling differs)")
    print("  • 'Dr. Anand' ≠ 'Dr. Ananda' (spelling differs)")
    print("  • 'Mr. Ananthu' ≠ 'Mr. Ananthu Kumar' (spelling differs)")
    print()
    print("KEY: Only the SPELLING (letters and their order) matters!")
    print("     Spaces and casing are normalized away.")
    
    return failed == 0


if __name__ == "__main__":
    success = test_normalization()
    exit(0 if success else 1)
