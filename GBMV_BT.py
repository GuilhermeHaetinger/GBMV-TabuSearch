from vertex_group import vertex_group as Group
from graph import graph as Graph
import random
import sys

ELEMENT_NOT_IN_GROUP     = -3
ELEMENT_ALREADY_IN_GROUP = -2
FAILED                   = -1
SUCCEEDED                =  0

#NAO SEI SE UTILIZAR
class tabu_movement:
    def __init__(self, remove_group_index, element):
        self.remove_group_index = remove_group_index
        self.element = element

def line_parsing(line):
    return line.replace(" \n", "").split(" ")

def initialize_groups_randomly(num_of_groups, num_of_vertices, list_of_boundaries):
    while True:
        vertices_per_groups    = num_of_vertices/num_of_groups
        list_of_group_vertices = []

        for i in range(0, num_of_groups):
            list_of_group_vertices.append([])
        
        for i in range(0, num_of_vertices):
            rand_group = random.randint(0, num_of_groups-1)
            while(len(list_of_group_vertices[rand_group]) == vertices_per_groups):
                rand_group = random.randint(0, num_of_groups-1)

            list_of_group_vertices[rand_group].append(i)

        groups = []

        for i in range(0, num_of_groups):
            min      = list_of_boundaries[i][0]
            max      = list_of_boundaries[i][1]
            vertices = list_of_group_vertices[i]
            group    = Group(min, max, vertices)
            groups.append(group)

        should_groups_be_published = True

        for group in groups:
            if not group.check_initial_consistency:
                should_groups_be_published = False
                break

        if should_groups_be_published:
            return groups

def initialize_groups_in_order(num_of_groups, num_of_vertices, list_of_boundaries):
    vertices_per_groups    = num_of_vertices/num_of_groups
    list_of_group_vertices = []
    group_vertices_buffer  = []
    division_buffer        = 0

    for i in range(0, num_of_vertices+1):
        if division_buffer + 1 == i / vertices_per_groups:
            division_buffer      += 1
            list_of_group_vertices.append(group_vertices_buffer)
            group_vertices_buffer = []

        group_vertices_buffer.append(i)
    
    groups = []

    for i in range(0, num_of_groups):
        min      = list_of_boundaries[i][0]
        max      = list_of_boundaries[i][1]
        vertices = list_of_group_vertices[i]
        group    = Group(min, max, vertices)
        groups.append(group)
    
    return groups

def get_random_group_indexes(list_of_groups):
    rand_remove_index = random.randint(0, len(list_of_groups)-1)
    rand_add_index    = random.randint(0, len(list_of_groups)-1)

    while rand_add_index == rand_remove_index:
        rand_add_index = random.randint(0, len(list_of_groups)-1)

    return [rand_remove_index, rand_add_index]

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

def get_instance_value(list_of_groups, graph):
    instance_value = 0
    for group in list_of_groups:
        instance_value += group.get_group_value(graph)

    return instance_value

#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#INITIALIZATION
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================

file = open(sys.argv[1], "r")

num_of_vertices, num_of_groups = line_parsing(file.next())
num_of_vertices                = int(num_of_vertices)
num_of_groups                  = int(num_of_groups)

print "number of vertices : " + str(num_of_vertices) + "\n" + "number of groups : " + str(num_of_groups) + "\n"

bound_line   = line_parsing(file.next())
bound_count  = 0
group_bounds = []

while(bound_count < num_of_groups):
    group_bounds.append([int(bound_line[bound_count*2]), int(bound_line[bound_count*2 + 1])])
    bound_count += 1 

print "boundaries for each group:"

for element in group_bounds:
    print element

weight_line    = line_parsing(file.next())
vertex_weights = []

for i in range(0, num_of_vertices):
    vertex_weights.append(weight_line[i])
    if vertex_weights[i] < 0:
        exit("NEGATIVE VERTEX FOUND!!!")

graph_dict = dict()

for line in file:
    edge_line                       = line.replace("\n", "").split(" ")
    
    origin                          = int(edge_line[0])
    destination                     = int(edge_line[1])
    value                           = float(edge_line[2])
    
    graph_dict[origin, destination] = value

#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#Application
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================

num_of_iterations = 1000
num_of_neighbors  = 100

groups = initialize_groups_randomly(num_of_groups, num_of_vertices, group_bounds)

for group in groups:
    print str(group.group_vertices) + str(group.max_bound) + ' ' + str(group.min_bound)

graph         = Graph(num_of_vertices, graph_dict, vertex_weights)
initial_value = get_instance_value(groups, graph)

print "initial value : " + str(initial_value)

#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================
#Tabu Search
#=========================================================================================================================
#=========================================================================================================================
#=========================================================================================================================

max_tabu_size   = 100
actual_instance = groups
actual_value    = initial_value


for i in range(0, num_of_iterations):

    best_neighbor_solution = 0
    best_neighbor          = None
    best_tabu_movement     = None

    for j in range(0, num_of_neighbors):
        remove_index, add_index = get_random_group_indexes(groups)
        element                 = groups[remove_index].get_random_element()
        tabu                    = tabu_movement(remove_index, element)

        if element not in tabu_movements:
            new_group_list     = set_random_neighbor(actual_instance, add_index, remove_index, element, graph)
            new_instance_value = get_instance_value(new_group_list, graph)

            if new_instance_value > best_neighbor_solution:
                best_neighbor          = new_group_list
                best_neighbor_solution = new_instance_value
                best_tabu_movement     = element

    if best_neighbor_solution > 0:
        if len(tabu_movements) == max_tabu_size:
            del tabu_movements[0:len(tabu_movements)]

        tabu_movements.append(best_tabu_movement)
        actual_instance = best_neighbor
        actual_value = best_neighbor_solution

print "Final value : " + str(actual_value)
print "Final Groups settings :"
for group in actual_instance:
    print group.group_vertices