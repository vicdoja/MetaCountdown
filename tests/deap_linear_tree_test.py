import multiprocessing
import random
import math
import re

import numpy

# pylint: disable=no-member
from deap import algorithms
from deap import base
from deap import creator 
from deap import tools

from metacountdown.individuals import LinearTreeIndividual
from metacountdown.utils import ALL_NUMBERS, DIFFICULT_INSTANCES, eval_linear
from metacountdown.solvers.genetic import run_optim_loop

def main():
    random.seed(64)
    verbose = True
    max_gen = 10
    pop_size = 3000

    for obj, poss_num in DIFFICULT_INSTANCES[:]:
        log, hof = run_optim_loop(obj, poss_num)

        print("-"*30)
        print("The objective number is %d \nAnd the usable numbers are %s" % \
          	(obj, poss_num))
        print(list(zip(map(lambda o: str(o[0]),hof), \
            [(eval_linear(poss_num, i[0].nums, i[0].ops), \
			abs(eval_linear(poss_num,i[0].nums,i[0].ops)-obj)) for i in hof])))
        print()

if __name__ == "__main__":
    main()
