from enum import Enum
import re

class RoundingMethod(Enum):
	TRUNCATE = "truncate"
	ROUND_DOWN = "round down"
	ROUND_UP = "round up"
	RTN_TE = "round to nearest (ties to even)"

# Description: Truncate Rounding Method
def truncate_val(x: str, sig_places: int):
    count = 0
    rounded = ''
    
    if x.startswith('-'):
        rounded += '-'
        x = x[1:]
    
    for digit in x:
        if count != sig_places:
            if digit != '.':
                rounded += digit
                count += 1
            else:
                rounded += digit           
    return rounded

# Description: Round-up Rounding Method
def roundup_val(x: str, sig_places: int):
    is_negative = x.startswith('-')

    if not is_negative:
        rounded_value = truncate_val(x, sig_places) 
        c = str(int(rounded_value[-1]) + 1)  
        rounded_value = rounded_value[:-1] + c 
    else:
        rounded_value = truncate_val(x, sig_places)

    return rounded_value.ljust(len(str(x)), '0')

# Description: Round-down Rounding Method
def rounddown_val(x: str, sig_places: int):
    is_negative = x.startswith('-')

    if is_negative:
        rounded_value = truncate_val(x, sig_places) 
        c = str(int(rounded_value[-1]) + 1)  
        rounded_value = rounded_value[:-1] + c 
    else:
        rounded_value = truncate_val(x, sig_places)

    return rounded_value.ljust(len(str(x)), '0')

# Description: Round to nearest, ties to even Rounding Method
def tiestoeven_val(x: str, sig_places: int):
    orig_len = len(x)

    truncated = truncate_val(x, sig_places)
    length = len(truncated)
    next_digit = int(x[length])
    
    if next_digit < 5:
        x = rounddown_val(x, sig_places)
    elif next_digit > 5:
        x = roundup_val(x, sig_places)    
    else:
        last = truncated[-1]
        x = truncated
        if int(last) % 2 == 0:
            c = str(int(x[-1]) + 1)  
            x = x[:-1] + c     
    return x.ljust(len(str(orig_len)), '0')

def is_valid_rounding_method(option: str) -> bool:
    return option in RoundingMethod.__members__.values()

def round_value(value: float, rounding_method: RoundingMethod):
    count = len(re.sub('[^0-9]', '', str(value)))

    if count >= 7:
        if rounding_method == RoundingMethod.TRUNCATE:
            rounded = truncate_val(str(value), 7)
            return rounded
        elif rounding_method == RoundingMethod.ROUND_UP:
            rounded = roundup_val(str(value), 7)
            return rounded
        elif rounding_method == RoundingMethod.ROUND_DOWN:
            rounded = rounddown_val(str(value), 7)
            return rounded
        elif rounding_method == RoundingMethod.RTN_TE:            
            rounded = tiestoeven_val(str(value), 7)
            return rounded
        
    return value

def normalize(significand: str, exponent: int) -> tuple:
	# return normalized significand and adjusted exponent, assumes significand was already rounded

    count_digits = len(re.sub('[^0-9]', '', significand))
 
    if '.' in significand: # ex. 123456.700 x 10^0 -> 123456700 x 10^-3
        integer_part, decimal_part = significand.split('.')

        significand = integer_part + decimal_part
        exponent -= len(decimal_part)

    if count_digits > 7: # ex. 123456700 x 10^-3 -> 1234567 x 10^-1
        sign_offset = int(significand.startswith('-'))

        truncated_digits = significand[7+sign_offset:]
        exponent += len(truncated_digits)

        significand = significand[:7+sign_offset]
    
    sign_offset = int(significand.startswith('-'))

    if significand.startswith('-'):
        significand = "-" + significand[1:].rjust(7, "0")
    else:
        significand = significand.rjust(7, "0")
                    
    return significand, exponent