import math
import time
import numpy as np
import json
#import matplotlib.pyplot as plt

DISTANCES = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150]
VOLTAGE_ARR = [2.6741967893100833, 2.428041609172852, 1.9243283122086527, 1.4918021619720478, 1.2048414979264128, 1.0117047802970858, 0.8767229852398923, 0.7615506187835538, 0.6963615788412932, 0.6198862137946517, 0.5605793766594694, 0.501670112704973, 0.46244888330766115, 0.42007979831505504, 0.38054010813492134]

def volt_to_cm(voltage:float):
    return -0.04 * voltage**6 + -10.46 * voltage**5 + 93.50 * voltage**4 + -335.54 * voltage**3 + 620.18 * voltage**2 + -619.52 * voltage**1 + 312.62 * voltage**0
def print_out_python_formatted_poly(coefficients:np.ndarray):
    equation_string = ""
    for i in range(len(coefficients)):
        equation_string += f"{coefficients[i]:.2f} * voltage**{len(coefficients)-i-1} + "
    print(equation_string)

def generate_coefficients_equation(degree:int) -> np.ndarray:
    coefficients =  np.polyfit(VOLTAGE_ARR,DISTANCES,degree)
    return coefficients

def volt_to_cm_poly(voltage:float,coefficients:np.ndarray):
    cm = 0
    for i in range(len(coefficients)):
        cm += coefficients[i] * voltage**(len(coefficients)-i-1)
    return cm

def main():
    coefficients = generate_coefficients_equation(6)
    print_out_python_formatted_poly(coefficients)
    print(volt_to_cm(2.3))
    print(volt_to_cm_poly(2.3, coefficients)) 


if __name__ == "__main__":
    main()