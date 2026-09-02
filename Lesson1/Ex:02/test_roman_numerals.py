import roman_numerals as roman_numerals


# Test single letters
def test_single_letters():
    assert roman_numerals.roman_to_decimal("I") == 1
    assert roman_numerals.roman_to_decimal("V") == 5
    assert roman_numerals.roman_to_decimal("X") == 10
    assert roman_numerals.roman_to_decimal("L") == 50
    assert roman_numerals.roman_to_decimal("C") == 100
    assert roman_numerals.roman_to_decimal("D") == 500
    assert roman_numerals.roman_to_decimal("M") == 1000
    print("Single letters: PASS")


# Test adding letters together (additive)
def test_adding_numbers():
    assert roman_numerals.roman_to_decimal("II") == 2
    assert roman_numerals.roman_to_decimal("III") == 3
    assert roman_numerals.roman_to_decimal("VI") == 6
    assert roman_numerals.roman_to_decimal("XX") == 20
    print("Adding numbers: PASS")


# Test subtractive (smaller before larger means subtract)
def test_subtracting_numbers():
    assert roman_numerals.roman_to_decimal("IV") == 4     # 5 - 1
    assert roman_numerals.roman_to_decimal("IX") == 9     # 10 - 1
    assert roman_numerals.roman_to_decimal("XL") == 40    # 50 - 10
    assert roman_numerals.roman_to_decimal("XC") == 90    # 100 - 10
    print("Subtracting numbers: PASS")


# Test complex numbers
def test_complex_numbers():
    assert roman_numerals.roman_to_decimal("XCIV") == 94          # (100-10) + (5-1)
    assert roman_numerals.roman_to_decimal("MDCCCLXVII") == 1867  # 1000+500+300+50+10+5+2
    assert roman_numerals.roman_to_decimal("MMMCMXCIX") == 3999   # Largest: 3000+900+90+9
    print("Complex numbers: PASS")


if __name__ == "__main__":
    test_single_letters()
    test_adding_numbers()
    test_subtracting_numbers()
    test_complex_numbers()
    print("\nAll tests passed!")
