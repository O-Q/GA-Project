from numpy.random import choice

from ga.chromosomes import Chromosome
from ga.genes import BinaryGene

from myga import KnapSackGeneticAlgorithm
from hillclimbing import HillClimbing


# from Solid.StochasticHillClimb import StochasticHillClimb


def hill_climbing_improve(offspring_after_mutation, ksga, max_improve, max_side_way, tabu_size):
    hc = HillClimbing(max_side_way, tabu_size, max_improve, ksga)
    offspring_hill_climbed = list()
    for child in offspring_after_mutation:
        offspring_hill_climbed.append(hc.improve(child))
    return offspring_hill_climbed


def main():
    params = dict()
    # get params from file
    init_params(params)
    filename = 'ks_20_878'
    # create first PopSize chromosome with gene length IndivSize
    chromosomes = Chromosome.create_random(gene_length=params['IndivSize'], n=params['PopSize'], gene_class=BinaryGene)
    parent_count = int(params['ParentPercent'] * params['PopSize'])
    mga = KnapSackGeneticAlgorithm(chromosomes, filename)
    selection = evaluated_chromosomes(mga, chromosomes)
    selected_parents = select_parents(chromosomes, selection, parent_count)
    offspring = mga.reproduce(selected_parents, params['CrossoverProb'], n_point_crossover=2)
    offspring_after_mutation = mutate_offspring(offspring, params['MutationProb'])
    hill_climbed_offspring = hill_climbing_improve(offspring_after_mutation, mga, params['MaxImprove'],
                                                   params['MaxSideway'], params['TabuSize'])
    chromosomes_with_offspring = chromosomes + hill_climbed_offspring
    selection_with_offspring = evaluated_chromosomes(mga, chromosomes_with_offspring)
    sorted_chromosomes_with_offspring = sort_list_with_another_list(chromosomes_with_offspring,
                                                                    selection_with_offspring)
    print(selection_with_offspring)
    best_with_offspring = sorted_chromosomes_with_offspring[:params['PopSize']]
    print(best_with_offspring[0].dna)


def init_params(params):
    with open('params.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            param = line.split()
            try:
                params[param[0]] = int(param[1])
            except ValueError:
                params[param[0]] = float(param[1])


def evaluated_chromosomes(mga: KnapSackGeneticAlgorithm, chromosomes: list):
    # return sorted chromosome based on fitness function and selection that is prob based on fitness value
    ## doing like above doesn't need sorting
    values = list()
    cum_values = 0
    for chromosome in chromosomes:
        value = mga.eval_fitness(chromosome)
        cum_values += value
        values.append(value)
    # sorted_values = sorted(values.items(), key=lambda kv: kv[1], reverse=True)
    selection = list()
    for i in range(len(chromosomes)):
        selection.append(values[i] / cum_values)
    # no prob considered. just most valuables
    return selection


def select_parents(chromosomes, selections, parent_count):
    """
    It chooses n(parent_count) parents from chromosomes with probability(selections)
    :return: chosen parents
    """
    parents = choice(chromosomes, parent_count, p=selections)
    return parents


def mutate_offspring(offspring: list, p_mutate: float):
    """
    mutate after offspring with probability
    :param offspring: chromosomes that newly generated
    :param p_mutate: probability for each gene to mutate
    :return: chromosomes after mutation
    """
    for child in offspring:
        child.mutate(p_mutate)
    return offspring


def sort_list_with_another_list(the_list, another_list):
    return [x for x, _ in sorted(zip(the_list, another_list), reverse=True, key=lambda item: item[1])]


main()
