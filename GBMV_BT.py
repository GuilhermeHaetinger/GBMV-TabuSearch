from vertex_group import vertex_group as Group
from graph import graph as Graph
from random import randint
import sys
import time

ELEMENT_NOT_IN_GROUP     = -3
ELEMENT_ALREADY_IN_GROUP = -2
FAILED                   = -1
SUCCEEDED                =  0

#NAO SEI SE UTILIZAR
class tabu_movement:
    def __init__(self, remove_group_index, element):
        self.remove_group_index = remove_group_index
        self.element = element

def test_if_element_repeats(list_of_groups):
    a = dict()

    for i in range(0, len(list_of_groups)):
        for k in range(0, len(list_of_groups[i].group_vertices)):
            if list_of_groups[i].group_vertices[k] in a:
                print list_of_groups[i].group_vertices[k]
            a[list_of_groups[i].group_vertices[k]] = 1 
            

def line_parsing(line):
    return line.replace(" \n", "").split(" ")

def fill_group_randomly(group, unused_vertices, num_of_vertices, graph):
    while(group.min_bound > group.get_group_value(graph)):
        rand_vertice = randint(0, len(unused_vertices)-1)
        group.group_vertices.append(unused_vertices[rand_vertice])
        unused_vertices.pop(rand_vertice)

    return group


def initialize_groups_randomly(num_of_groups, num_of_vertices, list_of_boundaries, graph):
    list_of_groups = []
    for i in range(0, num_of_groups):
        list_of_groups.append(Group(list_of_boundaries[i][0], list_of_boundaries[i][1], []))

    unused_vertices = []
    for i in range(0, num_of_vertices):
        unused_vertices.append(i)
    
    for i in range(0, num_of_groups):
        list_of_groups[i] = fill_group_randomly(list_of_groups[i], unused_vertices, num_of_vertices, graph)
        print list_of_groups[i].group_vertices

    for i in unused_vertices:
        randGroup = randint(0, num_of_groups-1)
        while(list_of_groups[randGroup].add_element(i, graph) != SUCCEEDED):
            randGroup = randint(0, num_of_groups-1)
       

    return list_of_groups


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
    rand_remove_index = randint(0, len(list_of_groups)-1)
    rand_add_index    = randint(0, len(list_of_groups)-1)

    while rand_add_index == rand_remove_index:
        rand_add_index = randint(0, len(list_of_groups)-1)

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

num_of_iterations = 500
num_of_neighbors  = 100


graph         = Graph(num_of_vertices, graph_dict, vertex_weights)


groups = initialize_groups_randomly(num_of_groups, num_of_vertices, group_bounds, graph)

for group in groups:
    print str(group.group_vertices) + str(group.max_bound) + ' ' + str(group.min_bound)

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
tabu_movements  = []
best_solution_found = 0
best_found = None
num_of_elements = 30
try:
    tabu_prob = int(sys.argv[2])
except Exception as e:
    tabu_prob = -1

init_time = time.time()


for i in range(0, num_of_iterations):

    best_neighbor_solution = 0
    best_neighbor          = None
    best_tabu_movement     = None

    for j in range(0, num_of_neighbors):
        tabu = []
        new_group_list = actual_instance[:]
        for k in range(0, num_of_elements):
            rand_remove, rand_add = get_random_group_indexes(new_group_list)
            element = new_group_list[rand_remove].get_random_element()
            if tabu_prob >= 0:
                if randint(0, tabu_prob) == 0:
                    tabu.append(element)
            if element not in tabu_movements:
                new_group_list = set_random_neighbor(new_group_list, rand_add, rand_remove, element, graph)

        new_instance_value = get_instance_value(new_group_list, graph)

        if new_instance_value > best_neighbor_solution:
            best_neighbor          = new_group_list
            best_neighbor_solution = new_instance_value
            best_tabu_movement     = tabu

    if best_neighbor_solution > 0:
        if len(tabu_movements) == max_tabu_size:
            del tabu_movements[0:len(tabu_movements)]

        tabu_movements.append(best_tabu_movement)
        #print tabu
        actual_instance = best_neighbor
        actual_value = best_neighbor_solution

        if actual_value > best_solution_found:
            best_solution_found  = actual_value
            best_found = actual_instance

print "Final value : " + str(actual_value)
print "Final Groups settings :"
for group in actual_instance:
    print group.group_vertices
if tabu_prob >= 0:
    print "Tabu probability used: " + str((1/float(tabu_prob+1))*100) + "%" 
else:
    print "Tabu probability not used"

print "time taken : " + str(time.time() - init_time) + " sec" 