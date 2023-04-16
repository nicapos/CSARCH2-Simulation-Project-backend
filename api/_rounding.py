from enum import Enum
import re

class RoundingMethod(Enum):
	TRUNCATE = "truncate"
	ROUND_DOWN = "round down"
	ROUND_UP = "round up"
	RTN_TE = "round to nearest (ties to even)"

# Description: Truncate Rounding Method
def truncate_val(x, y):
    sig_places = y
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
def roundup_val(x, y):
    isneg = False
    if x.startswith('-'):
        isneg = True
    if not isneg:
        x = truncate_val(x, y) 
        c = str(int(x[-1]) + 1)  
        x = x[:-1] + c 
    else:
        x = truncate_val(x, y)
    return x    

# Description: Round-down Rounding Method
def rounddown_val(x, y):
    isneg = False
    
    if x.startswith('-'):
        isneg = True
        
    print(isneg)    
    if isneg:
        x = truncate_val(x, y) 
        c = str(int(x[-1]) + 1)  
        x = x[:-1] + c 
    else:
        x = truncate_val(x, y)
    return x

# Description: Round to nearest, ties to even Rounding Method
def checkifeven(num):
    num = int(num)
    if num % 2 == 0:
        return True
    return False

# Description: Round to nearest, ties to even Rounding Method
def tiestoeven_val(x, y):
    truncated = truncate_val(x, y)
    length = len(truncated)
    next_digit = int(x[length])
    
    if next_digit < 5:
        x = rounddown_val(x, y)
    elif next_digit > 5:
        x = roundup_val(x, y)    
    else:
        last = truncated[-1]
        x = truncated
        if not checkifeven(last):
            c = str(int(x[-1]) + 1)  
            x = x[:-1] + c     
    return x

def modify_string(val, decimal_index, count):
    # check if the values after decimal are all zeroes
    checkzeros = bool(re.search(r'\.\d*[1-9]', val))
    if not checkzeros: # if all zeroes remove them
        val = val.replace(".", "")
        val = val.rstrip("0")

    if val[-1] == '0':
            val = val.rstrip("0") if "." in val else val

    if count == 7: # ex: 123.4567 = 1234567.
        return val + "."
    elif count < 7: # ex: 123.45 = 0012345. or 0.123 = 0000123.
        # check if it's negative
        if val.startswith('-'):
            val = val.lstrip("-")
            val = val.replace(".", "").rjust(7, "0")
            return "-" + val + "."
        # put decimal at the end and append a zero at the front until digits reaches 7
        val = val.rjust(7, "0")
        return val 
    elif count > 7: # ex: 12345678.90 = 1234567.890
        isneg = False
        if val.startswith('-'):
            isneg = True
            val = val.lstrip("-") 
        
        if val[-1] == '0':
            val = val.rstrip("0") if "." in val else val
        
        whole_num_count = decimal_index if decimal_index != -1 else len(val)
        if whole_num_count > 7:
            num_zeros = whole_num_count - 7
            val = val.replace('.', '')
            val = val.ljust(num_zeros + whole_num_count)
            val = val[:decimal_index - num_zeros] + '.' + val[decimal_index - num_zeros:]
        elif whole_num_count < 7:
            num_zeros = 7 - whole_num_count
            val = val.replace('.', '')
            val = val.rjust(num_zeros + whole_num_count)
            val = val[:decimal_index + num_zeros] + '.' + val[decimal_index + num_zeros:]

        if isneg: 
            return '-'+val

def is_valid_rounding_method(option: str) -> bool:
    return option in RoundingMethod.__members__.values()

def round(value: float, rounding_method: RoundingMethod) -> float:
    val = str(value)
    count = len(re.sub('[^0-9]', '', val))
    if count >= 7:
        if rounding_method == RoundingMethod.TRUNCATE:
            rounded = truncate_val(str(value), 7)
            return float(rounded)
        elif rounding_method == RoundingMethod.ROUND_UP:
            rounded = roundup_val(str(value), 7)
            return float(rounded)
        elif rounding_method == RoundingMethod.ROUND_DOWN:
            rounded = rounddown_val(str(value), 7)
            return float(rounded)
        elif rounding_method == RoundingMethod.RTN_TE:            
            rounded = tiestoeven_val(str(value), 7)
            return float(rounded)
    return value

def normalize(significand: float, exponent: int, rounding_method: RoundingMethod) -> tuple:
	# return normalized significand and adjusted exponent

	val = str(significand)
	count = len(re.sub('[^0-9]', '', val))
	has_dot = '.' in val
 
	if has_dot:
		digit_count = len(val.lstrip("-").split(".")[0])
		decimal_index = val.index('.')
		# check the number of digits before the decimal point
		if digit_count != 7: # ex: 123.45 = 0012345 and 123456789.890 = 1234567.89890
			val = modify_string(val, decimal_index, count)
                        
		new_decimal_index = val.index('.')
		exponent += decimal_index - new_decimal_index
	else:
		if count < 7: # ex: 123 = 0000123
			# append zeroes at the front until the number of digits in the number string is equal to 7
			val = val.rjust(7, "0")
		if count > 7: # ex: 123456789 = 1234567.89 
			# place a decimal point after the 7th digit
			val = val[:7] + "." + val[7:]
   
	# val has the updated string
	significand = float(val)
 
	return significand, exponent