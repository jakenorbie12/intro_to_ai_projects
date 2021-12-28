import sys
import csv
import queue

def main():
    # if invalid inputs are submitted
    if len(sys.argv) != 3:
        sys.exit("ERROR: Not enough or too many input arguments.")
    try:
        int(sys.argv[2])
    except:
        final_print(sys.argv[1],sys.argv[2],"FAILURE: INVALID PARK NUMBER","N/A","N/A","N/A")
        return

    #construction of global variables and main function variables
    global initial_state, min_parks, park_dict, zone_dict, state_guide, driving_list, goal_states
    (initial_state, min_parks) = (sys.argv[1],sys.argv[2])
    driving_list = []
    driving_list.append([])
    park_dict = {}
    zone_dict = {}

    # open driving csv and find rows. If inital state isn't in driving csv, return error
    with open('driving2.csv') as dcsv:
        d_reader = csv.reader(dcsv)
        state_guide = d_reader.__next__()
        for row in d_reader:
            driving_list.append(row)
    if initial_state not in state_guide:
        final_print(initial_state,min_parks,"FAILURE: INVALID INITIAL STATE","N/A","N/A","N/A")
        return
    #create park dictionary
    with open('parks.csv') as slcsv:
        p_reader = csv.reader(slcsv)
        p_guide = p_reader.__next__()
        park_row = p_reader.__next__()
        for i,park_num in enumerate(park_row[1:]):
            park_dict[p_guide[i+1]] = int(park_num)
    #create zone dictionary
    with open('zones.csv') as slcsv:
        z_reader = csv.reader(slcsv)
        z_guide = z_reader.__next__()
        st_index = z_guide.index(initial_state)
        zones_row = z_reader.__next__()
        for i,zone in enumerate(zones_row[1:]):
            if i+1 == st_index:
                initial_zone = int(zone)
            if zone not in zone_dict.keys():
                zone_dict[zone] = [z_guide[i+1]]
            else:
                zone_dict[zone].append(z_guide[i+1])
    #set goal_states to variable
    goal_states = zone_dict['12']


    final_results = constraint_search([initial_state], park_dict[initial_state], 0, initial_zone)
    if type(final_results[0]) != str:
        final_results[0] = list_to_str(final_results[0])
    final_print(final_results[0], final_results[1], final_results[2], final_results[3])


def constraint_search(state_path, curr_parks, curr_cost, curr_zone):
    #see if constraints are met, and if so return key values and True
    if curr_zone == 12 and curr_parks >= int(min_parks):
        return [state_path,len(state_path),curr_cost,curr_parks, True]
    #for each of the next_states...
    for state_node,dist in next_states(state_path[-1], str(curr_zone+1)):
        #find results of searching this state
        results = constraint_search(state_path+[state_node],curr_parks+park_dict[state_node],curr_cost+dist,curr_zone + 1)
        #if results are successful, return them
        if results[4]:
            return results
    #if all next_states have been investigated without success, return failure prompt and False
    return ["FAILURE: NO PATH FOUND", 0, 0, 0, False]

#defines valid next states
def next_states(state, zone):
    next_list = []
    for idx, next_dist in enumerate(driving_list[state_guide.index(state)][1:]):
        if int(next_dist) > 0 and state_guide[idx+1] in zone_dict[zone]:
            next_list.append((state_guide[idx+1],int(next_dist)))
    next_list.sort(reverse=True, key=lambda a : a[1])
    return next_list
        

#returns distance between two states
def state_to_state(start_state,end_state):
    return driving_list[state_guide.index(start_state)][state_guide.index(end_state)]

#makes list look pretty
def list_to_str(list):
    s = ""
    for value in list:
        s += value + ", "
    return s[:-2]

#final print statement converted to function for abstraction
def final_print(sol_path, num_states, path_cost, num_parks):
    print("\nNorbie, Jake A20459012 Solution:\nInitial state: " + initial_state + "\n" + "Minimum number of parks: " +
        min_parks + "\n\n" + "Solution Path: " + sol_path + "\nNumber of states on a path: " + str(num_states) +
        "\nPath Cost: " + str(path_cost) + "\nNumber of national parks visited: " + str(num_parks) + "\n")
    return

main()
