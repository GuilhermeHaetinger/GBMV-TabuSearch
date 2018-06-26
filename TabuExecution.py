import GBMV_BT
import sys
import random
import time

random.seed(123123)

file_to_write = open(sys.argv[1], "w+")
file 	  = open(sys.argv[2], "r")
tabu_prob = float(sys.argv[3])
option    = sys.argv[4]

graph, groups, num_of_vertices = GBMV_BT.read_instance_file(file)
max_tabu_size = float(sys.argv[5]) * num_of_vertices
num_iter = int(sys.argv[6])


print "initial value --- " + str(GBMV_BT.get_instance_value(groups, graph)) + "\n"
print "writing on " + sys.argv[1]

new_groups = []
init_time = 0
end_time = 0

if option == 'big_step':
	init_time = time.time()
	new_groups = GBMV_BT.run_big_step_tabu_search(groups, graph, num_iter, 100, 30, max_tabu_size, tabu_prob)
	end_time = time.time()

elif option == 'simple':
	init_time = time.time()
	new_groups = GBMV_BT.run_simple_tabu_search(groups, graph, num_iter, max_tabu_size, tabu_prob)
	end_time = time.time()

elif option == 'mixed':
	num_iter_for_solution_gen = int(sys.argv[7])
	init_time = time.time()
	new_groups = GBMV_BT.run_big_step_tabu_search(groups, graph, num_iter_for_solution_gen, 100, 30, max_tabu_size, 0)
	new_groups = GBMV_BT.run_simple_tabu_search(new_groups, graph, num_iter, max_tabu_size, tabu_prob)
	end_time = time.time()

else:
	print "Commando invalido"
	exit(0)
file_to_write.write("Best Solution : \n")

for group in new_groups:
	file_to_write.write(str(group.group_vertices) + "\n")

file_to_write.write("Final Value : " + str(GBMV_BT.get_instance_value(new_groups, graph)) + "\n")
file_to_write.write("Execution Time : " + str(end_time - init_time))