from deap import algorithms
from deap import base
from deap import creator 
from deap import tools

from metacountdown.individuals import LinearTreeIndividual, AbstractIndividual
from metacountdown.utils import ALL_NUMBERS, MAX_FIT

from typing import Union, List, Callable, Tuple

import random

import numpy

def run_optim_loop(obj: Union[int, None] = None, \
    poss_num: Union[List[int], None] = None, \
    ind_type: AbstractIndividual = LinearTreeIndividual, \
    tour_type: Callable = tools.selTournament) \
    -> Tuple[tools.Logbook, List[type(AbstractIndividual)]]:
    """This function runs the full genetic algorithm on the given
    instance and with the given parameters.

    Args:
        obj (Union[int, None], optional): Objective value of the instance. 
            Defaults to None.
        poss_num (Union[List[int, ...], None], optional): Possible numbers of 
            the instance. Defaults to None.
        ind_type (AbstractIndividual, optional): Type of representation for 
            the individual. Defaults to LinearTreeIndividual.
        tour_type (function, optional): Individual selection function. 
            Defaults to tools.selTournament.

    Returns:
        Tuple[tools.Logbook, List[AbstractIndividual, ...]]: Returns the object 
            with the calculated statistics along generations and the hall of 
            fame of individuals
    """    

    random.seed(64)
    verbose = True
    max_gen = 10
    pop_size = 3000

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
    toolbox.register("gen_tree", ind_type.generate_individual, \
      	pos_num=poss_num)

    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual, \
      	toolbox.gen_tree, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", ind_type.evaluate_individual, \
      	objective=obj, pos_num=poss_num)

    toolbox.register("mate", ind_type.mate_individual)
    toolbox.register("mutate", ind_type.mutate_individual, \
      	pos_num=poss_num, indpb=0.05)
    toolbox.register("select", tour_type, tournsize=10)

    pop = toolbox.population(n=pop_size)
    hof = tools.HallOfFame(3)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("best", numpy.min)
    stats.register("valid", lambda pop: (numpy.array(pop) < MAX_FIT).sum())
    stats.register("invalid", lambda pop: (numpy.array(pop) >= MAX_FIT).sum())
    stats.register("% of valid", \
        lambda pop: (numpy.array(pop) < MAX_FIT).sum()/len(pop))
    
    pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, \
        ngen=max_gen, stats=stats, halloffame=hof, verbose=verbose)

    return log, hof
