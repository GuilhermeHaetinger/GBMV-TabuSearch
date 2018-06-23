from vertex_group import vertex_group as Group
from graph import graph as Graph
from random import randint
from random import uniform
import sys
import time

ELEMENT_NOT_IN_GROUP     = -3
ELEMENT_ALREADY_IN_GROUP = -2
FAILED                   = -1
SUCCEEDED                =  0
'''
Parses an input line ignoring the carriage return

Params:
    line(string) : line to parse

returns:
    line's values that were separated by a blank space, ignoring carriage return (List(string))

'''
def line_parsing(line):
    return line.replace(" \n", "").split(" ")

'''
Reads an instance of the GBMV problem, creating, initializing (even randomly) and attributing the right values 

Params:
    file(File) : instance file

returns:
    graph(Graph)               : instantiated graph
    groups(List(vertex_group)) : instantiated groups in a list, or 
    num_of_vertices(int)       : number of vertices for further operations
    *in this respective order*

'''
def read_instance_file(file):    
    num_of_vertices, num_of_groups = line_parsing(file.next())
    num_of_vertices                = int(num_of_vertices)
    num_of_groups                  = int(num_of_groups)

    bound_line   = line_parsing(file.next())
    bound_count  = 0
    group_bounds = []

    while(bound_count < num_of_groups):
        group_bounds.append([int(bound_line[bound_count*2]), int(bound_line[bound_count*2 + 1])])
        bound_count += 1 

    weight_line    = line_parsing(file.next())
    vertex_weights = []

    for i in range(0, num_of_vertices):
        vertex_weights.append(int(weight_line[i]))
        if vertex_weights[i] < 0:
            exit("NEGATIVE VERTEX FOUND!!!")

    graph_dict = dict()

    for line in file:
        edge_line                       = line.replace("\n", "").split(" ")
        
        origin                          = int(edge_line[0])
        destination                     = int(edge_line[1])
        value                           = float(edge_line[2])
        
        graph_dict[origin, destination] = value


    graph  = Graph(num_of_vertices, graph_dict, vertex_weights)
    groups = initialize_groups_randomly(num_of_groups, num_of_vertices, group_bounds, graph)

    return graph, groups, num_of_vertices

'''
Calculates the problem's solution value

Params:
    graph(Graph)                       : graph with the required values
    list_of_groups(List(vertex_group)) : problem solution

returns:
    solution's value (int)

'''
def get_instance_value(list_of_groups, graph):
    instance_value = 0
    for group in list_of_groups:
        instance_value += group.get_group_value(graph)

    return instance_value

'''
Gets two random diferent groups from the problem's solution

Params:
    list_of_groups(List(vertex_group)) : problem solution

returns:
    group1 index (int)
    group2 index (int)

'''
def get_random_group_indexes(list_of_groups):
    rand_remove_index = randint(0, len(list_of_groups)-1)
    rand_add_index    = randint(0, len(list_of_groups)-1)

    while rand_add_index == rand_remove_index:
        rand_add_index = randint(0, len(list_of_groups)-1)

    return [rand_remove_index, rand_add_index]

'''
fills a given group with available vertices until it hits the lower limit of weights

Params:
    group(vertex_group)        : group to fill
    unused_vertices(List(int)) : available vertices
    graph(Graph)               : Graph with the required values for weight validation 

returns:
    filled group (vertex_group)

'''
def fill_group_randomly(group, unused_vertices, graph):
    while(group.min_bound > group.get_group_value(graph)):
        rand_vertice = randint(0, len(unused_vertices)-1)
        group.group_vertices.append(unused_vertices[rand_vertice])
        unused_vertices.pop(rand_vertice)

    return group

'''
Creates a valid first solution randomly

Params:
    num_of_groups(int)   : number of groups for the problem instance
    num_of_vertices(int) : number of vertices for the problem instance
    list_of_boundaries(List(int)) : boundaries for each group in the format [group1Lower, group1Higher, group2Lower, group2Higher, ...]
    graph(Graph)               : Graph with the required values for weight validation 

returns:
    filled group (vertex_group)

'''
def initialize_groups_randomly(num_of_groups, num_of_vertices, list_of_boundaries, graph):
    list_of_groups = []
    for i in range(0, num_of_groups):
        list_of_groups.append(Group(list_of_boundaries[i][0], list_of_boundaries[i][1], []))

    unused_vertices = []
    for i in range(0, num_of_vertices):
        unused_vertices.append(i)
    
    for i in range(0, num_of_groups):
        list_of_groups[i] = fill_group_randomly(list_of_groups[i], unused_vertices, graph)

    for i in unused_vertices:
        randGroup = randint(0, num_of_groups-1)
        while(list_of_groups[randGroup].add_element(i, graph) != SUCCEEDED):
            randGroup = randint(0, num_of_groups-1)
       

    return list_of_groups

'''
Executes a change on the solution, changing an element from a group to another

Params:
    list_of_groups(List(vertex_group)) : actual solution
    add_group_index(int)               : index for the group in which the element will be added
    remove_group_index(int)            : index for the group in which the element will be removed
    element(int)                       : element in transition
    graph(Graph)                       : Graph with the required values for weight validation 

returns:
    solution with the executed changes

'''
def set_random_neighbor(list_of_groups, add_group_index, remove_group_index, element, graph): 
    new_group_list = list_of_groups[:]

    group_removed  = new_group_list[remove_group_index].copy()
    group_added    = new_group_list[add_group_index].copy()

    if group_removed.remove_element(element, graph) != SUCCEEDED:
        return new_group_list
    
    if group_added.add_element(element, graph) != SUCCEEDED:
        return new_group_list

    new_group_list[remove_group_index] = group_removed
    new_group_list[add_group_index]    = group_added

    return new_group_list

'''
Runs TS with imediate neighbors

Params:
    groups(List(vertex_group)) : initial solution
    graph(Graph)               : Graph with the required values for weight validation 
    num_of_iterations(int)     : wanted number of iterations
    max_tabu_size(int)         : tabu movements list limiter
    tabu_prob(float)           : probability to be added in tabu movements list
    file_to_write(File)        : file in which the results will be written

returns:
    final solution (List(vertex_groups))

'''
def run_simple_tabu_search(groups, graph, num_of_iterations, max_tabu_size, tabu_prob, file_to_write):

    actual_instance = groups[:]
    actual_value    = get_instance_value(actual_instance, graph)
    tabu_movements  = []
    best_solution_found = 0

    #for every iteration
    for i in range(0, num_of_iterations):

        best_neighbor_solution = 0
        best_neighbor          = None
        best_tabu_movement     = None
        new_group_list = actual_instance[:]
        rand_group, rand_add = get_random_group_indexes(new_group_list) #rand_add wont be used because we will execute for every group available
        element = new_group_list[rand_group].get_random_element()

        #for every group available to send the element
        for j in range(0, len(new_group_list)):
            
            if element not in tabu_movements:
                if j != rand_group:
                    new_group_list = set_random_neighbor(new_group_list, j, rand_group, element, graph)
            
            new_instance_value = get_instance_value(new_group_list, graph)

            if new_instance_value > best_neighbor_solution:
                best_neighbor          = new_group_list
                best_neighbor_solution = new_instance_value
                best_tabu_movement     = element

        if uniform(0, 1) <= tabu_prob:
            tabu_movements.append(element)

        if best_neighbor_solution > 0:
            if len(tabu_movements) == max_tabu_size:
                del tabu_movements[0:len(tabu_movements)]

            tabu_movements.append(best_tabu_movement)
            actual_instance = best_neighbor
            actual_value    = best_neighbor_solution

            if actual_value > best_solution_found:
                best_solution_found  = actual_value
                best_found           = actual_instance


    file_to_write.write(str(best_solution_found) + ","  + str(actual_value) + "\n")
    return groups

'''
Executes a change on the solution, changing an element from a group to another as well as treating tabu conditions

Params:
    groups(List(vertex_group))    : actual solution
    tabu_prob(float)              : probability to add element in tabu list
    graph(Graph)                  : Graph with the required values for weight validation 
    new_tabu_movements(List(int)) : list of TO BE ADDED tabus
    tabu_movements(List(int))     : actual tabu movements

returns:
    solution with the executed changes

'''
def execute_shift(groups, tabu_prob, graph, new_tabu_movements, tabu_movements):
    rand_remove, rand_add = get_random_group_indexes(groups)
    element = groups[rand_remove].get_random_element()
    if element not in tabu_movements:
        if tabu_prob >= 0:
            if uniform(0, 1) <= tabu_prob :
                new_tabu_movements.append(element)
        groups = set_random_neighbor(groups, rand_add, rand_remove, element, graph)
    return groups


'''
Runs TS with "Big-Step" neighbors

Params:
    groups(List(vertex_group)) : initial solution
    graph(Graph)               : Graph with the required values for weight validation 
    num_of_iterations(int)     : wanted number of iterations
    num_of_neighbors(int)      : wanted number of neighbors to compare
    num_of_elements(int)       : wanted number of shifts in a neighbor execution
    max_tabu_size(int)         : tabu movements list limiter
    tabu_prob(float)           : probability to be added in tabu movements list
    file_to_write(File)        : file in which the results will be written

returns:
    final solution (List(vertex_groups))

'''

def run_big_step_tabu_search(groups, graph, num_of_iterations, num_of_neighbors, num_of_elements, max_tabu_size, tabu_prob, file_to_write):
    
    actual_instance = groups[:]
    actual_value    = get_instance_value(actual_instance, graph)
    tabu_movements  = []
    best_solution_found = 0
    best_found = None

    # for every iteration
    for i in range(0, num_of_iterations):
        best_neighbor_solution = 0
        best_neighbor          = None
        best_tabu_movement     = None
    # for every neighbor 
        for j in range(0, num_of_neighbors):
            new_tabu_movements = []
            new_group_list = actual_instance[:]
    # for every shift
            for k in range(0, num_of_elements):
                new_group_list = execute_shift(new_group_list, tabu_prob, graph, new_tabu_movements, tabu_movements)
            neighbor_value = get_instance_value(new_group_list, graph)

            #if the new value is higher, we shoul make it the best neighbor
            if neighbor_value > best_neighbor_solution:
                best_neighbor          = new_group_list
                best_neighbor_solution = neighbor_value
                best_tabu_movement     = new_tabu_movements

        # if the best neighbor is valid
        if best_neighbor_solution > 0:
            #if the tabu list exceeds its maximum size we should erase it completely
            if len(tabu_movements) == max_tabu_size:
                del tabu_movements[0:len(tabu_movements)]
            #exchange the actual values
            tabu_movements.append(best_tabu_movement)
            actual_instance = best_neighbor
            actual_value    = best_neighbor_solution
            #exchange the best value found if needed
            if actual_value >= best_solution_found:
                best_solution_found  = actual_value
                best_found           = actual_instance

    #write the result
    if file_to_write != None:
        file_to_write.write(str(best_solution_found) + ","  + str(actual_value) + "\n")
    return best_found