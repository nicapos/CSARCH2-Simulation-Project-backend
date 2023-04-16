from flask import Flask, request
from api._rounding import round_value, normalize, is_valid_rounding_method
from api._convert import convert_bin, format_bin
import re

import json

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/convert')
def converter():
    args = request.args

    significand = args.get('significand', default="NaN", type=str)
    exponent = args.get('exponent', default=0, type=int)

    if significand == "NaN":
        repr_binary = "01111100000000000000000000000000"
        repr_hex = hex(int(repr_binary, 2))[2:]
        repr_binary = format_bin(repr_binary)
    else:
        repr_binary = convert_bin(significand, exponent)
        repr_hex = hex(int(repr_binary, 2))[2:]
        repr_binary = format_bin(repr_binary)

    return {
        'binary': repr_binary,
        'hex': repr_hex
    }

@app.route('/api/normalize')
def round():
    args = request.args

    param_significand = args.get('significand', default="NaN", type=str)
    param_exponent = args.get('exponent', default=0, type=int)
    rounding_method = args.get('rounding_method', default='truncate', type=str)

    if param_significand == "NaN":
        return {
            'significand': "NaN", 
            'exponent': "NaN"
        }
    
    rounded_significand = round_value(param_significand, rounding_method)
    significand, exponent = normalize(rounded_significand, param_exponent)

    return {
        'significand': significand, 
        'exponent': exponent
    }
