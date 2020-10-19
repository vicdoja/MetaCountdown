from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Tuple
  
class AbstractIndividual(ABC): 
	"""Abstract class for every other individual.

	This abstract class forces every other class for an individual 
	to implement mandatory functions.

	"""

	def __init__(self) -> None:
		"""Init function of the class.

		"""    
		pass

	@abstractmethod
	def __str__(self):
		pass

	@staticmethod
	@abstractmethod  
	def evaluate_individual(ind: AbstractIndividual) -> Tuple[int, ]: 
		"""Calculate the fitness for a particular individual.

		Args:
			ind (AbstractIndividual): Individual to evaluate.

		Returns:
			int: Fitness of the individual ind.
		"""    
		pass

	@classmethod
	@abstractmethod
	def generate_individual(cls) -> AbstractIndividual: 
		"""Generate an individual.

		Returns:
			AbstractIndividual: Generated individual.
		"""    
		pass

	@staticmethod
	@abstractmethod
	def mutate_individual(ind: AbstractIndividual) -> Tuple[AbstractIndividual, ]: 
		"""Muate an individual in-place.

		Args:
			ind (AbstractIndividual): Individual to mutate.
		"""    
		pass

	@staticmethod
	@abstractmethod
	def mate_individual(ind1: AbstractIndividual, ind2: AbstractIndividual) \
		-> Tuple[AbstractIndividual, AbstractIndividual]:
		"""Mate two individuals in-place.

		Args:
			ind1 (AbstractIndividual): Parent individual 1.
			ind2 (AbstractIndividual): Parent individual 1.
		"""     
		pass

  