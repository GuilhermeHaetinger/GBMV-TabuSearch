import random

from graph import graph as Graph

#Definitions for returning values for specific methods
ELEMENT_NOT_IN_GROUP   = -3
ELEMENT_ALREADY_IN_GROUP = -2
FAILED           = -1
SUCCEEDED        =  0

class vertex_group:

  '''
  Constructor for vertex_group class

  Params:
    min_bound(int)              : Group's lower weight limit   
    max_bound(int)              : Group's higher weight limit
    list_of_vertices(List(int)) : Group's vertices

  returns:
    vertex_group instance (vertex_group)

  '''
  def __init__(self, min_bound, max_bound, list_of_vertices):
      self.min_bound      = min_bound
      self.max_bound      = max_bound
      self.group_vertices = list_of_vertices
  
  '''
  Group's value calculation method

  Params:
    graph(Graph) : Graph that contains all edges values

  returns:
    The total value of the group (int)

  '''
  def get_group_value(self, graph):
    group_value = 0

    for i in range(0, len(self.group_vertices)):
      for j in range (0, len(self.group_vertices)):
        if self.group_vertices[i] < self.group_vertices[j]:
          group_value += graph.get_edge_value(self.group_vertices[i], self.group_vertices[j])
          
    return group_value


  '''
  Group's total weight calculation method

  Params:
    graph(Graph) : GRaph that contains all vertices weights

  returns:
    Group's total vertex weight(int)
  
  '''
  def get_group_total_weight(self, graph):
    total_weight = 0

    for element in self.group_vertices:
      total_weight += graph.get_vertex_value(element)

    return total_weight

  '''
  Group's method for element inclusion

  Params:
    element(int) : element to include
    graph(Graph) : Graph with the information for group validation

  returns:
    Inclusion final status(int):
      0  : Inclusion was successful
      -1 : Inclusion exceeds weight limit
      -2 : element is already in the group 
  
  '''
  def add_element(self, element, graph):
    if element in self.group_vertices:
      return ELEMENT_ALREADY_IN_GROUP

    group_buffer = self.copy()
    group_buffer.group_vertices.append(element)

    new_weight = group_buffer.get_group_total_weight(graph)

    if  new_weight > self.max_bound:
      return FAILED

    else:
      self.group_vertices.append(element)
      return SUCCEEDED

  '''
  Group's method for element removal

  Params:
    element(int) : element to remove
    graph(Graph) : Graph with the information for group validation

  returns:
    Removal final status(int):
      0  : removal was successful
      -1 : removal takes the group's weight out of the limited interval
      -3 : element is not in the group 

  '''
  def remove_element(self, element, graph):
    if element not in self.group_vertices:
      return ELEMENT_NOT_IN_GROUP

    elif len(self.group_vertices) > 1:
      
      group_buffer = self.copy()
      group_buffer.group_vertices.remove(element)

      new_weight = group_buffer.get_group_total_weight(graph)

      if  self.min_bound > new_weight:
        return FAILED

      else:
        self.group_vertices.remove(element)
        return SUCCEEDED
        
    else:
      return FAILED
  
  '''
  Random vertex picker

  returns:
    reandom vertex(int)

  '''
  def get_random_element(self):
    rand_index = random.randint(0, len(self.group_vertices)-1)
    return self.group_vertices[rand_index]

  '''
  Group copier (without memory reference)

  returns:
    A copy of the group (vertex_group)

  '''
  def copy(self):
    new_list_of_vertices = self.group_vertices[:]
    return vertex_group(self.min_bound, self.max_bound, new_list_of_vertices)
  
  '''
  Group's method for weight validation
  returns:
    group weight validation (boolean)
    
  '''
  def check_initial_consistency(self):
    return self.min_bound < self.get_group_total_weight and self.get_group_total_weight < self.max_bound