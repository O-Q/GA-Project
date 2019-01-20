import random
import string

from ga.algorithms import BaseGeneticAlgorithm
from ga.chromosomes import Chromosome
from ga.genes import BaseGene, Base10Gene
from numpy.random import choice, randint
from collections import defaultdict
from numpy import std, ceil


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
    def create_random_chromosomes(n, courses_list, course_prof, timespan, course_room, course_hour):
        chromosomes = list()
        for i in range(n):
            genes = list()
            rooms = defaultdict(
                lambda: [[x for x in range(timespan[0], timespan[1])] for _ in range(5)])  # 5 days is work day
            profs = defaultdict(
                lambda: [[x for x in range(timespan[0], timespan[1])] for _ in range(5)])  # 5 days is work day
            for course in courses_list:
                genes.append(NameGene(course))  # course name
                while True:
                    selected_prof = choice(course_prof[course])  # random prof between profs who can teach this course
                    selected_room = choice(course_room[course])  # random room between rooms with enough capacity
                    days = [d + 1 for d in range(5)]
                    selected_day = choice(days)
                    hours_needed = int(ceil(course_hour[course]))
                    room_free_hours = rooms[selected_room][selected_day - 1]
                    prof_free_hours = profs[selected_prof][selected_day - 1]
                    intersection_prof_room_free = [value for value in prof_free_hours if value in room_free_hours]
                    if intersection_prof_room_free:
                        hour = choice(intersection_prof_room_free)
                        for h in range(hours_needed):
                            if rooms[course][selected_day - 1].count(hour + h) and profs[course][
                                selected_day - 1].count(hour + h):
                                rooms[course][selected_day - 1].remove(hour + h)
                                profs[course][selected_day - 1].remove(hour + h)
                            else:
                                continue
                        genes.append(NameGene(selected_prof, compare_to=course_prof[course], name='prof'))
                        genes.append(DayOfWeekGene(str(selected_day), name='day'))  # day of week
                        genes.append(HourGene(str(hour), timespan, name='hour'))
                        genes.append(NameGene(selected_room, course_room[course], name='room'))

                        break
            chromosomes.append(CSChromosome(genes, course_hour))
        return chromosomes


class NameGene(BaseGene):
    GENETIC_MATERIAL_OPTIONS = string.ascii_letters + '. 1234567890'

    def __init__(self, dna, compare_to=None, suppressed=False, name=None):
        super().__init__(dna, suppressed, name)
        self.compare_to = compare_to

    def copy(self):
        return type(self)(self.dna, compare_to=self.compare_to, suppressed=self.suppressed, name=self.name)

    def mutate(self, p_mutate):
        if self.compare_to and len(self.compare_to) > 1 and random.random() < p_mutate:
            new_dna = self.dna
            while new_dna == self.dna:
                new_dna = choice(self.compare_to)
            self.dna = new_dna


class DayOfWeekGene(BaseGene):
    GENETIC_MATERIAL_OPTIONS = '1234567'

    def mutate(self, p_mutate):
        if random.random() < p_mutate:
            # It can be GENERIC_MATERIAL_OPTIONS but tur and fri are holiday and have not been choose
            days = [1, 2, 3, 4, 5]
            days.remove(int(self.dna))
            self.dna = str(choice(days))


class HourGene(BaseGene):
    GENETIC_MATERIAL_OPTIONS = '1234567890'

    def __init__(self, dna, span, suppressed=False, name=None):
        super().__init__(dna, suppressed=suppressed, name=name)
        self.timespan = span

    def copy(self):
        """ Return a new instance of this gene with the same DNA. """
        return type(self)(self.dna, self.timespan, suppressed=self.suppressed, name=self.name)

    def mutate(self, p_mutate):
        assert 0 <= int(self.dna) < 24
        if random.random() < p_mutate:
            new_dna = self.dna
            while new_dna == self.dna:
                new_dna = str(choice(randint(self.timespan[0], self.timespan[1])))
            self.dna = new_dna


class CSChromosome(Chromosome):
    # CPDHR: index   i is Course, i + 1 is Prof, i + 2 is Dayofweek, i + 3 is Hour, i + 4 is Room

    def __init__(self, genes, course_duration):
        super().__init__(genes)
        rooms = defaultdict(lambda: [[] for _ in range(5)])  # 5 days is work day
        profs = defaultdict(lambda: [[] for _ in range(5)])
        self.course_duration = course_duration
        self.update_tables()

    def copy(self):
        """ Return a new instance of this chromosome by copying its genes. """
        genes = [g.copy() for g in self.genes]
        return type(self)(genes, self.course_duration)

    def crossover(self, chromosome, points):
        assert len(self.genes) == len(chromosome.genes)
        new_genes = []
        other_new_genes = []
        points = [i for i in range(len(self.genes))]
        first = True
        while first or (not self.is_valid or not chromosome.is_valid):
            new_genes = []
            other_new_genes = []
            if points:
                point = choice(points)
                points.remove(point)
            else:
                return
            new_genes += chromosome.genes[0:point]
            other_new_genes += self.genes[0:point]
            new_genes += chromosome.genes[point:]
            other_new_genes += self.genes[point:]
            self.after_crossover(chromosome)

        self.genes = new_genes
        chromosome.genes = other_new_genes

    def after_crossover(self, another_chromosome):
        self.update_tables()
        another_chromosome.update_tables()

    def after_mutate(self):
        self.update_tables()

    def update_tables(self):
        self.rooms = defaultdict(lambda: [[] for _ in range(5)])  # 5 days is work day
        self.profs = defaultdict(lambda: [[] for _ in range(5)])
        for i in range(0, len(self.genes), 5):
            for hour_count in range(int(ceil(self.course_duration[self.genes[i].dna]))):
                if str(int(self.genes[i + 3].dna) + hour_count) in self.rooms[self.genes[i + 4].dna][
                    int(self.genes[i + 2].dna) - 1]:
                    self.is_valid = False
                if str(int(self.genes[i + 3].dna) + hour_count) in self.profs[self.genes[i + 1].dna][
                    int(self.genes[i + 2].dna) - 1]:
                    self.is_valid = False
                self.rooms[self.genes[i + 4].dna][int(self.genes[i + 2].dna) - 1].append(
                    str(int(self.genes[i + 3].dna) + hour_count))
                self.profs[self.genes[i + 1].dna][int(self.genes[i + 2].dna) - 1].append(
                    str(int(self.genes[i + 3].dna) + hour_count))
        return self.is_valid
