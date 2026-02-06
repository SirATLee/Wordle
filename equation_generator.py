import random
from RPN import *
def generate_equation(length):
    op = ["+", "-", "*", "/"]
    while True:
        print(1)
        num_ops = random.choice([1,2])
        if num_ops == 2:
            numbers = [random.randint(1,10) for _ in range(num_ops + 1)]
        else:
            numbers = [random.randint(1,99) for _ in range(num_ops + 1)]
        ops = [random.choice(op) for _ in range(num_ops)]
        
        left = ""
        for i in range(num_ops):
            left += str(numbers[i]) + ops[i]
        left += str(numbers[-1])

        try:
            right = cal_rpn(infix_to_rpn(tokenize(left)))
            if right is None or right < 0 or right != int(right):
                continue

            full_equ = left + "=" + str(int(right))

            if len(full_equ) == length:
                return full_equ
        except:
            continue
