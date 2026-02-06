def tokenize(equ):
    result = []
    number = ""
    
    for i in equ:
        if i in "1234567890":
            number += i
        else:
            if number:
                result.append(number)
                number = ""
            result.append(i)
    if number:
        result.append(number)
    return result

def priority(ope):
    if ope == "*" or ope == "/":
        return 2
    elif ope == "+" or ope == "-":
        return 1
    else:
        return 0
def infix_to_rpn(equ):
    stack = []
    result = []

    for ope in equ:
        if ope[0].isdigit():
            result.append(ope)

        elif ope in "*/+-":
            while (stack and priority(stack[-1]) >= priority(ope)):
                result.append(stack.pop())
            stack.append(ope)
    
    while stack:
        result.append(stack.pop())
    return result

def cal_rpn(rpn_equ):
    stack = []
    for ope in rpn_equ:
        if ope.isdigit():
            stack.append(int(ope))

        else:
            if len(stack) < 2: return None
            b = stack.pop()
            a = stack.pop()

            if ope == "+": stack.append(a + b)
            elif ope == "-": stack.append(a - b)
            elif ope == "*": stack.append(a * b)
            elif ope == "/":
                if b == 0 or a % b != 0: return None
                stack.append(a / b)
    if stack:
        return stack[0]
    return None
def is_valid_equation(equ):
    if equ.count("=") != 1:
        return False
    
    parts = equ.split('=')
    left = parts[0]
    right = parts[1]

    if not left or not right:
        return False
    
    left_value = cal_rpn(infix_to_rpn(tokenize(left)))
    right_value = cal_rpn(infix_to_rpn(tokenize(right)))

    if left_value == right_value:
        return True
    return False
