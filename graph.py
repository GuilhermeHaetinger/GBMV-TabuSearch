ELEMENT_NOT_IN_GROUP 	 = -3
ELEMENT_ALREADY_IN_GROUP = -2
FAILED					 = -1
SUCCEEDED				 =  0


class graph:
    '''
    Constructor for graph class

    Params:
        graph_dict(dict(int, int) -> float) : edges values
        graph_values(List(int))             : vertices weights

    returns:
        graph instance (graph)

    '''
    def __init__(self, size, graph_dict, graph_values):
        self.size         = size
        self.graph_dict   = graph_dict
        self.graph_values = graph_values
   
    '''
    Graph's method for edge value retrieval

    Params:
        vertex_a(int) : the first vertex 
        vertex_b(int) : the second vertex

    returns:
        edge value (int)

    '''
    def get_edge_value(self, vertex_a, vertex_b):
        return self.graph_dict[vertex_a, vertex_b]
    
    '''
    Graph's method for vertex weight retrieval

    Params:
        vertex(int) : vertex from which the weight is wanted

    returns:
        vertex weight (int)

    '''
    def get_vertex_value(self, vertex):
        return self.graph_values[vertex]