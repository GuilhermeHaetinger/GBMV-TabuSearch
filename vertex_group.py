import random

from graph import graph as Graph


ELEMENT_NOT_IN_GROUP   = -3
ELEMENT_ALREADY_IN_GROUP = -2
FAILED           = -1
SUCCEEDED        =  0

class vertex_group:

  def __init__(self, min_bound, max_bound, list_of_vertices):
      self.min_bound      = min_bound
      self.max_bound      = max_bound
      self.group_vertices = list_of_vertices
  
  def get_group_value(self, graph):
    group_value = 0

    for i in range(0, len(self.group_vertices)):
      for j in range (0, len(self.group_vertices)):
        if self.group_vertices[i] < self.group_vertices[j]:
          group_value += graph.get_edge_value(self.group_vertices[i], self.group_vertices[j])
          
    return group_value

  def get_group_total_weight(self, graph):
    total_weight = 0

    for element in self.group_vertices:
      total_weight += graph.get_vertex_value(element)

    return total_weight

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

  def get_random_element(self):
    rand_index = random.randint(0, len(self.group_vertices)-1)
    return self.group_vertices[rand_index]

  def copy(self):
    new_list_of_vertices = self.group_vertices[:]
    return vertex_group(self.min_bound, self.max_bound, new_list_of_vertices)

  def check_initial_consistency(self):
    return self.min_bound < self.get_group_total_weight and self.get_group_total_weight < self.max_bound