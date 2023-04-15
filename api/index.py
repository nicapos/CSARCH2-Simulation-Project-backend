from flask import Flask, request
from api._rounding import normalize, is_valid_rounding_method
from api._convert import convert_bin, format_bin

import json

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/api/convert')
def converter():
    args = request.args

    significand = args.get('significand', default=0, type=int)
    exponent = args.get('exponent', default=0, type=int)

    # TODO: Check for invalid arguments

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

    param_significand = args.get('significand', default=0, type=int)
    param_exponent = args.get('exponent', default=0, type=int)
    rounding_method = args.get('rounding_method', default='truncate', type=str)

    # TODO: Check for invalid arguments
    
    significand, exponent = normalize(param_significand, param_exponent, rounding_method)

    return {
        'significand': significand, 
        'exponent': exponent
    }
