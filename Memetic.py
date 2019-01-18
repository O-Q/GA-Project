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


def evaluated_chromosomes(bga: BaseGeneticAlgorithm, chromosomes: list):
    values = list()
    cum_values = 0
    for chromosome in chromosomes:
        value = bga.eval_fitness(chromosome)
        cum_values += value
        values.append(value)
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


def print_chromosomes(chromosomes):
    for chromosome in chromosomes:
        print(chromosome.dna)
    print()
