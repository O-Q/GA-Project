from functools import reduce

from numpy.random import choice

from ga.algorithms import BaseGeneticAlgorithm


def init_params(params_filename='params.txt') -> dict:
    params = dict()
    with open(params_filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            param = line.split()
            try:
                params[param[0]] = int(param[1])
            except ValueError:
                params[param[0]] = float(param[1])
    return params


def is_same_chromosomes(chromosomes):
    # consider it's sorted list
    current = chromosomes[0]
    for chromosome in chromosomes:
        if current.dna != chromosome.dna:
            return False
        current = chromosome
    return True


def evaluated_chromosomes(bga: BaseGeneticAlgorithm, chromosomes: list, big_better=True):
    values = list()
    cum_values = 0
    for chromosome in chromosomes:
        value = bga.eval_fitness(chromosome)
        cum_values += value
        values.append(value)

    if not big_better:
        inverse_values = list()
        cum_values = 0
        multiply_all = reduce(lambda x, y: x * y if (x and y) else 1, values)
        for value in values:
            new_value = multiply_all / value
            inverse_values.append(new_value)
            cum_values += new_value
        values = inverse_values
    selection = list()
    try:
        for i in range(len(chromosomes)):
            selection.append(values[i] / cum_values)
    except ZeroDivisionError:
        cum_values = len(values)
        for i in range(len(chromosomes)):
            selection.append(1 / cum_values)
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


def print_chromosomes(chromosomes):
    for chromosome in chromosomes:
        print(chromosome.dna)
    print()
