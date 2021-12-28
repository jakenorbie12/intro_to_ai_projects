import sys
import time
import csv
import queue

def main():
    if len(sys.argv) != 3:
        sys.exit("ERROR: Not enough or too many input arguments.")

    (initial, goal) = sys.argv[1:]
    global state_guide
    global driving_list
    driving_list = []
    driving_list.append([])
    global straight_list
    straight_list = []
    global goal_list

    with open('driving.csv') as dcsv:
        d_reader = csv.reader(dcsv)
        state_guide = d_reader.__next__()
        for row in d_reader:
            driving_list.append(row)
    with open('straightline.csv') as slcsv:
        sl_reader = csv.reader(slcsv)
        sl_reader.__next__()
        for row in sl_reader:
            straight_list.append(row)

    if initial not in state_guide or goal not in state_guide:
        print("\nNorbie, Jake A20459012 Solution:\nInitial state: " + initial + "\nGoal state: " + goal + "\n")
        print("Greedy Best First Search:\nSolution Path: [NOT FOUND]" + "\nNumber of states on a path: N/A" + 
            "\nPath Cost: N/A" + "\nExecution Time: N/A" + "\n")
        print("A* Search:\nSolution Path: [NOT FOUND]" + "\nNumber of states on a path: N/A" + 
            "\nPath Cost: N/A" + "\nExecution Time: N/A" + "\n")
        return
    goal_list = straight_list[state_guide.index(goal) - 1]


    greedy_start_time = time.time()
    greedy_results = best_first_search(Node(initial, "None", 0, 0), goal, queue.PriorityQueue(), {}, "greedy")
    greedy_time = time.time() - greedy_start_time
    a_star_start_time = time.time()
    a_star_results = best_first_search(Node(initial, "None", 0, 0), goal, queue.PriorityQueue(), {}, "a*")
    a_star_time = time.time() - a_star_start_time
    print("\nNorbie, Jake A20459012 Solution:\nInitial state: " + initial + "\nGoal state: " + goal + "\n")
    print("Greedy Best First Search:\nSolution Path: " + str(greedy_results[0]) + "\nNumber of states on a path: " + str(greedy_results[1]) + 
            "\nPath Cost: " + str(greedy_results[2]) + "\nExecution Time: " + str(greedy_time) + "\n")
    print("A* Search:\nSolution Path: " + str(a_star_results[0]) + "\nNumber of states on a path: " + str(a_star_results[1]) + 
            "\nPath Cost: " + str(a_star_results[2]) + "\nExecution Time: " + str(a_star_time))



def best_first_search(current, goal, frontier, visited, metric):
    if current.getState() == goal:
        visited[current.getParent()] = (current.getState(), current.getPathCost())
        final_results = dict_to_list(visited, "None")
        return [final_results[0], len(final_results[0]), final_results[1]]
    visited[current.getParent()] = (current.getState(), current.getPathCost())
    new_frontier = expand(current, frontier, visited, metric)
    if new_frontier.empty():
        return ["FAILURE: NO PATH FOUND", 0, 0]
    temp = new_frontier.get()
    print(temp.getParent(), temp.getState())
    new_curr = closer(temp, visited, frontier)
    print(new_curr.getParent(), new_curr.getState())
    return best_first_search(new_curr, goal, new_frontier, visited, metric)

def expand(curr_node, fr_nodes, v_nodes, metric):
    for idx, state in enumerate(driving_list[state_guide.index(curr_node.getState())]):
        if state.isnumeric():
            distance = int(state)
            s = state_guide[idx]
            g = int(goal_list[idx])
            if curr_node.getState() in v_nodes.keys():
                break
            if distance > 0 and s not in v_nodes.keys():
                if metric == "greedy":
                    print(s, curr_node.getState(), distance, g)
                    fr_nodes.put(Node(s, curr_node.getState(), distance, g))
                else:
                    print(s, curr_node.getState(), distance, distance + g)
                    fr_nodes.put(Node(s, curr_node.getState(), distance, distance + g))         
    return fr_nodes

def dict_to_list(dict, i):
    final_list = []
    indicator = i
    total_cost = 0
    while indicator in dict.keys():
        final_list.append(dict[indicator][0])
        total_cost += int(dict[indicator][1])
        indicator = dict[indicator][0]
    return (final_list, total_cost)

#at some point, pop off all frontier nodes with a shorter cost than the "to-be-added", and if the path is shorter than dict_to_list distance, don't add
def closer(state, v_nodes, fr_nodes):
    v_nodes[state.getParent()] = state.getState()
    temp_list = []
    while not fr_nodes.empty():
        potential = fr_nodes.get()
        temp_list.append(potential)
        print(potential.getParent(), potential.getState())
        if potential.getPathCost() > dict_to_list(v_nodes, state)[1]:
            break
        if potential.getState() == state and potential.getParent() in v_nodes.keys():
            return potential
    for node in temp_list:
        fr_nodes.put(node)
    return state

class Node:
    def __init__(self, state, parent, pathCost, cost):
        self.state = state
        self.parent = parent
        self.pathCost = pathCost
        self.cost = cost

    def getState(self):
        return self.state
    
    def getParent(self):
        return self.parent

    def getPathCost(self):
        return self.pathCost

    def getCost(self):
        return self.cost

    def __lt__(self, other):
        return self.getCost() < other.getCost()

main()