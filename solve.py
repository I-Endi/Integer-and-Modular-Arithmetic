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
from asyncio.windows_events import NULL
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
            answer = integer_addition(exercise["x"], exercise["y"] , exercise["radix"] )
            answer = {"answer" : answer}
        elif exercise["operation"] == "subtraction":
            # Solve integer arithmetic subtraction exercise
            answer = integer_subtraction(exercise["x"], exercise["y"], exercise["radix"] )
            answer = {"answer" : answer}            
        elif exercise["operation"] == "multiplication_primary":
            # Solve integer arithmetic primary school multiplication exercise
            answer = integer_primary_multiplication(exercise["x"], exercise["y"] , exercise["radix"] )
            answer = {"answer" : answer}
        elif exercise["operation"] == "multiplication_karatsuba":
            # Solve integer arithmetic karatsuba multiplication exercise
            answer = integer_karatsuba(exercise["x"], exercise["y"], exercise["radix"] )
            answer = {"answer" : answer}
        elif exercise["operation"] == "extended_euclidean_algorithm" :
            # Solve integer arithmetic extended euclidian algorithm exercise
            a, b, gcd = integer_euclidian(exercise["x"], exercise["y"], exercise["radix"] )
            answer = {"answer-a" : a, "answer-b" : b, "answer-gcd" : gcd}
    else: # exercise["type"] == "modular_arithmetic"
        # Check what operation within the modular arithmetic operations we need to solve
        if exercise["operation"] == "reduction":
            # Solve modular arithmetic reduction exercise
            answer = modular_reduction(exercise["x"], exercise["modulus"] , exercise["radix"] )
            answer = {"answer" : answer}
        elif exercise["operation"] == "addition":
            # Solve modular arithmetic addition exercise
            answer = modular_addition(exercise["x"], exercise["y"], exercise["modulus"], exercise["radix"] )
            answer = {"answer" : answer}
        elif exercise["operation"] == "subtraction":
            # Solve modular arithmetic subtraction exercise
            answer = modular_subtraction(exercise["x"], exercise["y"], exercise["modulus"], exercise["radix"] )
            answer = {"answer" : answer}
        elif exercise["operation"] == "multiplication":
            # Solve modular arithmetic multiplication exercise
            answer = modular_multiplication(exercise["x"], exercise["y"], exercise["modulus"], exercise["radix"] )
            answer = {"answer" : answer}
        elif exercise["operation"] == "inversion":
            # Solve modular arithmetic inversion exercise
            answer = modular_inversion(exercise["x"], exercise["modulus"], exercise["radix"] )
            answer = {"answer" : answer}

    # Open file at answer_location for writing, creating the file if it does not exist yet
    # (and overwriting it if it does already exist).
    with open(answer_location, "w") as answer_file:
        # Serialize Python answer data (stored in answer) to JSON answer data and write it to answer_file
        json.dump(answer, answer_file, indent=4)
    
### Integer Arithmetic ###

def integer_addition(x: string, y: string, radix: int):

    sign = ""
    x, y, negativeX, negativeY = signCheck(x, y)
    
    if negativeX and negativeY:
        sign = "-"
    elif negativeX:
        return integer_subtraction(y, x, radix)
    elif negativeY:
        return integer_subtraction(x, y, radix)

    x, y = addZero(x, y)

    carry = False
    digit = 0
    result = ""
    for i in reversed(range(len(x))):
        digit = extended_int(x[i]) + extended_int(y[i]) + carry
        if digit >= radix:
            carry = True
        else:
            carry = False
        digit = digit % radix
        result = digit_to_str(digit) + result

    result = sign + removeZero(str(int(carry)) + result)
    return result

def integer_subtraction(x: string, y: string, radix: int):

    x, y, negativeX, negativeY = signCheck(x, y)
    
    if negativeX and negativeY:
        return integer_subtraction(y, x, radix)
    elif negativeX:
        return integer_addition("-" + x, "-" +  y, radix)
    elif negativeY:
        return integer_addition(x, y, radix)

    x, y = addZero(x, y)

    if not(geq(x, y)):
        return "-" + integer_subtraction(y, x, radix)

    carry = False
    digit = 0
    result = ""
    for i in reversed(range(len(x))):
        digit = extended_int(x[i]) - extended_int(y[i]) - carry
        if digit < 0:
            carry = True
            digit = digit + radix
        else:
            carry = False
        result = digit_to_str(digit) + result

    result = removeZero(result)
    return result

def integer_primary_multiplication(x: string, y: string ,radix: int):
    
    x, y , negativeX, negativeY = signCheck(x, y)
    result = "0"

    if geq(y, x):
        x, y = y, x
    
    for i in reversed(range(len(y))):
        temp = "0"
        for j in reversed(range(len(x))):
            temp = integer_addition(temp, convert_to_radix(str(extended_int(y[i]) * extended_int(x[j])), radix) + "0"*(i + j), radix)
        result = integer_addition(result, str(temp), radix)
    
    if negativeX ^ negativeY:
        result = "-" + result
    return result


def integer_karatsuba(x: string, y: string, radix: int):
    if len(x) <= 2 or len(y) <= 2:
        return integer_primary_multiplication(x, y, radix)

    if len(x) != len(y):
        addZero(x, y)
    x1, x2 = split_string(x)
    y1, y2 = split_string(y)
    result1 = integer_primary_multiplication(x1,y1,radix)
    result3 = integer_primary_multiplication(x2,x2,radix)
    sumx = integer_addition(x1,x2,radix)
    sumy = integer_addition(y1,y2,radix)
    multsum = integer_primary_multiplication(sumx,sumy,radix)
    diff1 = integer_subtraction(multsum,result1,radix)
    result2 = integer_subtraction(diff1,result3,radix)
    return result1+result2+result3

def integer_euclidian(x: string, y: string, radix: int):
    switch = False
    if x =="0":
        return x, "1", y
    elif y == "0":
        return "1", y, x
    elif geq(x, y):
        a, b = x, y
    else:
        a, b = y, x
        switch = True

    s_old = "1"
    s_new = "0"
    t_old = "0"
    t_new = "1" 
    #r = 1 #doesn't really matter as long as it is not 0
    while b != 0:
        q, r = division(a, b, radix)
        mult = integer_primary_multiplication(q,s_new,radix)
        s_new, s_old = integer_subtraction(s_old,integer_primary_multiplication(q,s_new,radix),radix), s_new
        t_new, t_old = integer_subtraction(t_old,integer_primary_multiplication(q,t_new,radix),radix), t_new
        a = b
        b = r 

    if switch:
        return t_old, s_old, a
    else:
        return s_old, t_old, a

    

### Modular Arithmetic ###

def modular_reduction(x: string, mod: string, radix: int):

    if geq("0", mod):
        return "undefined"
    
    x, negativeX = singleSignCheck(x)

    while geq(x, mod):
        x = integer_subtraction(x, mod + "0"*(len(x) - len(mod) - 1), radix)    

    if negativeX:
        x =  integer_subtraction(mod, x, radix)
    
    return x


    
def modular_addition(x: string, y: string, mod: string, radix: int):

    sum = integer_addition(x, y, radix)
    result = modular_reduction(sum, mod, radix)
    return result
    

def modular_subtraction(x: string, y: string, mod: string, radix: int):

    diff = integer_subtraction(x, y, radix)
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
        b = integer_subtraction(b, "1", radix)
    return None

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

    if len(x) > len(y):
        return True

    elif len(y) > len(x):
        return False

    else:
        for i in range(len(x)):
            if extended_int(x[i]) > extended_int(y[i]):
                return True
            elif extended_int(x[i]) < extended_int(y[i]): 
                return False
        return True

def signCheck(x: string, y: string):
    
    negativeX = False
    negativeY = False
    if x[0] == "-":
        negativeX = True
        x = x[1:]
    if y[0] == "-":
        negativeY = True
        y = y[1:]
    return x, y, negativeX, negativeY

def singleSignCheck(x: string):
    
    negativeX = False
    if x[0] == "-":
        negativeX = True
        x = x[1:]
    return x, negativeX

def addZero(x: string, y: string):
    
    length_diff = len(x) - len(y)
    if length_diff > 0:
        y = ( "0" * length_diff ) + y
    elif length_diff < 0:
        x = ( "0" * abs(length_diff) ) + x
    return x, y

def removeZero(x: string):
    
    while x[0] == "0" and len(x) > 1:
        x = x[1:]
    return x

def split_string(x: string):
    n = len(x)//2
    return x[:n], x[n:] 

def extended_int(x: string):
    
    if len(x) > 1:
        return extended_int(x[:len(x)//2]) + extended_int(x[len(x)//2:])
    else:
        match x:
            case "A":
                return 10
            case "B":
                return 11
            case "C":
                return 12
            case "D":
                return 13
            case "E":
                return 14
            case "F":
                return 15
            case _:
                return int(x)

def digit_to_str(x: int):
    
    match x:
        case 10:
            return "A"
        case 11:
            return "B"
        case 12:
            return "C"
        case 13:
            return "D"
        case 14:
            return "E"
        case 15:
            return "F"
        case _:
            return str(x)
    
def convert_to_radix(x: string, radix: int):
    
    if not(geq(x, str(radix))):
        return x

    i = 1
    q, r = division(x, str(radix**i), 10)
    while geq(q, str(radix)):
        i += 1
        q, r = division(x, str(radix**i), 10)
    return q + convert_to_radix(r, radix)

def division(x: string, y: string, radix: int):

    x, y, negativeX, negativeY = signCheck(x,y)
    q = "0"

    if geq(y,x):
        return

    while geq(x, y):
        x = integer_subtraction(x, y + "0"*(len(x) - len(y) - 1), radix)  
        q = integer_addition(q, "1"+"0"*(len(x) - len(y) - 1), radix)    

    if negativeX ^ negativeY: #xor function
        q = "-" + q
        if negativeX:
            x = "-" + x
        
    return q, x



for i in range(0,14):
    print(i)
    solve_exercise("Simple\Exercises\exercise" + str(i) + ".json", "Simple\Calculated\ answer" + str(i) + ".json")

for i in range(0,14):
    print(i)
    solve_exercise("Realistic\Exercises\exercise" + str(i) + ".json", "Realistic\Calculated\ answer" + str(i) + ".json")