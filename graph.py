ELEMENT_NOT_IN_GROUP 	 = -3
ELEMENT_ALREADY_IN_GROUP = -2
FAILED					 = -1
SUCCEEDED				 =  0


class graph:

    def __init__(self, size, graph_dict, graph_values):
        self.size         = size
        self.graph_dict   = graph_dict
        self.graph_values = graph_values

    def get_edge_value(self, vertex_a, vertex_b):
        return self.graph_dict[vertex_a, vertex_b]

    def get_vertex_value(self, vertex):
        return int(self.graph_values[vertex])