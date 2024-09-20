import math
import time
import numpy as np
import json
from src.utils.math_utils import generate_coefficients_equation,print_out_python_formatted_poly,volt_to_cm_poly

DISTANCES = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
VOLTAGE_ARR = [2.6741967893100833, 2.428041609172852, 1.9243283122086527, 1.4918021619720478, 1.2048414979264128, 1.0117047802970858, 0.8767229852398923, 0.7615506187835538, 0.6963615788412932, 0.6198862137946517, 0.5605793766594694, 0.501670112704973, 0.46244888330766115, 0.42007979831505504, 0.38054010813492134]

def main():
    coefficients = generate_coefficients_equation(4,DISTANCES,VOLTAGE_ARR)
    print(coefficients)
    print_out_python_formatted_poly(coefficients)

    print(volt_to_cm_poly(2.3, coefficients)) 


if __name__ == "__main__":
    main()