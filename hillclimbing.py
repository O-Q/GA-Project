from ga.chromosomes import Chromosome
from myga import KnapSackGeneticAlgorithm, CSChromosome, ClassSchedulingGeneticAlgorithm, NameGene


class HillClimbing:
    def __init__(self, max_side_way, tabu_size, max_improve):
        self.max_sideWay = max_side_way
        self.tabu_size = tabu_size
        self.max_improve = max_improve

    def improve(self, solution, **kwargs):
        pass


class HillClimbingKnapSack(HillClimbing):
    def __init__(self, max_side_way, tabu_size, max_improve, ksga: KnapSackGeneticAlgorithm):
        super().__init__(max_side_way, tabu_size, max_improve)
        self.ksga = ksga

    def improve(self, chromosome: Chromosome, is_binary=True):
        if is_binary:
            improve_count = 0
            tabu = list()
            max_chromosome = chromosome.copy()
            max_value = self.ksga.eval_fitness(max_chromosome)
            while True:
                last_step_max_chromosome = max_chromosome.copy()
                last_step_max_value = self.ksga.eval_fitness(last_step_max_chromosome)
                index_changed = -1
                # choose steepest ascent between neighbors
                for i, gene in enumerate(max_chromosome.dna):
                    copied_chromosome = max_chromosome.copy()
                    if gene == '0':
                        copied_chromosome.dna = copied_chromosome.dna[0:i] + '1' + copied_chromosome.dna[i + 1:]
                    else:
                        copied_chromosome.dna = copied_chromosome.dna[0:i] + '0' + copied_chromosome.dna[i + 1:]
                    value = self.ksga.eval_fitness(copied_chromosome)
                    if value > last_step_max_value:
                        last_step_max_chromosome = copied_chromosome
                        last_step_max_value = value
                        index_changed = i
                    elif last_step_max_value == max_value == value and not tabu.count(i):  # plateau
                        last_step_max_chromosome = copied_chromosome
                        index_changed = i
                if index_changed == -1:  # NOT found neighbor to go
                    return max_chromosome
                else:  # found neighbors to go
                    max_chromosome = last_step_max_chromosome
                    improve_count += 1
                    if improve_count == self.max_improve:  # enough improve
                        return max_chromosome
                    if last_step_max_value == max_value:  # side way move
                        if self.tabu_size < len(tabu) + 1:  # tabu size limit's reached
                            return max_chromosome
                        else:
                            tabu.append(index_changed)
                    else:  # not side way move. so we can clear tabu
                        tabu.clear()
                        max_value = last_step_max_value


class HillClimbingClassScheduling(HillClimbing):
    def __init__(self, max_side_way, tabu_size, max_improve, csga: ClassSchedulingGeneticAlgorithm):
        super().__init__(max_side_way, tabu_size, max_improve)
        self.csga = csga

    def improve(self, chromosome: CSChromosome, **kwargs):
        improve_count = 0
        tabu = list()
        min_chromosome = chromosome.copy()
        min_value = self.csga.eval_fitness(min_chromosome)
        while True:
            last_step_min_chromosome = min_chromosome.copy()
            last_step_min_value = self.csga.eval_fitness(last_step_min_chromosome)
            index_changed = -1
            # choose steepest ascent between neighbors
            for i, gene in enumerate(min_chromosome.genes):
                copied_chromosome = min_chromosome.copy()
                if gene.name == 'prof':
                    for prof in gene.compare_to:
                        copied_chromosome.genes[i].dna = prof
                        copied_chromosome.update_tables()
                        if copied_chromosome.is_valid:
                            value = self.csga.eval_fitness(copied_chromosome)
                            if value < last_step_min_value:
                                last_step_min_value = value
                                last_step_min_chromosome = copied_chromosome
                                index_changed = i
                elif gene.name == 'room':
                    for room in gene.compare_to:
                        copied_chromosome.genes[i].dna = room
                        copied_chromosome.update_tables()
                        if copied_chromosome.is_valid:
                            value = self.csga.eval_fitness(copied_chromosome)
                            if value < last_step_min_value:
                                last_step_min_value = value
                                last_step_min_chromosome = copied_chromosome
                                index_changed = i
                elif gene.name == 'day':
                    for day in [1, 2, 3, 4, 5]:
                        copied_chromosome.genes[i].dna = str(day)
                        copied_chromosome.update_tables()
                        if copied_chromosome.is_valid:
                            value = self.csga.eval_fitness(copied_chromosome)
                            if value < last_step_min_value:
                                last_step_min_value = value
                                last_step_min_chromosome = copied_chromosome
                                index_changed = i
                elif gene.name == 'hour':
                    for hour in range(gene.timespan[0], gene.timespan[1]):
                        copied_chromosome.genes[i].dna = str(hour)
                        copied_chromosome.update_tables()
                        if copied_chromosome.is_valid:
                            value = self.csga.eval_fitness(copied_chromosome)
                            if value < last_step_min_value:
                                last_step_min_value = value
                                last_step_min_chromosome = copied_chromosome
                                index_changed = i
            if index_changed == -1:
                return min_chromosome
            else:
                min_chromosome = last_step_min_chromosome
                improve_count += 1
                if improve_count == self.max_improve:  # enough improve
                    return min_chromosome
                if last_step_min_value == min_value:  # side way move
                    if self.tabu_size < len(tabu) + 1:  # tabu size limit's reached
                        return min_chromosome
                    else:
                        tabu.append(index_changed)
                else:  # not side way move. so we can clear tabu
                    tabu.clear()
                    min_value = last_step_min_value
