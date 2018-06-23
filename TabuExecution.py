import GBMV_BT
import sys

file 	  = open(sys.argv[1], "r")
tabu_prob = float(sys.argv[2])
option    = sys.argv[3]
times     = int(sys.argv[4])

graph, groups, num_of_vertices = GBMV_BT.read_instance_file(file)
max_tabu_size = 0.9 * num_of_vertices

name = sys.argv[1] + "-" + option + "-" + "prob" + str(tabu_prob) + ".txt"

file_to_write = open(name, "w+")

print "writing on " + name

for i in range(0, times):

	if option == 'big_step':

		GBMV_BT.run_big_step_tabu_search(groups, graph, 500, 100, 30, max_tabu_size, tabu_prob, file_to_write)

	if option == 'simple':
		GBMV_BT.run_simple_tabu_search(groups, graph, 10000, max_tabu_size, tabu_prob, file_to_write)

	if option == 'mixed':
		new_groups = GBMV_BT.run_big_step_tabu_search(groups, graph, 300, 100, 30, max_tabu_size, tabu_prob, None)
		GBMV_BT.run_simple_tabu_search(new_groups, graph, 1000, max_tabu_size, tabu_prob, file_to_write)