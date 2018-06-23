import sys

name = sys.argv[1]

file = open(name, "r")

headers = file.readline().split(",")

size = len(headers)

values = [0]*size

num_of_exec = 0

for line in file:
	num_of_exec += 1
	for i in range(0, size):
		values[i] += float(line.split(",")[i])

for i in range(0, size):
	print "medium " + headers[i].replace("\n", "") + " : " + str(values[i] / num_of_exec)