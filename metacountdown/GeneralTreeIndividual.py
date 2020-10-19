from __future__ import annotations

from .AbstractIndividual import AbstractIndividual

from .utils import eval_polish, OPS_LIST, MAX_FIT

from typing import Tuple

import random

import re

class GeneralTreeIndividual(AbstractIndividual): 
  """This class inherits from the abstract individual class. It represents
  the way of coding an individual as an expression string.

  This way of coding covers more extensively the search space, but
  in turn is more expensive and produces more invalid individuals.

  """

  def __init__(self, expr: str) -> None:
    """Init function of the class.

    Args:
        expr (str): Expression that defines the individual
                    with numbers and operators.
    """    
    self.expr = expr

  @staticmethod  
  def evaluate_individual(ind: GeneralTreeIndividual, objective: int, \
    pos_num: Tuple[int, ...]) -> Tuple[int, ]: 
    """Calculate the fitness for a particular individual.

    Args:
        ind (GeneralTreeIndividual): Individual to evaluate.
        objective (int): Objective value.
        pos_num (Tuple[int, ...]): Numbers available to use.

    Returns:
        int: Fitness of the individual ind.
    """    
    un_ind = ind[0]
    if any(un_ind.expr.count(str(n)) > pos_num.count(n) for n in set(pos_num)):
        return MAX_FIT,
    aux = eval_polish(un_ind.expr)
    if aux == None:
        return MAX_FIT,
    return abs(aux-objective),

  @classmethod
  def generate_individual(cls, pos_num: Tuple[int, ...]) \
    -> GeneralTreeIndividual: 
    """Generate an individual.

    Args:
        pos_num (Tuple[int, ...]): Numbers available to use.

    Returns:
        GeneralTreeIndividual: Generated individual.
    """    
    return cls(GeneralTreeIndividual.recursive_tree(pos_num, 3))
  
  @staticmethod
  def recursive_tree(pos_num: Tuple[int, ...], m_d: int) -> str:
    if m_d > 1:
        left  = "%s" % str(random.choice(pos_num)) if random.random() > 0.5 \
          else GeneralTreeIndividual.recursive_tree(pos_num, m_d - 1)
        right = "%s" % str(random.choice(pos_num)) if random.random() > 0.5 \
          else GeneralTreeIndividual.recursive_tree(pos_num, m_d - 1)
        return "%s %s %s" % (left, right, random.choice(OPS_LIST))
    else:
        return "%d %d %s" % (random.choice(pos_num), random.choice(pos_num), \
          random.choice(OPS_LIST))

  @staticmethod
  def mutate_individual(ind: GeneralTreeIndividual, pos_num: Tuple[int, ...], \
    indpb: float) -> Tuple[GeneralTreeIndividual, ]: 
    """Muate an individual in-place.

    Args:
        ind (GeneralTreeIndividual): Individual to mutate.
    """    
    un_ind = ind[0]
    mutant = ""
    for t in un_ind.expr.split():
        if random.random() < indpb:
            if t in OPS_LIST:
                mutant += " " + random.choice(OPS_LIST)
            else:
                mutant += " " + str(random.choice(pos_num))
        else:
            mutant += " " + t
    un_ind.expr = mutant
    return ind,

  @staticmethod
  def mate_individual(ind1: GeneralTreeIndividual, \
                      ind2: GeneralTreeIndividual) \
    -> Tuple[GeneralTreeIndividual, GeneralTreeIndividual]:
    """Mate two individuals in-place.

    Args:
        ind1 (GeneralTreeIndividual): Parent individual 1.
        ind2 (GeneralTreeIndividual): Parent individual 1.
    """     
    un_ind1, un_ind2 = ind1[0], ind2[0]
    p1 = random.randint(1, len(un_ind1.expr.split()))
    p2 = random.randint(1, len(un_ind2.expr.split()))

    sel1, wild1 = GeneralTreeIndividual.find_subtree(un_ind1.expr, p1)
    sel2, wild2 = GeneralTreeIndividual.find_subtree(un_ind2.expr, p2)

    '''print([wild1, wild2])
    print([sel1, sel2])'''

    un_ind1.expr = re.sub("#", sel2, wild1).strip() 
    un_ind2.expr = re.sub("#", sel1, wild2).strip()

    return ind1, ind2

  @staticmethod
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
    
    return sel, wild