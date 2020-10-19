import multiprocessing
import random
import math
import re

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import metacountdown.utils as utils

def init(obj=None, poss_num=None):
    if not obj:
        obj = random.randint(101, 999)
    if not poss_num:
        poss_num = random.choices(utils.ALL_NUMBERS, k=6)

    try:
        del creator.FitnessMin
        del creator.Individual
    except:
        pass

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    #pool = multiprocessing.Pool()
    pool = "fun"
    #toolbox.register("map", pool.map)

    # Attribute generator
    toolbox.register("gen_tree", utils.generate_tree, max_depth=3, POSSIBLE_NUMBERS=poss_num)
    #toolbox.register("gen_tree", generate_valid, max_depth=3, POSSIBLE_NUMBERS=poss_num)
    #toolbox.register("gen_tree", utils.generate_tree_alt, POSSIBLE_NUMBERS=poss_num)

    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.gen_tree)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", utils.eval_sequence, OBJECTIVE=obj, POSSIBLE_NUMBERS=poss_num)
    #toolbox.register("evaluate", utils.eval_sequence_alt, OBJECTIVE=obj, POSSIBLE_NUMBERS=poss_num)

    #toolbox.register("mate", utils.mate_tree_alt)
    toolbox.register("mate", utils.mate_tree)
    #toolbox.register("mutate", utils.mutate_tree_alt, indpb=0.05, POSSIBLE_NUMBERS=poss_num)
    toolbox.register("mutate", utils.mutate_tree, indpb=0.05, POSSIBLE_NUMBERS=poss_num)
    toolbox.register("select", tools.selTournament, tournsize=10)
    #toolbox.register("select", tools.selDoubleTournament, fitness_size=3, parsimony_size=2, fitness_first=True)

    return toolbox, pool, obj, poss_num

def main():
    random.seed(64)
    verbose = True
    max_gen = 300
    pop_size = 1000

    for obj, poss_num in utils.DIFFICULT_INSTANCES[:]:
        toolbox, pool, obj, poss_num = init(obj=obj, poss_num=poss_num)
        
        pop = toolbox.population(n=pop_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values[0])
        stats.register("best", numpy.min)
        stats.register("valid", lambda pop: (numpy.array(pop) < 10**6).sum())
        stats.register("invalid", lambda pop: (numpy.array(pop) >= 10**6).sum())
        stats.register("% of valid", lambda pop: (numpy.array(pop) < 10**6).sum()/len(pop))
        
        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=max_gen, 
                                    stats=stats, halloffame=hof, verbose=verbose)

        #pool.close()

        print("-"*30)
        print("The objective number is %d \nAnd the usable numbers are %s" % (obj, poss_num))
        print(list(zip(hof, [(utils.eval_alt(i[0], i[1], poss_num), utils.eval_sequence_alt(i, obj, poss_num)[0]) for i in hof])))
        #print(list(zip(hof, [(utils.eval_polish(i[0]), abs(utils.eval_polish(i[0])-obj)) for i in hof])))
        print()

if __name__ == "__main__":
    main()
