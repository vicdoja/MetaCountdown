from abc import ABC, abstractmethod
  
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
  @staticmethod  
  def evaluate_individual(ind: AbstractIndividual) -> int: 
    """Calculate the fitness for a particular individual.

    Args:
        ind (AbstractIndividual): Individual to evaluate.

    Returns:
        int: Fitness of the individual ind.
    """    
    pass

  @abstractmethod
  @classmethod
  def generate_individual(cls) -> AbstractIndividual: 
    """Generate an individual.

    Returns:
        AbstractIndividual: Generated individual.
    """    
    pass

  @abstractmethod
  @staticmethod
  def mutate_individual(ind: AbstractIndividual): 
    """Muate an individual in-place.

    Args:
        ind (AbstractIndividual): Individual to mutate.
    """    
    pass

  @abstractmethod
  @staticmethod
  def mate_individual(ind1: AbstractIndividual, ind2: AbstractIndividual):
    """Mate two individuals in-place.

    Args:
        ind1 (AbstractIndividual): Parent individual 1.
        ind2 (AbstractIndividual): Parent individual 1.
    """     
    pass

  