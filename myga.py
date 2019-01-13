from ga.algorithms import BaseGeneticAlgorithm
from ga.chromosomes import Chromosome


class KnapSackGeneticAlgorithm(BaseGeneticAlgorithm):
    def __init__(self, chromosomes, filename):
        super().__init__(chromosomes)
        self.items = list()
        with open(filename, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if i == 0:
                    self.max_weight = int(line.split()[1])
                else:
                    # first value, second weight
                    self.items.append(list(map(int, line.split())))

    def eval_fitness(self, chromosome: Chromosome):
        cum_value = 0
        cum_weight = 0
        for i, item in enumerate(self.items):
            if chromosome.dna[i] == '1':
                cum_value += item[0]
                cum_weight += item[1]
        if cum_weight <= self.max_weight:
            return cum_value
        else:
            return 0
