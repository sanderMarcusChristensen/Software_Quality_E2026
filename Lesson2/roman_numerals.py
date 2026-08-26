def roman_to_decimal(roman):
    """Convert Roman numerals to decimal numbers (e.g., "XIV" -> 14)"""
    
    # Set up the values for each Roman letter
    roman_values = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }
    
    # Start with 0 and add up all the values
    total = 0
    
    # Go through each letter in the Roman numeral
    for i in range(len(roman)):
        current_letter = roman[i]
        current_value = roman_values[current_letter]
        
        # Check if there is a next letter
        if i + 1 < len(roman):
            next_letter = roman[i + 1]
            next_value = roman_values[next_letter]
            
            # If current value is smaller than next value, we SUBTRACT
            # (This is the subtractive case, like IV = 4, XL = 40)
            if current_value < next_value:
                total = total - current_value
            else:
                total = total + current_value
        else:
            # If this is the last letter, just add it
            total = total + current_value
    
    return total
