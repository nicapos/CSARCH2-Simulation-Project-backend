import re
 
# Description: Get the MSD  
def processMSD(val):
    first_digit = int(re.search(r'[1-9]|0', val).group()) if re.search(r'[1-9]|0', val) else 0
    binoutput = format(first_digit, '04b')
    return first_digit, binoutput

# Description: Get E'
def processE_prime(exp):
    exp = int(exp)
    ep = exp + 101
    output = format(ep, '08b') 
    return output

# Description: Check combination case
def check_combiCase(first_digit):
    if first_digit <= 7:
        return 1
    elif first_digit == 8 or first_digit == 9:
        return 2
    return 0
 
# Description: Get combination field    
def process_combiField(case, ep, msb_bin):
    if case == 1:
        return ep[:2] + msb_bin[1:4]
    if case == 2:
        return [1, 1, ep[0], ep[1], msb_bin[3]]
    return ['1','1','1','1','0'] # TODO: Return field for special case (part of requirements) 

# Description: check DPBCD case
def dpbcdCase(aei_list, binary):
    aei_str = ''.join(aei_list)
    output = []
    bin = list(binary)

    middle_bit_map = {
        # aei: [p, q, s, t, w, x]
        "000": [bin[1],  bin[2], bin[5],  bin[6], bin[9], bin[10]], 
        "001": [bin[1],  bin[2], bin[5],  bin[6],    '0',     '0'],
        "010": [bin[1],  bin[2], bin[9], bin[10],    '0',     '1'],
        "011": [bin[1],  bin[2],    '1',     '0',    '1',     '1'],
        "100": [bin[9], bin[10], bin[5],  bin[6],    '1',     '0'],
        "101": [bin[5],  bin[6],    '0',     '1',    '1',     '1'],
        "110": [bin[9], bin[10],    '0',     '0',    '1',     '1'],
        "111": [   '0',     '0',    '1',     '1',    '1',     '1']
    }

    output = middle_bit_map[aei_str]
    
    output.insert(2, bin[3])    # insert r
    output.insert(5, bin[7])    # insert u
    output.append(bin[11])      # insert y

    v = '0' if aei_str == '000' else '1'
    output.insert(6, v)         # insert v = 6

    return output      


# Description: convert Coefficient to Densely packed BCD
def processcoefficient_cont(val):
    if val.startswith('-'):
        val = val[1:]
    
    # Remove first digit
    val = val[1:]
    length = len(val)
    count = 0

    # check if there are 8/9 digits
    if not ("8" in val or "9" in val):
        # Convert each digit to binary and concatenate
        binary_str = ''
        for digit in val:
            if count == int(length/2 - 1) or count == length - 1:
                binary_str += format(int(digit), '04b')
            else:
                binary_str += format(int(digit), '03b')
            count += 1
        return binary_str
    
    else: #convert using DPBCD
        n = 3
        substring_list = []

        for i in range(0, len(val), n):
            substring = val[i:i+n]
            substring_list.append(substring)

        bin_list = []
        for substr in substring_list:
            bin_str = ''
            for digit in substr:
                digit_bin = format(int(digit), '04b')
                bin_str += digit_bin
            bin_list.append(bin_str)    
            
        aei = []
        count = 0

        # Get aei to get case
        for item in bin_list:
            for x in item:
                if count % 4 == 0:
                    aei.append(x)
                count += 1 
        
        # Find the index of the middle element
        middle_index = len(aei) // 2

        # Split the list in half using slicing
        list1 = aei[:middle_index]
        list2 = aei[middle_index:]

        ans = dpbcdCase(list1, bin_list[0])   
        binary_str = ''.join(ans) 
        ans = dpbcdCase(list2, bin_list[1])   
        binary_str += ''.join(ans) 
        
        return binary_str               

# Description: Convert binary string to hex equivalent
def toHex(bin: str):
    return hex(int(bin, 2))[2:]

def convert_bin(significand: int, exponent: int) -> str:
    val = str(significand)

# (A) Process
	# (1) Process MSB
    first_digit, msb_bin = processMSD(val)
    # (2) Process E'
    ep = processE_prime(exponent)
    if exponent <= 90 and exponent >= -101:
        case = check_combiCase(first_digit)
    else:
        case = 0
    # (3) Process Combination Field    
    combi = process_combiField(case, ep, msb_bin)
    # (4) Process Exponent Continuation
    ep = ep[2:]        
    # (5) Process Coefficient Continuation
    coeff = processcoefficient_cont(val)
    
 # (B) Put in output
	# (1) Add Sign Bit
    output = '1' if val.startswith('-') else '0'
    # (2) Add Combination Field
    combi = ''.join([str(elem) for elem in combi])
    output = output + combi
    # (3) Add Exponent Continuation
    output = output + ep
    # (4) Add Coefficient Continuation
    output = output + coeff
    
    return output

def format_hex(bin: str) -> str:
    hex_output = toHex(bin)
    return hex_output

def format_bin(bin: str) -> str:
	# Add spaces between sections in a condensed binary result
	return bin[0] + " " + bin[1:6] + " " + bin[6:12] + " " + bin[12:]