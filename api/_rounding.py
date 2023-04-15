from enum import Enum

class RoundingMethod(Enum):
	TRUNCATE = "truncate"
	ROUND_DOWN = "round down"
	ROUND_UP = "round up"
	RTN_TE = "round to nearest (ties to even)"

def is_valid_rounding_method(option: str) -> bool:
    return option in RoundingMethod.__members__.values()

def round(value: int, rounding_method: RoundingMethod) -> int:
    # TODO: implement rounding
	return 0

def normalize(significand: int, exponent: int, rounding_method: RoundingMethod) -> tuple:
	# TODO: return normalized and rounded value
	# return normalized significand and adjusted exponent
	return significand, exponent