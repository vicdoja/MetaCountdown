import random

from simanneal import Annealer

from metacountdown.utils import DIFFICULT_INSTANCES, generate_tree, generate_valid, eval_sequence, mutate_tree_valid, mutate_tree

class NumericalSequenceAnnealer(Annealer):
    def __init__(self, state, objective, poss_num):
        self.objective = objective
        self.poss_num = poss_num
        super(NumericalSequenceAnnealer, self).__init__(state)  # important!

    def move(self):
        self.state = mutate_tree(self.state, 0.05, self.poss_num)[0]
        #self.state = mutate_tree_valid(self.state, 0.05, self.poss_num, self.objective)

    def energy(self):
        return eval_sequence(self.state, self.objective, self.poss_num)[0]

def main():
    random.seed(64)
    verbose = False
    max_gen = 300

    for obj, poss_num in DIFFICULT_INSTANCES[:1]:
        initial_tree = [generate_tree(2, poss_num)]

        print(initial_tree)

        annealer = NumericalSequenceAnnealer(initial_tree, obj,  poss_num)

        auto_schedule = annealer.auto(minutes=1)
        annealer.set_schedule(auto_schedule)

        print(annealer.anneal())

if __name__ == "__main__":
    main()