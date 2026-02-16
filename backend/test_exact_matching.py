"""
Test to verify EXACT matching behavior - spacing, casing, and spelling all matter
"""

def test_python_exact_matching():
    """Test Python's exact string matching behavior"""
    
    print("=" * 80)
    print("PYTHON EXACT STRING MATCHING TEST")
    print("=" * 80)
    print()
    
    test_cases = [
        # Test spacing
        ("Mr. Ananthu", "Mr. Ananthu", True, "Exact match"),
        ("Mr. Ananthu", "Mr.Ananthu", False, "Different spacing (no space after period)"),
        ("Mr. Ananthu", "Mr.  Ananthu", False, "Different spacing (extra space)"),
        
        # Test casing
        ("Mr. Ananthu", "mr. ananthu", False, "Different casing (lowercase)"),
        ("Mr. Ananthu", "MR. ANANTHU", False, "Different casing (uppercase)"),
        ("Mr. Ananthu", "Mr. ananthu", False, "Different casing (name lowercase)"),
        
        # Test spelling
        ("Anandha Kumaran", "Anandhakumaran", False, "Different spelling (no space in second)"),
        ("Anandha Kumaran", "Ananda Kumaran", False, "Different spelling (one 'h' missing)"),
        ("Dr. Anand", "Dr. Ananda", False, "Different spelling (extra 'a')"),
        
        # Test combination
        ("Mr. Ananthu Kumar", "Mr. Ananthu", False, "Different (second is substring)"),
        ("Ananthu", "Mr. Ananthu", False, "Different (first is substring)"),
    ]
    
    passed = 0
    failed = 0
    
    for name1, name2, should_match, description in test_cases:
        # Test how Python's 'in' operator works with lists (same as our code)
        staff_list = [name1]
        actual_match = name2 in staff_list
        
        # Also test dictionary keys (used in engine.py)
        staff_dict = {name1: 1}
        dict_match = name2 in staff_dict
        
        test_passed = (actual_match == should_match) and (dict_match == should_match)
        status = "✓ PASS" if test_passed else "✗ FAIL"
        
        if test_passed:
            passed += 1
        else:
            failed += 1
        
        print(f"{status} - {description}")
        print(f"  Name 1: '{name1}'")
        print(f"  Name 2: '{name2}'")
        print(f"  Expected Match: {should_match}")
        print(f"  List Match: {actual_match}, Dict Match: {dict_match}")
        
        # Show character-by-character comparison for failed tests
        if not test_passed or not should_match:
            print(f"  Character comparison:")
            print(f"    Name 1 length: {len(name1)} chars")
            print(f"    Name 2 length: {len(name2)} chars")
            if len(name1) == len(name2):
                diffs = [i for i in range(len(name1)) if name1[i] != name2[i]]
                if diffs:
                    print(f"    Different at positions: {diffs}")
                    for i in diffs:
                        print(f"      Position {i}: '{name1[i]}' (ASCII {ord(name1[i])}) vs '{name2[i]}' (ASCII {ord(name2[i])})")
        print()
    
    print("=" * 80)
    print(f"RESULTS: {passed} passed, {failed} failed out of {passed + failed} tests")
    print("=" * 80)
    print()
    
    # Summary statement
    print("CONCLUSION:")
    print("Python string matching is EXACT and requires:")
    print("  ✓ Same spelling (character-by-character)")
    print("  ✓ Same spacing (every space matters)")
    print("  ✓ Same casing (case-sensitive)")
    print()
    print("Examples of DIFFERENT names:")
    print("  • 'Mr. Ananthu' ≠ 'Mr.Ananthu' (spacing)")
    print("  • 'Mr. Ananthu' ≠ 'mr. ananthu' (casing)")
    print("  • 'Anandha Kumaran' ≠ 'Anandhakumaran' (spelling/spacing)")
    
    return failed == 0


if __name__ == "__main__":
    success = test_python_exact_matching()
    exit(0 if success else 1)
