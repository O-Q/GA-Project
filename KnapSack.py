from Memetic import init_params, is_same_chromosomes, select_parents, evaluated_chromosomes, mutate_offspring
from ga.chromosomes import Chromosome
from ga.genes import BinaryGene

from myga import KnapSackGeneticAlgorithm
from hillclimbing import HillClimbingKnapSack
import numpy as np


def main():
    # get params from file
    params = init_params('params2.txt')
    # filename = 'ks_20_878'
    filename = 'ks_100_997'  # params2.txt
    # filename = 'ks_200_1008'  # params3.txt
    # create first PopSize chromosome with gene length IndivSize
    chromosomes = Chromosome.create_random(gene_length=np.ones(params['IndivSize'], dtype='int32'), n=params['PopSize'],
                                           gene_class=BinaryGene, binary_zero_prob=.9)

    parent_count = int(params['ParentPercent'] * params['PopSize'])
    max_gen = params['MaxGen']
    gen_count = 0
    first = True
    ksga = KnapSackGeneticAlgorithm(chromosomes, filename)
    hc = HillClimbingKnapSack(params['MaxSideway'], params['TabuSize'], params['MaxImprove'], ksga)
    while gen_count < max_gen and (first or not is_same_chromosomes(chromosomes)):
        first = False
        selection = evaluated_chromosomes(ksga, chromosomes)
        selected_parents = select_parents(chromosomes, selection, parent_count)
        offspring = ksga.reproduce(selected_parents, params['CrossoverProb'], n_point_crossover=2)
        offspring_after_mutation = mutate_offspring(offspring, params['MutationProb'])
        hill_climbed_offspring = hill_climbing_improve(offspring_after_mutation, hc)
        chromosomes_with_offspring = chromosomes + hill_climbed_offspring
        selection_with_offspring = evaluated_chromosomes(ksga, chromosomes_with_offspring)
        sorted_chromosomes_with_offspring = sort_list_with_another_list(chromosomes_with_offspring,
                                                                        selection_with_offspring)
        chromosomes = sorted_chromosomes_with_offspring[:params['PopSize']]
        gen_count += 1
        print('Generation: ' + str(gen_count))
        print('Best in this generation: ' + chromosomes[0].dna)
        print('Best score: ' + str(ksga.eval_fitness(chromosomes[0])))
        cum_score = 0
        for i in range(params['PopSize']):
            cum_score += ksga.eval_fitness(chromosomes[i])
        average_score = str(cum_score / params['PopSize'])
        print('Average Score: ' + average_score)
    print('END Generation: ' + str(gen_count))
    print('Best Solution Found: ' + chromosomes[0].dna)
    print('Max Value:' + str(ksga.eval_fitness(chromosomes[0])))


def hill_climbing_improve(offspring_after_mutation, hc):
    offspring_hill_climbed = list()
    for child in offspring_after_mutation:
        offspring_hill_climbed.append(hc.improve(child))
    return offspring_hill_climbed


def sort_list_with_another_list(the_list, another_list):
    return [x for x, _ in sorted(zip(the_list, another_list), reverse=True, key=lambda item: item[1])]


if __name__ == '__main__':
    main()
