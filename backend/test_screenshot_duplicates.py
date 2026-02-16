"""
Test to verify the exact duplicate names from the screenshot will be merged
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


def test_screenshot_duplicates():
    """Test the exact duplicate names from the screenshot"""
    
    print("=" * 80)
    print("SCREENSHOT DUPLICATE TEST - Verifying Duplicates Will Be Merged")
    print("=" * 80)
    print()
    
    test_cases = [
        {
            "variants": ["Dr. A. Rajiv Kannan", "Dr. A. Rajivkannan"],
            "description": "Dr. Rajiv Kannan with/without space in name"
        },
        {
            "variants": ["Dr. E. Baby Anitha", "Dr. E. BabyAnitha"],
            "description": "Dr. Baby Anitha with/without space in name"
        },
        {
            "variants": ["Dr.A.Rajiv Kannan", "Dr. A. Rajivkannan", "DR.A.RAJIVKANNAN"],
            "description": "Dr. Rajiv Kannan various spacing/casing"
        },
    ]
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        variants = test["variants"]
        description = test["description"]
        
        # Normalize all variants
        normalized = [normalize_staff_name(name) for name in variants]
        unique_normalized = list(set(normalized))
        
        # Should all normalize to the same value (1 unique)
        test_passed = len(unique_normalized) == 1
        status = "✓ MERGED" if test_passed else "✗ STILL DUPLICATE"
        
        if not test_passed:
            all_passed = False
        
        print(f"Test {i}: {status}")
        print(f"  Description: {description}")
        print(f"  Variants: {variants}")
        print(f"  Normalized to: {normalized}")
        print(f"  Unique count: {len(unique_normalized)} (should be 1)")
        if len(unique_normalized) == 1:
            print(f"  ✓ All variants normalize to: '{unique_normalized[0]}'")
        else:
            print(f"  ✗ Different normalized values: {unique_normalized}")
        print()
    
    print("=" * 80)
    if all_passed:
        print("✓ SUCCESS: All duplicates from screenshot will be MERGED")
    else:
        print("✗ FAILED: Some duplicates will still appear separately")
    print("=" * 80)
    print()
    
    # Show more examples
    print("NORMALIZATION EXAMPLES:")
    print("=" * 80)
    examples = [
        "Dr. A. Rajiv Kannan",
        "Dr. A. Rajivkannan",
        "Dr.A.Rajivkannan",
        "dr.a.rajiv kannan",
        "Dr. E. Baby Anitha",
        "Dr. E. BabyAnitha",
        "Dr.E.BabyAnitha"
    ]
    
    for example in examples:
        normalized = normalize_staff_name(example)
        print(f"'{example:30s}' → '{normalized}'")
    
    print()
    print("KEY INSIGHT:")
    print("  • ALL spacing variations are removed")
    print("  • Only the actual letters (spelling) matter")
    print("  • 'Rajiv Kannan' = 'Rajivkannan' after normalization")
    print("  • 'Baby Anitha' = 'BabyAnitha' after normalization")
    
    return all_passed


if __name__ == "__main__":
    success = test_screenshot_duplicates()
    exit(0 if success else 1)
