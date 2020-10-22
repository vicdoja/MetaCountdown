from typing import Union, Tuple

import random
import re

import numpy

OPS = {
	"+": (lambda a, b: a + b),
	"-": (lambda a, b: a - b),
	"*": (lambda a, b: a * b),
	"/": (lambda a, b: a / b)
}
OPS_LIST = list(OPS.keys())
MAX_FIT = numpy.Infinity

ALL_NUMBERS = 2*list(range(1,11)) + [25*i for i in range(1,5)]
ALL_NUMBERS_EXP = 3*list(range(1,11)) + 2*list(range(10,110,10)) + [25*i*10 for i in range(1,5)]

DIFFICULT_INSTANCES = [
    (264, [9  , 6  , 75, 7 , 2  , 50 ]),
    (458, [5  , 3  , 9 , 50, 4  , 5  ]),
    (322, [1  , 10 , 3 , 3 , 75 , 4  ]),
    (305, [100, 2  , 6 , 4 , 25 , 6  ]),
    (274, [2  , 1  , 10, 10, 7  , 100]),
    (661, [1  , 100, 4 , 50, 3  , 4  ]),
    (431, [10 , 8  , 75, 2 , 100, 4  ]),
    (511, [100, 75 , 1 , 8 , 3  , 75 ]),
    (407, [100, 3  , 2 , 25, 3  , 9  ]),
    (713, [5  , 50 , 1 , 8 , 75 , 8  ])
]

def eval_polish(expression: str) -> Union[int, None]:
    """Given a mathematic expression in reverse polish notation as a string, 
    evaluate it and return the value.

    Args:
        expression (str): Expression to evaluate.

    Returns:
        Union[int, None]: Returns the evaluation of the expression if it's
                          valid, None otherwise.

    """    
    #print("eval_polish", expression)
    tokens = expression.split()
    stack = []

    for token in tokens:
        if token in OPS:
            arg2 = stack.pop()
            arg1 = stack.pop()
            if token == "/" and arg2 == 0:
                return None
            result = OPS[token](arg1, arg2)
            if isinstance(result, float) and not result.is_integer():
                return None
            stack.append(int(result))
        else:
            stack.append(int(token))

    return stack.pop()

def eval_linear(pos_num: Tuple[int, ...], terminals: Tuple[int, ...], \
    operators: Tuple[str, ...]) -> int:
    """[summary]

    Args:
        pos_num (Tuple[int, ...]): Possible numbers.
        terminals (Tuple[int, ...]): List of indexes for pos_num.
        operators (Tuple[str, ...]): List of operators to apply.

    Returns:
        int: Returns the evaluation of the linear expression defined by
             the parameters terminals and operators
    """    
    #print(terminals, operators)
    res = int(pos_num[terminals[0]])
    for i, op in enumerate(operators):
        if op == "/" and pos_num[terminals[i+1]] == 0:
            return None
        res = OPS[op](res, pos_num[terminals[i+1]])
        if isinstance(res, float) and not res.is_integer():
            return None
        res = int(res)
    return res

def generate_valid_general(max_depth, POSSIBLE_NUMBERS):
    if len(POSSIBLE_NUMBERS) < 2:
        return "%d" % (POSSIBLE_NUMBERS[0])

    shuffled = POSSIBLE_NUMBERS[:]
    random.shuffle(shuffled)
    cut_point = random.randint(1, len(shuffled) - 1)

    left_slice = shuffled[:cut_point]
    right_slice = shuffled[cut_point:]

    if max_depth > 1:
        left  = "%s" % str(random.choice(left_slice)) if random.random() < 0.5\
            else generate_valid_general(max_depth - 1, left_slice)
        right = "%s" % str(random.choice(right_slice)) if random.random() < 0.5\
            else generate_valid_general(max_depth - 1, right_slice)
    else:
        left  = str(random.choice(left_slice))
        right = str(random.choice(right_slice))

    operator = random.choice(OPS_LIST)

    if operator == "/" and \
        eval_polish("%s %s %s" % (left, right, operator)) == None:
        if random.random() < 0.1:
            return "%d" % (shuffled[0])
        else:
            operator = random.choice(OPS_LIST[:-1])

    return "%s %s %s" % (left, right, operator)
