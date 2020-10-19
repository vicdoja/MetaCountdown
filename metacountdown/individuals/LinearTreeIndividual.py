from __future__ import annotations

from .AbstractIndividual import AbstractIndividual

from ..utils import eval_linear, OPS_LIST, OPS, MAX_FIT

from typing import Tuple

import random

import re

class LinearTreeIndividual(AbstractIndividual): 
	"""Complete

	"""

	def __init__(self, nums: Tuple[int, ...], ops: Tuple[str, ...]) -> None:
		"""Initialize the individual.

		Args:
			nums (Tuple[int, ...]): Terminals of the linear tree
			ops (Tuple[str, ...]): Operators to apply along the linear tree
		"""		
		self.nums = nums
		self.ops = ops

	def __str__(self):
		return " ".join([str(self.nums[0])]+["%s %d" % (self.ops[i], self.nums[i+1])\
			for i in range(len(self.ops))])

	@staticmethod  
	def evaluate_individual(ind: LinearTreeIndividual, objective: int, \
		pos_num: Tuple[int, ...]) -> Tuple[int, ]: 
		"""Calculate the fitness for a particular individual.

		Args:
			ind (LinearTreeIndividual): Individual to evaluate.
			objective (int): Objective value.
			pos_num (Tuple[int, ...]): Numbers available to use.

		Returns:
			int: Fitness of the individual ind.
		"""    
		un_ind = ind[0]
		terminals, operators = un_ind.nums, un_ind.ops
		
		res = eval_linear(pos_num, terminals, operators)

		return abs(res - objective),

	@classmethod
	def generate_individual(cls, pos_num: Tuple[int, ...]) \
		-> LinearTreeIndividual: 
		"""Generate an individual.

		Args:
			pos_num (Tuple[int, ...]): Numbers available to use.

		Returns:
			LinearTreeIndividual: Generated individual.
		"""    
		terminals = tuple(random.sample(range(len(pos_num)), \
			k=random.randint(1, len(pos_num))))
		operators = tuple(random.choices(OPS_LIST[:-1], k=len(terminals)-1))
		return cls(terminals, operators)
	
	@staticmethod
	def mutate_individual(ind: LinearTreeIndividual, pos_num: Tuple[int, ...], \
		indpb: float) -> Tuple[LinearTreeIndividual, ]: 
		"""Muate an individual in-place.

		Args:
			ind (LinearTreeIndividual): Individual to mutate.
		"""    
		un_ind = ind[0]
		terminals, operators = list(un_ind.nums), list(un_ind.ops)

		# Terminal swapping scan
		for i in range(len(terminals)):
			if random.random() < indpb:
				s = random.randint(0,len(terminals)-1)
				terminals[i], terminals[s] = terminals[s], terminals[i]

		# Operator swapping scan
		for i in range(len(operators)):
			if random.random() < indpb:
				s = random.randint(0,len(operators)-1)
				operators[i], operators[s] = operators[s], operators[i]

		valid_new_indexes = list(filter(lambda i: i not in terminals, \
			range(len(pos_num))))

		while random.random() < indpb:
			if not valid_new_indexes:
				valid_new_indexes.append(\
					terminals.pop(random.randint(0, len(terminals)-1)))
				operators.pop(random.randint(0, len(operators)-1))
			elif len(terminals) == 1:
				terminals.append(valid_new_indexes.pop(\
					random.randint(0, len(valid_new_indexes)-1)))
				operators.append(random.choice(OPS_LIST))
			else:
				if random.random() < 0.5:
					valid_new_indexes.append(\
						terminals.pop(random.randint(0, len(terminals)-1)))
					operators.pop(random.randint(0, len(operators)-1))
				else:
					terminals.append(valid_new_indexes.pop(\
						random.randint(0, len(valid_new_indexes)-1)))
					operators.append(random.choice(OPS_LIST))

		un_ind.nums, un_ind.ops = tuple(terminals), tuple(operators)

		return ind,

	@staticmethod
	def mate_individual(ind1: LinearTreeIndividual, \
						ind2: LinearTreeIndividual) \
		-> Tuple[LinearTreeIndividual, LinearTreeIndividual]:
		"""Mate two individuals in-place.

		Args:
			ind1 (LinearTreeIndividual): Parent individual 1.
			ind2 (LinearTreeIndividual): Parent individual 1.
		"""     
		un_ind1, un_ind2 = ind1[0], ind2[0]

		split = random.randint(0,\
			 max(0, min(len(un_ind1.ops), len(un_ind2.ops))-1))
		un_ind1.nums, un_ind2.nums = un_ind1.nums[:split+1]+\
			un_ind2.nums[split+1:], un_ind2.nums[:split+1]+un_ind1.nums[split+1:]
		un_ind1.ops, un_ind2.ops = un_ind1.ops[:split]+\
			un_ind2.ops[split:], un_ind2.ops[:split]+un_ind1.ops[split:]

		return ind1, ind2
