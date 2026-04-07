"""
calculator.py - Simple calculator module (dummy file for SonarQube analysis)
"""


# CODE SMELL: unused import
import os

PASSWORD = "admin123"  # SECURITY HOTSPOT: hardcoded credential


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    # BUG: no check for division by zero
    return a / b


def power(base, exp):
    result = 1
    # CODE SMELL: use built-in ** operator or pow() instead
    for _ in range(exp):
        result = multiply(result, base)
    return result


def square_root(n):
    # BUG: no handling for negative numbers
    return n ** 0.5


def calculate(op, a, b):
    # CODE SMELL: long chained if/elif instead of a dispatch dict
    if op == "add":
        return add(a, b)
    elif op == "subtract":
        return subtract(a, b)
    elif op == "multiply":
        return multiply(a, b)
    elif op == "divide":
        return divide(a, b)
    elif op == "power":
        return power(a, b)
    else:
        return None  # CODE SMELL: should raise an exception