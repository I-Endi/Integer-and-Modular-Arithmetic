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

    # Check type of exercise, call the appropriate function to solve and assign the solution to the list named 'answer'
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

def integer_addition(x: str, y: str, radix: int):
    """
    Do an integer addition on the two inputs x and y represented as strings and return the result as a string.
    Both x and y have their value in the appropriate radix specified by the input 'radix' which is an integer.
    """
    # If an input is zero return the other.
    if y == "0":
        return x
    elif x == "0":
        return y

    # Variable to be appended in the result
    sign = ""

    # Make inputs positive and remember their signs.
    x, y, negativeX, negativeY = signCheck(x, y)
    
    # Adding two negative numbers returns a negative result.
    if negativeX and negativeY:
        sign = "-"
    # If only one input is negative subtract it from the positive one.
    elif negativeX:
        return integer_subtraction(y, x, radix)
    elif negativeY:
        return integer_subtraction(x, y, radix)

    # Make the size of both the inputs identical by adding leading zeroes
    x, y = addLeadingZero(x, y)

    # Introduce carry, digit and result
    carry = False
    digit = 0
    result = ""
    # Loop through all the digits starting from the rightmost digit
    for i in reversed(range(len(x))):
        # Add the i-th digit from each number and the carry
        digit = extended_int(x[i]) + extended_int(y[i]) + carry

        # If the digit addition is bigger than the radix add a carry and make the digit radix apporpriate
        if digit >= radix:
            carry = True
            digit = digit % radix
        else:
            carry = False
        # Append the digit to the top of the result as a string.
        result = digit_to_str(digit) + result

    # Return the result. Sign is appeneded, leading zeros are removed and if there is another carry that is added.
    result = sign + removeLeadingZero(str(int(carry)) + result)
    return result




def integer_subtraction(x: str, y: str, radix: int):
    """
    Do an integer subtraction on the two inputs x and y represented as strings and return the result as a string.
    The second argument is deducted from the first. Both x and y have their value in the appropriate radix 
    specified by the input 'radix' which is an integer.
    """

    # Make inputs positive and remember their signs.
    x, y, negativeX, negativeY = signCheck(x, y)
    
    # If both numbers are negative it is the same as deducting the first number form the second.
    if negativeX and negativeY:
        return integer_subtraction(y, x, radix)
    
    # Deducting a positive number from a negative is the same as adding two negative numbers.
    elif negativeX:
        return integer_addition("-" + x, "-" +  y, radix)

    # Deducting a negative number from a positive is the same as adding both numbers.
    elif negativeY:
        return integer_addition(x, y, radix)

    # Make the size of both the inputs identical by adding leading zeroes
    x, y = addLeadingZero(x, y)

    # Deduct the small number from the big number.
    if not(geq(x, y)):
        return "-" + integer_subtraction(y, x, radix)

    # Introduce carry, digit and result
    carry = False
    digit = 0
    result = ""
    # Loop through all the digits starting from the rightmost digit
    for i in reversed(range(len(x))):
        # Subtract the i-th digits and the carry if it is used.
        digit = extended_int(x[i]) - extended_int(y[i]) - carry
        # If the subtraction is negative, add a radix and make the carry positive.
        if digit < 0:
            carry = True
            digit = digit + radix
        else:
            carry = False
        # Append the digit to the top of the result as a string.
        result = digit_to_str(digit) + result
    
    # Remove leading zeros and return
    result = removeLeadingZero(result)
    return result




def integer_primary_multiplication(x: str, y: str ,radix: int):
    """
    Do an integer multiplication on the two inputs x and y represented as strings and return the result as a string.
    Both x and y have their value in the appropriate radix specified by the input 'radix' which is an integer.
    """

    # If an input is zero return zero.
    if y == "0" or x == "0":
        return "0"
    
    # Make inputs positive and remember their signs.
    x, y , negativeX, negativeY = signCheck(x, y)
    result = "0"

    # Make the smallest number as the second number to ease computation.
    if geq(y, x):
        x, y = y, x
    
    # Loop through the digits of the second number starting from the rightmost digit
    for i in reversed(range(len(y))):
        # Introduce temoporary sum and carry
        temp = ""
        carry = 0
        # print(i)
        # Loop through the digits of the first number starting from the rightmost digit
        for j in reversed(range(len(x))):
            # Multiply the i-th digit of the second number and the j-th digit of the first number and add carry
            prod = (extended_int(y[i]) * extended_int(x[j])) + carry
            #  Append the digit to the temporary sum
            temp = digit_to_str(prod % radix) + temp 
            # Calculate multiplication carry
            carry = prod // radix
        # Add the last carry, and the zeros as in primary school multiplication
        temp = digit_to_str(carry) + temp + "0"*(len(y) - i - 1)
        # Add the temporary sum to the final result
        result = integer_addition(result, temp, radix)
    
    # Remove leading zeros, fix the sign and return
    result = removeLeadingZero(result)
    if negativeX ^ negativeY:
        result = "-" + result
    return result




def integer_karatsuba(x: str, y: str, radix: int):
    """
    Do an integer multiplication with the karatsuba method on the two inputs x and y represented as strings and return the result as a string.
    Both x and y have their value in the appropriate radix specified by the input 'radix' which is an integer.
    """

    # Make inputs positive and remember their signs.
    x, y, negativeX, negativeY = signCheck(x, y)

    # If only one input is negative fix the sign
    if negativeX ^ negativeY:
        return '-' + integer_karatsuba(x,y , radix)

    # If one of the inputs has 1 digit then do a primary school multiplication
    if len(x) < 2 or len(y) < 2:
        return integer_primary_multiplication(x, y, radix)
    
    # Make the size of both the inputs identical by adding leading zeroes
    x, y = addLeadingZero(x, y)

    if not (len(x) % 2 == 0):
        # add 0 to the start of x and y so that they are both of even length
        x = "0" + x
        y = "0" + y

    # Split the input into two
    x1, x2 = split_string(x)
    y1, y2 = split_string(y)

    # Multiply the first two halves together and the second two halves together
    ac = integer_karatsuba(x1, y1, radix)
    bd = integer_karatsuba(x2, y2, radix)

    # ad + bc = [(a + b) * (c + d)] - ac - bd
    ad_Plus_bc = integer_subtraction(integer_subtraction(integer_karatsuba(integer_addition(x1, x2, radix), integer_addition(y1, y2, radix), radix), ac, radix), bd, radix)

    # return ac*(radix^n) + ad_Plus_bc*(radix^(n/2)) + bd
    return integer_addition(integer_addition(ac + ("0" * (2 * (len(x)//2))), ad_Plus_bc + ("0" * (len(x)//2)), radix), bd, radix)


    
    
def integer_euclidian(x: str, y: str, radix: int):
    """
    Do an extended euclidain algorithm on both inputs in radix specified by 'radix' argument.
    Return gcd of x and y, return a and return b where (a*x + b*y = gcd). 
    """

    # Make inputs positive and remember their signs.
    x, y, negativeX, negativeY = signCheck(x,y)

    switch = False
    # If any of the inputs is zero return its coefficient as zero and the other coefficient as 1. The gcd is equal to the non-zero input
    if x =="0":
        return x, "1", y 
    elif y == "0":
        return "1", y, x
    # Rename x and y as a and b if x is bigger or b and a if y is bigger
    elif geq(x, y):
        a, b = x, y
    else:
        a, b = y, x
        switch = True

    # s is coefficient for x and t is coefficient for y.
    s_old = "1"
    s_new = "0"
    t_old = "0"
    t_new = "1" 

    # Loop until b hits zero
    while geq(b, "1"):
        # Execute extended euclidian algorithm as referenced in the lecture notes
        q, r = division(a, b, radix)
        s3 = integer_subtraction(s_old,integer_karatsuba(q,s_new,radix),radix)
        s_old = s_new
        s_new = s3
        t3 = integer_subtraction(t_old,integer_karatsuba(q,t_new,radix),radix)
        t_old = t_new
        t_new = t3
        a = b
        b = r 
    
    # If we already swiched the value we switch the coefficients
    if switch:
        s_old, t_old = t_old, s_old

    # Fix the result depending on x and y sign
    if negativeX:
        s_old= s_old[1:]

    if negativeY:
        t_old = t_old[1:]
    
    return s_old, t_old, a


### Modular Arithmetic ###

def modular_reduction(x: str, mod: str, radix: int):
    """
    Do a modular reduction on x with 'mod' as modulus with radix specified by argument 'radix'. x and modulus are inputed as strings. 
    """

    # If mod is 0 or less then return null
    if geq("0", mod):
        return 

    # Make x positive and remember the sign
    x, negativeX = singleSignCheck(x)

    # Deduct modulus from x until x is less than mod. If x has 2 more digits than mod or more than add zeros behind mod so we make less subtractions.
    while geq(x, mod):
        suffix = "0"*(len(x) - len(mod) - 1)
        x = integer_subtraction(x, mod + suffix, radix)    

    # If x was negative in the beginning subract current x from mod.
    if negativeX:
        x =  integer_subtraction(mod, x, radix)
    
    return x



  
def modular_addition(x: str, y: str, mod: str, radix: int):
    """
    Do a modular addition on x and y with 'mod' as a modulus and with radix specified by argument 'radix'. x, y and modulus are inputed as strings. 
    """
    # If mod is 0 or less then return null
    if geq("0", mod):
        return 
    # Do reduction on both x and y and then add and reduce the result
    x, y = modular_reduction(x, mod, radix), modular_reduction(y, mod, radix)
    result = integer_addition(x, y, radix)
    return modular_reduction(result, mod, radix)


    

def modular_subtraction(x: str, y: str, mod: str, radix: int):
    """
    Do a modular subtraction on x and y with 'mod' as a modulus and with radix specified by argument 'radix'. x, y and modulus are inputed as strings. 
    """

    # If mod is 0 or less then return null
    if geq("0", mod):
        return 
    # Do reduction on both x and y and then subtract and reduce the result
    x, y = modular_reduction(x, mod, radix), modular_reduction(y, mod, radix)
    result = integer_subtraction(x, y, radix)
    return modular_reduction(result, mod, radix)



     
def modular_multiplication(x: str, y: str, mod: str, radix: int):
    """
    Do a modular multiplication on x and y with 'mod' as a modulus and with radix specified by argument 'radix'. x, y and modulus are inputed as strings. 
    """

    # If mod is 0 or less then return null
    if geq("0", mod):
        return 
    # Do reduction on both x and y and then multiply and reduce the result
    x, y = modular_reduction(x, mod, radix), modular_reduction(y, mod, radix)
    result = integer_karatsuba(x, y, radix)
    return modular_reduction(result, mod, radix)




def modular_inversion(x: str, mod: str, radix: int):
    """
    Find the modular inverse of inputs x as a string with modulus as 'mod' and radix specified by 'radix'
    """

    # Do reduction on x
    x = modular_reduction(x, mod, radix)
    # Call extended euclidian algorithm
    a, b, g = integer_euclidian(x,mod,radix)
    # If gcd is not 1 then there is no inverse and else return coefficient of x reduced by mod.
    if g != "1":
        return
    else:
        return modular_reduction(a,mod, radix)


### Helping Functions ###

# Return the absolute value of string representation of number x as a string
def absolute(x: str):
    
    if x[0] == "-":
        return x[1:]
    return x



# Return whether x is bigger than y
def geq(x: str, y: str):

    x, y, negativeX, negativeY = signCheck(x, y)

    if negativeX and negativeY:
        return geq_absolute(y, x)
    elif negativeX:
        return False
    elif negativeY:
        return True
    else:
        return geq_absolute(x, y)



# Return whether x is bigger than y if they are both positive
def geq_absolute(x: str, y: str):

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



# Make the input positive and return if it was negative or not
def singleSignCheck(x: str):
    
    negativeX = False
    if x[0] == "-":
        negativeX = True
        x = absolute(x)
    return x, negativeX



# Make both inputs positive and return whether they were negative
def signCheck(x: str, y: str):
    
    x, negativeX = singleSignCheck(x)
    y, negativeY = singleSignCheck(y)
    return x, y, negativeX, negativeY



# Make number of digits equal for both x and y by adding leading zeros
def addLeadingZero(x: str, y: str):
    
    length_diff = len(x) - len(y)
    if length_diff > 0:
        y = ( "0" * length_diff ) + y
    elif length_diff < 0:
        x = ( "0" * abs(length_diff) ) + x
    return x, y



# Remove leading zeros.
def removeLeadingZero(x: str):
    
    while x[0] == "0" and len(x) > 1:
        x = x[1:]
    return x



# Split a string into two equal halves
def split_string(x: str):
    return x[:len(x)//2], x[len(x)//2:] 



# Return integer version of a number in string version.
def extended_int(x: str):
    
    if len(x) > 1:
        return extended_int(split_string(x)[0]) + extended_int(split_string(x)[1])
    else:
        x = ord(x)
        if 48 <= x <= 57:
            return x - 48
        elif 65 <= x <= 90:
            return x - 55
        else:
            return



# Convert a integer digit to a string version
def digit_to_str(x: int):
    
    if x < 10:
        return str(x)
    elif x < 35: 
        return chr(x + 55)
    else:
        return


# Divide x by y and return quotient and remainder
def division(x: str, y: str, radix: int):

    # you cant divide by 0 
    if y == "0":
        return 

    # Make inputs positive and remember their signs.
    x, y, negativeX, negativeY = signCheck(x,y)
    q = "0"

    if geq(x, y):    

        # Count how many times we can subtract y from x.
        while geq(x, y):
            x, q = integer_subtraction(x, y + "0"*(len(x) - len(y) - 1), radix), integer_addition(q, "1"+"0"*(len(x) - len(y) - 1), radix)   

        # Fix signs
        if negativeX ^ negativeY: #xor function
            q = "-" + q

    if negativeX:
        x = "-" + x
        
    return q, x



