def convert_bin(significand: int, exponent: int) -> str:
    # TODO: implement convert to binary rep algo.
	return "0" * 32

def format_bin(bin: str) -> str:
	# Add spaces between sections in a condensed binary result
	return bin[0] + " " + bin[1:6] + " " + bin[6:12] + " " + bin[12:]