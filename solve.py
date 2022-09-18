##
# 2WF90 Algebra for Security -- Software Assignment 1 
# Integer and Modular Arithmetic
# solve.py
#
#
# Group number: 34
# group_number 
#
# Author names and student IDs:
# Endi Isuf (1542591) 
# Dea Llazo (1589857)
# Ilesh Yadav (1540025)
# Luca Pistone (1263765)
##

# Import built-in json library for handling input/output 
import json
from re import M, X
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

### Integer Arithmetic ###

def integer_addition(x: string, y: string):
    pass

def integer_subtraction(x: string, y: string, radix: int):
    pass

def integer_primary_multiplication(x: string, y: string ,radix: int):
    pass

def integer_karatsuba(x: string, y: string, radix: int):
    pass

def integer_euclidian(x: string, y: string, radix: int):
    pass

### Modular Arithmetic ###

def modular_reduction(x: string, mod: string, radix: int):
    
    if x[0] == "-":
        negativeX = True
        x = x[1:]

    while geq(x, mod):
        x = integer_subtraction(absolute(x), mod + "0"*(x.length - mod.length))    
        x = absolute(x)    

    if negativeX:
        x =  integer_subtraction(mod, x)
    
    return x


    
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
    pass


### Helping Functions ###

def absolute(x: string):
    
    if x[0] == "-":
        return x[1:]
    return x

def geq(x: string, y: string):
    
    if x[0] == "-":
        if y[0] == "-":
            return geq_absolute(y, x)

        else:
            return False

    else:
        if y[0] == "-":
            return True   
            
        else:
            return geq_absolute(x, y)

def geq_absolute(x: string, y: string):

    x = absolute(x)
    y = absolute(y)

    if x.length > y.length:
        return True

    elif y.length > x.length:
        return False

    else:
        for i in x:
            if int(x.i) < int(y.i):
                return False
        return True

    