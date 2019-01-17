from ga.algorithms import BaseGeneticAlgorithm
from ga.chromosomes import Chromosome
from ga.genes import BaseGene, Base10Gene
from numpy.random import choice, permutation, randint


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


class ClassSchedulingGeneticAlgorithm(BaseGeneticAlgorithm):
    def eval_fitness(self, chromosome):
        pass

    @staticmethod
    def create_random_chromosomes(n, courses_list, course_prof, timespan, course_room):
        chromosomes = list()
        for i in range(n):
            genes = list()
            for course in courses_list:
                genes.append(NameGene(course))  # course name
                genes.append(
                    NameGene(choice(course_prof[course])))  # random prof between profs who can teach this course
                genes.append(Base10Gene(str(choice(range(1, 6)))))  # day of week
                genes.append(Base10Gene(str(randint(timespan[0], timespan[1]))))
                genes.append(NameGene(choice(course_room[course])))  # random room between rooms with enough capacity
            chromosomes.append(Chromosome(genes))
        return chromosomes


class NameGene(BaseGene):
    GENETIC_MATERIAL_OPTIONS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. 1234567890'
