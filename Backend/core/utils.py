import math

def calculate_emi(principal, rate, tenure):
    r = rate / (12 * 100)
    emi = (principal * r * ((1 + r) ** tenure)) / (((1 + r) ** tenure) - 1)
    return round(emi, 2)

