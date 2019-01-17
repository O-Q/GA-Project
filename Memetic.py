from numpy.random import choice


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
