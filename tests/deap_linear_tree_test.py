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

def init(obj=None, poss_num=None):
    if not obj:
        obj = random.randint(101, 999)
    if not poss_num:
        poss_num = random.choices(ALL_NUMBERS, k=6)

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
    toolbox.register("gen_tree", LinearTreeIndividual.generate_individual, \
      	pos_num=poss_num)

    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, \
      	toolbox.gen_tree, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", LinearTreeIndividual.evaluate_individual, \
      	objective=obj, pos_num=poss_num)

    toolbox.register("mate", LinearTreeIndividual.mate_individual)
    toolbox.register("mutate", LinearTreeIndividual.mutate_individual, \
      	pos_num=poss_num, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=10)

    return toolbox, pool, obj, poss_num

def main():
    random.seed(64)
    verbose = True
    max_gen = 10
    pop_size = 3000

    for obj, poss_num in DIFFICULT_INSTANCES[:]:
        toolbox, pool, obj, poss_num = init(obj=obj, poss_num=poss_num)
        
        pop = toolbox.population(n=pop_size)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values[0])
        stats.register("best", numpy.min)
        stats.register("valid", lambda pop: (numpy.array(pop) < 10**6).sum())
        stats.register("invalid", lambda pop: (numpy.array(pop) >= 10**6).sum())
        stats.register("% of valid", \
         	lambda pop: (numpy.array(pop) < 10**6).sum()/len(pop))
        
        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, \
          	ngen=max_gen, stats=stats, halloffame=hof, verbose=verbose)

        #pool.close()

        print("-"*30)
        print("The objective number is %d \nAnd the usable numbers are %s" % \
          	(obj, poss_num))
        print(list(zip(map(lambda o: str(o[0]),hof), \
            [(eval_linear(poss_num, i[0].nums, i[0].ops), \
			abs(eval_linear(poss_num,i[0].nums,i[0].ops)-obj)) for i in hof])))
        print()

if __name__ == "__main__":
    main()
