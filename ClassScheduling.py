# CPTR Presentation
# each chromosome has 4 value integers
# C: Class
# P: Professor
# D: Day of week
# H: Hour
# R: Room
from Memetic import init_params, is_same_chromosomes, evaluated_chromosomes, select_parents
from myga import ClassSchedulingGeneticAlgorithm


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
                                                                            course_room)
    parent_count = int(params['ParentPercent'] * params['PopSize'])
    max_gen = params['MaxGen']
    gen_count = 0
    first = True
    while gen_count < max_gen and (first or not is_same_chromosomes(chromosomes)):
        first = False
        csga = ClassSchedulingGeneticAlgorithm(chromosomes, seperates)
        selection = evaluated_chromosomes(csga, chromosomes)
        selected_parents = select_parents(chromosomes, selection, parent_count)
        gen_count += 1
        print(gen_count)

    for chromosome in chromosomes:
        print(chromosome.dna)


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
                    try:
                        param[0] = param[0].replace("'", '')
                        times[param[0]] = float(param[1])
                    except IndexError:
                        times[param[0]] = 2
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
    return courses, profs, times, rooms, span, seperates


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
    return [x for x, _ in sorted(zip(the_list, another_list), reverse=False, key=lambda item: item[1])]


if __name__ == '__main__':
    __main__()
