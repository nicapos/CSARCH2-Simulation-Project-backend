# IEEE-754 Decimal-32 floating-point converter API

A web-based IEEE-754 Decimal-32 floating-point converter that can convert decimal and base-10 inputs (up to 7 digits and more) into binary output with spaces between sections, hexadecimal equivalent, and with the option to output the results to a text file. 

This converter can handle all special cases, including NaN input, and provides the user with the ability to choose their preferred rounding method.

The main project can be found [here](https://github.com/nicapos/CSARCH2-Simulation-Project).

## Running Locally

1. If you haven't installed [Flask], you need to install it first. 
```bash
pip install flask
```

2. Run the development server.
```bash
python3 main.py
```

[Flask]: https://github.com/pallets/flask