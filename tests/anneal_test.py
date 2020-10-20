import random

from simanneal import Annealer

from metacountdown.utils import DIFFICULT_INSTANCES, eval_polish
from metacountdown.individuals import LinearTreeIndividual

class NumericalSequenceAnnealer(Annealer):
    def __init__(self, state, objective, poss_num):
        self.objective = objective
        self.poss_num = poss_num
        super(NumericalSequenceAnnealer, self).__init__(state)  # important!

    def move(self):
        self.state = LinearTreeIndividual.mutate_individual\
            (self.state, self.poss_num, 0.05)[0]

    def energy(self):
        return LinearTreeIndividual.evaluate_individual\
            (self.state, self.objective, self.poss_num)[0]

def main():
    random.seed(64)
    verbose = False
    max_gen = 300

    for obj, poss_num in DIFFICULT_INSTANCES:
        initial_tree = \
            [LinearTreeIndividual.generate_individual(pos_num=poss_num)]

        annealer = NumericalSequenceAnnealer(initial_tree, obj,  poss_num)

        auto_schedule = annealer.auto(minutes=0.05)
        annealer.set_schedule(auto_schedule)

        result = annealer.anneal()
        print()
        print(result[0][0], LinearTreeIndividual.evaluate_individual(result[0],\
            obj,poss_num)[0], obj)

if __name__ == "__main__":
    main()