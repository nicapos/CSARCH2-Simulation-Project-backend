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
    abcde = []
    if case == 1:
        abcde.append(ep[0])
        abcde.append(ep[1])
        abcde.append(msb_bin[1])
        abcde.append(msb_bin[2])
        abcde.append(msb_bin[3])
        return abcde
    if case == 2:
        abcde.append(1)
        abcde.append(1)
        abcde.append(ep[0])
        abcde.append(ep[1])
        abcde.append(msb_bin[3])
        return abcde
    error("This is a special case.")    

# Description: check DPBCD case
def dpbcdCase(aei_list, binary):
    aei_str = ''.join(aei_list)
    output = []
    binary_list = list(binary)

    output.insert(2, binary_list[3])
    output.insert(5, binary_list[7])
    output.insert(9, binary_list[11])

    if aei_str != "000":
        output.insert(6, '1')
    else:
        output.insert(6, '0')    

    if aei_str == "000":
        # pq == bc
        output.insert(0, binary_list[1])
        output.insert(1, binary_list[2])
        # st == fg
        output.insert(3, binary_list[5])
        output.insert(4, binary_list[6])
        # wx == jk
        output.insert(7, binary_list[9])
        output.insert(8, binary_list[10])
    if aei_str == "001":
        # pq == bc
        output.insert(0, binary_list[1])
        output.insert(1, binary_list[2])
        # st == fg
        output.insert(3, binary_list[5])
        output.insert(4, binary_list[6])
        # wx == 00
        output.insert(7, '0')
        output.insert(8, '0')
    if aei_str == "010":
        # pq == bc
        output.insert(0, binary_list[1])
        output.insert(1, binary_list[2])
        # st == jk
        output.insert(3, binary_list[9])
        output.insert(4, binary_list[10])
        # wx == 01
        output.insert(7, '0')
        output.insert(8, '1')
    if aei_str == "011":
        # pq == bc
        output.insert(0, binary_list[1])
        output.insert(1, binary_list[2])
        # st == 10
        output.insert(3, '1')
        output.insert(4, '0')
        # wx == 11
        output.insert(7, '1')
        output.insert(8, '1')          
    if aei_str == "100":
        # pq == jk
        output.insert(0, binary_list[9])
        output.insert(1, binary_list[10])
        # st == fg
        output.insert(3, binary_list[5])
        output.insert(4, binary_list[6])
        # wx == 10
        output.insert(7, '1')
        output.insert(8, '0')    
    if aei_str == "101":
        # pq == fg
        output.insert(0, binary_list[5])
        output.insert(1, binary_list[6])
        # st == 01
        output.insert(3, '0')
        output.insert(4, '1')
        # wx == 11
        output.insert(7, '1')
        output.insert(8, '1')
    if aei_str == "110":
        # pq == jk
        output.insert(0, binary_list[9])
        output.insert(1, binary_list[10])
        # st == 00
        output.insert(3, '0')
        output.insert(4, '0')
        # wx == 11
        output.insert(7, '1')
        output.insert(8, '1')   
    if aei_str == "111":
        # pq == bc
        output.insert(0, '0')
        output.insert(1, '0')
        # st == fg
        output.insert(3, '1')
        output.insert(4, '1')
        # wx == jk
        output.insert(7, '1')
        output.insert(8, '1')  
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
    x = val.find("8")
    y = val.find("9")
    
    if x == -1 and y == -1:
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
        binary_substrings = []

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
        dpbcd = ''
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
def toHex(bin_string):
    chunks = []
    count = 0
    
    fours = ''
    for x in bin_string:
        fours += x
        if count == 3:
            chunks.append(fours)
            count -= 4
            fours = ''
        count += 1
    
    hex_string = ''
    for item in chunks:
        hex_digit = hex(int(item, 2))[2:].upper() 
        hex_string += hex_digit
    
    return hex_string

def convert_bin(significand: float, exponent: int) -> str:
    # TODO: implement convert to binary rep algo.
    output = ''
    val = str(significand)
    count = len(re.sub('[^0-9]', '', val))
    exp = exponent

# (A) Process
	# (1) Process MSD
    first_digit, msb_bin = processMSD(val)
    ep = processE_prime(exp)
	# (2) Process Combination Field
    case = check_combiCase(first_digit)
    combi = process_combiField(case, ep, msb_bin)
    # (3) Process Exponent Continuation
    ep = ep[2:]
    # (4) Process Coefficient Continuation
    coeff = processcoefficient_cont(val)
    
 # (B) Put in output
	# (1) Add Sign Bit
    if val.startswith('-'):
        output = output + '1'
    else:
        output = output + '0'
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