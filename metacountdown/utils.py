from typing import Union

import random
import re

OPS = {
  "+": (lambda a, b: a + b),
  "-": (lambda a, b: a - b),
  "*": (lambda a, b: a * b),
  "/": (lambda a, b: a / b)
}
OPS_LIST = list(OPS.keys())
MAX_FIT = 10**6

ALL_NUMBERS = 2*list(range(1,11)) + [25*i for i in range(1,5)]

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

def eval_polish(expression: str) -> Union[float, None]:
    """Given a mathematic expression in reverse polish notation as a string, 
    evaluate it and return the value.

    Args:
        expression (str): Expression to evaluate.

    Returns:
        Union[float, None]: Returns the evaluation of the result if it's valid,
                            None otherwise.
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

def eval_sequence(individual, OBJECTIVE, POSSIBLE_NUMBERS):
    #print("eval_seq", individual)
    max_fit = 10**6
    if any(x > y for x in [individual[0].count(str(t)) for t in POSSIBLE_NUMBERS] for y in [POSSIBLE_NUMBERS.count(t) for t in POSSIBLE_NUMBERS]):
        return max_fit,
    aux = eval_polish(individual[0])
    if aux == None:
        return max_fit,
    return abs(aux-OBJECTIVE),

def eval_alt(terminals, operators, POSSIBLE_NUMBERS):
    acc = float(POSSIBLE_NUMBERS[terminals[0]])
    for i, op in enumerate(operators):
        acc = OPS[op](acc, POSSIBLE_NUMBERS[terminals[i+1]])
    return acc

def eval_sequence_alt(individual, OBJECTIVE, POSSIBLE_NUMBERS):
    terminals, operators = individual
    
    res = eval_alt(terminals, operators, POSSIBLE_NUMBERS)

    if res < 0 or not res.is_integer():
        return 10**6,

    return abs(res - OBJECTIVE),


def generate_tree(max_depth, POSSIBLE_NUMBERS):
    if max_depth > 1:
        left  = "%s" % str(random.choice(POSSIBLE_NUMBERS)) if random.random() > 0.5 else generate_tree(max_depth - 1, POSSIBLE_NUMBERS)
        right = "%s" % str(random.choice(POSSIBLE_NUMBERS)) if random.random() > 0.5 else generate_tree(max_depth - 1, POSSIBLE_NUMBERS)
        return "%s %s %s" % (left, right, random.choice(OPS_LIST))
    else:
        return "%d %d %s" % (random.choice(POSSIBLE_NUMBERS), random.choice(POSSIBLE_NUMBERS), random.choice(OPS_LIST))

def generate_valid(max_depth, POSSIBLE_NUMBERS):
    if len(POSSIBLE_NUMBERS) < 2:
        return "%d" % (POSSIBLE_NUMBERS[0])

    shuffled = POSSIBLE_NUMBERS[:]
    random.shuffle(shuffled)
    cut_point = random.randint(1, len(shuffled) - 1)

    left_slice = shuffled[:cut_point]
    right_slice = shuffled[cut_point:]

    if max_depth > 1:
        left  = "%s" % str(random.choice(left_slice)) if random.random() < 0.5 else generate_valid(max_depth - 1, left_slice)
        right = "%s" % str(random.choice(right_slice)) if random.random() < 0.5 else generate_valid(max_depth - 1, right_slice)
    else:
        left  = str(random.choice(left_slice))
        right = str(random.choice(right_slice))

    operator = random.choice(OPS_LIST)

    if operator == "/" and eval_polish("%s %s %s" % (left, right, operator)) == None:
        if random.random() < 0.1:
            return "%d" % (shuffled[0])
        else:
            operator = random.choice(OPS_LIST[:-1])

    return "%s %s %s" % (left, right, operator)

def generate_tree_alt(POSSIBLE_NUMBERS):
    terminals = tuple(random.sample(range(len(POSSIBLE_NUMBERS)), k=random.randint(1, len(POSSIBLE_NUMBERS))))
    operators = tuple(random.choices(OPS_LIST[:-1], k=len(terminals)-1))
    return terminals, operators

def mutate_tree(ind, indpb, POSSIBLE_NUMBERS):
    mutant = ""
    for t in ind[0].split():
        if random.random() < indpb:
            if t in OPS_LIST:
                mutant += " " + random.choice(OPS_LIST)
            else:
                mutant += " " + str(random.choice(POSSIBLE_NUMBERS))
        else:
            mutant += " " + t
    ind[0] = mutant
    return ind,

def mutate_tree_valid(ind, indpb, POSSIBLE_NUMBERS):
    # COMPLETE
    bag = {}
    mutant = ""
    for t in ind[0].split():
        if random.random() < indpb:
            if t in OPS_LIST:
                mutant += " " + random.choice(OPS_LIST)
            else:
                mutant += " " + str(random.choice(POSSIBLE_NUMBERS))
        else:
            mutant += " " + t
    ind[0] = mutant
    return ind,

def mutate_tree_alt(ind, indpb, POSSIBLE_NUMBERS):
    terminals, operators = list(ind[0]), list(ind[1])

    

    if len(terminals) == 1:
        pass
    elif len(terminals) == len(POSSIBLE_NUMBERS):
        pass
    else:
        pass
    return ind,

def find_subtree(tree, p):
    toks = tree.split()
    toks.reverse()

    if toks[p-1] not in OPS_LIST:
        sel = toks[p-1]
        toks[p-1] = "#"
        wild = " ".join(reversed(toks))
        #print([sel, wild])
        return sel, wild

    aux = 2
    wild = ""
    sel = ""

    for t in toks:
        if p > 0:
            p -= 1
            if p == 0:
                sel = t
                wild = "# " + wild
            else:
                wild = t + " " + wild
        elif aux > 0:
            if t in OPS_LIST:
                aux += 1
            else:
                aux -= 1
            sel = t + " " + sel
        else:
            wild = t + " " + wild
    
    #print([sel, wild])
    return sel, wild

def mate_tree(ind1, ind2):
    p1, p2 = random.randint(1, len(ind1[0].split())), random.randint(1, len(ind2[0].split()))

    sel1, wild1 = find_subtree(ind1[0], p1)
    sel2, wild2 = find_subtree(ind2[0], p2)

    '''print([wild1, wild2])
    print([sel1, sel2])'''

    ind1[0], ind2[0] = re.sub("#", sel2, wild1).strip(), re.sub("#", sel1, wild2).strip()

    return ind1, ind2

def mate_tree_alt(ind1, ind2):
    return ind1, ind2