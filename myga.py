from ga.algorithms import BaseGeneticAlgorithm
from ga.chromosomes import Chromosome
from ga.genes import BaseGene, Base10Gene
from numpy.random import choice, randint
from collections import defaultdict
from numpy import std


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
    def __init__(self, chromosomes, separates: list):
        super().__init__(chromosomes)
        self.separates = separates
        self.a1 = .4
        self.a2 = .2
        self.a3 = .3
        self.a4 = .1

    def eval_fitness(self, chromosome):
        """
        CPDHR: index i is Course, i+1 is Prof, i+2 is Day of week, i+3 is Hour, i+4 is Room
        """
        num_days_sum = 0
        num_rooms_sum = 0
        dist_sum = 0
        total_time = [0, 0, 0, 0, 0, 0, 0]
        prof_day = defaultdict(lambda: [])
        prof_room = defaultdict(lambda: [])
        course_day = dict()
        genes = chromosome.genes
        for i in range(0, len(genes), 5):
            if not prof_day[genes[i + 1].dna].count(genes[i + 2].dna):
                num_days_sum += 1
                prof_day[genes[i + 1].dna].append(genes[i + 2].dna)
            if not prof_room[genes[i + 1].dna].count(genes[i + 4].dna):
                num_rooms_sum += 1
                prof_room[genes[i + 1].dna].append(genes[i + 4].dna)
            total_time[int(genes[i + 2].dna) - 1] += int(genes[i + 3].dna)
            course_day[genes[i].dna] = int(genes[i + 2].dna)
        std_total_time = std(total_time)
        for seperate_list in self.separates:
            c_a = course_day[seperate_list[0]]
            c_b = course_day[seperate_list[1]]
            dist_sum += abs(c_a - c_b)
        return self.a1 * num_days_sum + self.a2 * num_rooms_sum + self.a3 * std_total_time - self.a4 * dist_sum

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
