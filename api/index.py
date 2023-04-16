from flask import Flask, request
from api._rounding import round, normalize, is_valid_rounding_method
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

    significand = args.get('significand', default="NaN", type=float)
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

    param_significand = args.get('significand', default=0, type=float)
    param_exponent = args.get('exponent', default=0, type=int)
    rounding_method = args.get('rounding_method', default='truncate', type=str)
    
    rounded_significand = round(param_significand, rounding_method)
    significand, exponent = normalize(rounded_significand, param_exponent, rounding_method)

    return {
        'significand': significand, 
        'exponent': exponent
    }
