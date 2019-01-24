import numpy as np


class Node:
    def __init__(self, step_count, current_value, current_weight, selected_items: list):
        self.step_count = step_count
        self.current_value = current_value
        self.current_weight = current_weight
        self.selected_items = selected_items


def main():
    counter = 0
    max_weight, items = read_file('ks_100_997')
    optimal = 2397
    items_length = len(items)
    priority_list = list()
    priority_list.append(Node(0, 0, 0, []))
    while True:
        counter += 1
        # select best in list
        best_index = -1
        best_value = -1
        for i, node in enumerate(priority_list):
            if node.current_value + heuristic(node.current_value, optimal, max_weight) > best_value:
                best_value = node.current_value
                best_index = i
        best_node = priority_list[best_index]
        print("Max Value: " + str(best_node.current_value))
        print("Weight: " + str(best_node.current_weight))
        print("Depth: " + str(best_node.step_count))
        print("Counter:" + str(counter))
        print("Best Found: " + str(
            np.array([1 if i in best_node.selected_items else 0 for i in range(items_length)])))

        # check if it's goal
        if goal(best_node.selected_items, items, optimal, max_weight):
            break
        # delete and expand selected
        selected_before = best_node.selected_items
        for i in range(items_length):
            if i not in selected_before:
                selected_items = selected_before + [i]
                new_node_value = items[i][0] + best_node.current_value
                new_node_weight = best_node.current_weight + items[i][1]
                if new_node_weight <= max_weight:
                    priority_list.append(
                        Node(best_node.step_count + 1, new_node_value, new_node_weight, selected_items))
        priority_list.remove(best_node)

    print("Max Value: " + str(best_node.current_value))
    print("Weight: " + str(best_node.current_weight))
    print("Depth: " + str(best_node.step_count))
    print("Counter:" + str(counter))
    print("Best Solution Found: " + str(
        np.array([1 if i in best_node.selected_items else 0 for i in range(items_length)])))


def read_file(filename):
    items = list()
    max_weight = 0
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                max_weight = int(line.split()[1])
            else:
                # first value, second weight
                items.append(list(map(int, line.split())))
    return max_weight, items


def goal(selected_items: list, items: list, optimal_value: int, max_weight):
    cum_weight = 0
    cum_value = 0
    for i in selected_items:
        cum_value += items[i][0]  # value
        cum_weight += items[i][1]  # weight
    if optimal_value == cum_value and cum_weight <= max_weight:
        return True
    return False


def heuristic(g, optimal, max_weight):
    return abs(g - optimal) / max_weight


if __name__ == '__main__':
    main()
