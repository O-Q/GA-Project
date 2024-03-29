# CPTR Presentation
# each chromosome has 4 value integers
# C: Class
# P: Professor
# D: Day of week
# H: Hour
# R: Room
from Memetic import init_params, is_same_chromosomes, evaluated_chromosomes, select_parents, mutate_offspring
from hillclimbing import HillClimbingClassScheduling
from myga import ClassSchedulingGeneticAlgorithm, CSChromosome

WEEK = {1: 'Sat', 2: 'Sun', 3: 'Mon', 4: 'Tue', 5: 'Wed', 6: 'Tur', 7: 'Fri'}


def __main__():
    courses, profs, times, rooms, span, seperates = init_csp('cs.txt')
    params = init_params()
    courses_list = list(courses.keys())
    course_prof = get_course_prof(profs)
    course_room = get_course_room(courses, rooms)
    print(courses)
    print(profs)
    print(times)
    print(rooms)
    print(span)
    print(seperates)
    print(course_prof)
    print(course_room)
    chromosomes = ClassSchedulingGeneticAlgorithm.create_random_chromosomes(params['PopSize'], courses_list,
                                                                            course_prof, span,
                                                                            course_room, times)
    parent_count = int(params['ParentPercent'] * params['PopSize'])
    max_gen = params['MaxGen']
    gen_count = 0
    first = True
    while gen_count < max_gen and (first or not is_same_chromosomes(chromosomes)):
        first = False
        csga = ClassSchedulingGeneticAlgorithm(chromosomes, seperates)
        selection = evaluated_chromosomes(csga, chromosomes, big_better=False)
        selected_parents = select_parents(chromosomes, selection, parent_count)
        offspring = csga.reproduce(selected_parents, params['CrossoverProb'])
        offspring_after_mutation = mutate_offspring(offspring, params['MutationProb'])
        hill_climbed_offspring = hill_climbing_improve(offspring_after_mutation, csga, params['MaxImprove'],
                                                       params['MaxSideway'], params['TabuSize'])
        chromosomes_with_offspring = chromosomes + hill_climbed_offspring
        selection_with_offspring = evaluated_chromosomes(csga, chromosomes_with_offspring, big_better=False)
        sorted_chromosomes_with_offspring = sort_list_with_another_list(chromosomes_with_offspring,
                                                                        selection_with_offspring)
        chromosomes = sorted_chromosomes_with_offspring[:params['PopSize']]
        gen_count += 1
        print('Generation: ' + str(gen_count))
        print('Best in this generation: ' + chromosomes[0].dna)
        print('Best score: ' + str(csga.eval_fitness(chromosomes[0])))
    print('END Generation: ' + str(gen_count))
    print('Best Solution Found: ')
    print_solution(chromosomes[0])
    print('Min Value:' + str(csga.eval_fitness(chromosomes[0])))


def init_csp(params_filename='params.txt'):
    courses = dict()
    profs = dict()
    times = dict()
    rooms = dict()
    span = list()
    seperates = list()
    current_cat = str()
    with open(params_filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line[0] == '#':
                current_cat = line.strip()[1:]
                continue
            elif not current_cat:
                raise IOError
            else:
                if current_cat == 'Course':
                    param = line.strip().split("' ")
                    try:
                        param[0] = param[0].replace("'", '')
                        courses[param[0]] = int(param[1])
                    except IndexError:
                        courses[param[0]] = 30
                elif current_cat == 'Prof':
                    param = line.strip().split("' ")
                    for i in range(len(param)):
                        param[i] = param[i].replace("'", '')
                    profs[param[0]] = [course for course in param[1:]]
                elif current_cat == 'Time':
                    param = line.strip().split("' ")
                    param[0] = param[0].replace("'", '')
                    times[param[0]] = float(param[1])
                elif current_cat == 'Room':
                    param = line.strip().split("' ")
                    try:
                        param[0] = param[0].replace("'", '')
                        rooms[param[0]] = int(param[1])
                    except IndexError:
                        rooms[param[0]] = 35
                elif current_cat == 'Span':
                    param = line.strip().split()
                    span.append(int(param[0]))
                    span.append(int(param[1]))
                elif current_cat == 'Separate':
                    param = line.strip().split("' ")
                    for i in range(len(param)):
                        param[i] = param[i].replace("'", '')
                    seperates.append([course for course in param])
    if not span:
        span.append(8)
        span.append(16)
    for course in courses:
        if not times.get(course):
            times[course] = 2
    return courses, profs, times, rooms, span, seperates


def hill_climbing_improve(offspring_after_mutation, csga, max_improve, max_side_way, tabu_size):
    hc = HillClimbingClassScheduling(max_side_way, tabu_size, max_improve, csga)
    offspring_hill_climbed = list()
    for child in offspring_after_mutation:
        offspring_hill_climbed.append(hc.improve(child))
    return offspring_hill_climbed


def get_course_prof(profs: dict) -> dict:
    """
    :param profs: dict key: prof and value: course
    :return: return a dict that key is course and value is profs can teach the course
    """
    course_prof = dict()
    for prof in profs.keys():
        for course in profs[prof]:
            if course_prof.get(course):
                course_prof[course].append(prof)
            else:
                course_prof[course] = [prof]
    return course_prof


def get_course_room(courses, rooms):
    """
    :param courses: dict that key is course and value is number of students
    :param rooms: dict that key is name of room and value is capacity
    :return: dict that key is course and value is rooms that fits to course and its student
    """
    course_room = dict()
    for course in courses.keys():
        for room in rooms.keys():
            if courses[course] <= rooms[room]:
                if course_room.get(course):
                    course_room[course].append(room)
                else:
                    course_room[course] = [room]
    return course_room


def sort_list_with_another_list(the_list, another_list):
    return [x for x, _ in sorted(zip(the_list, another_list), reverse=True, key=lambda item: item[1])]


def print_solution(chromosome: CSChromosome):
    for i in range(0, len(chromosome.genes), 5):
        print('Course: ' + chromosome.genes[i].dna)
        print('Professor: ' + chromosome.genes[i + 1].dna)
        print('Class: ' + chromosome.genes[i + 4].dna)
        print(WEEK[int(chromosome.genes[i + 2].dna)] + ' ' + chromosome.genes[i + 3].dna)
        print('----------')


if __name__ == '__main__':
    __main__()
