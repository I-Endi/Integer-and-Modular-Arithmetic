##
# 2WF90 Algebra for Security -- Software Assignment 1 
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number:
# group_number 
#
# Author names and student IDs:
# Endi Isuf (1542591) 
# Dea Llazo (1589857)
# Ilesh Yadav (1540025)
# Luca (author_student_ID_4)
##

# Import built-in json library for handling input/output 
import json
import string



def solve_exercise(exercise_location : str, answer_location : str):
    """
    solves an exercise specified in the file located at exercise_location and
    writes the answer to a file at answer_location. Note: the file at
    answer_location might not exist yet and, hence, might still need to be created.
    """
    
    # Open file at exercise_location for reading.
    with open(exercise_location, "r") as exercise_file:
        # Deserialize JSON exercise data present in exercise_file to corresponding Python exercise data 
        exercise = json.load(exercise_file)
        

    ### Parse and solve ###

    # Check type of exercise
    if exercise["type"] == "integer_arithmetic":
        # Check what operation within the integer arithmetic operations we need to solve
        if exercise["operation"] == "addition":
            # Solve integer arithmetic addition exercise
            pass
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            pass
        elif exercise["operation"] == "multiplication_primary":
            # Solve integer arithmetic primary school multiplication exercise
            pass
        elif exercise["operation"] == "multiplication_karatsuba":
            # Solve integer arithmetic karatsuba multiplication exercise
            pass
        elif exercise["operation"] == "extended_euclidean_algorithm" :
            # Solve integer arithmetic extended euclidian algorithm exercise
            pass
    else: # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        if exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            pass
        elif exercise["operation"] == "addition":
            # Solve modular arithmetic addition exercise
            pass
        elif exercise["operation"] == "subtraction":
            # Solve modular arithmetic subtraction exercise
            pass
        elif exercise["operation"] == "multiplication":
            # Solve modular arithmetic multiplication exercise
            pass
        elif exercise["operation"] == "inversion":
            # Solve modular arithmetic inversion exercise
            pass
        




    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)
    

def convert(x: string):
    pass

def integer_addition(x: string, y: string, radix: int):
    pass

def integer_subtraction(x: string, y: string, radix: int):
    pass

def integer_primary_multiplication(x: string, y: string ,radix: int):
    pass

def integer_karatsuba(x: string, y: string, radix: int):
    pass

def integer_euclidian(x: string, y: string, radix: int):
    pass

def modular_reduction(x: string, mod: string, radix: int):
    pass

def modular_addition(x: string, y: string, mod: string, radix: int):
    sum = integer_addition(x,y,radix)
    result = modular_reduction(sum, mod, radix)
    return result
    

def modular_subtraction(x: string, y: string, mod: string, radix: int):
    diff = integer_subtraction(x,y, radix)
    result = modular_reduction(diff, mod, radix)
    return result
    
def modular_multiplication(x: string, y: string, mod: string, radix: int):
    mult = integer_karatsuba(x, y, radix)
    result = modular_reduction(mult, mod, radix)
    return result

def modular_inversion(x: string, mod: string, radix: int):
    b = integer_subtraction(mod, "1", radix)
    while b != "-1":
        mult_mod = modular_multiplication(x, b, mod, radix)
        if mult_mod == "1":
            return b
