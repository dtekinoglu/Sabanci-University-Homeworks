# -*- coding: utf-8 -*-
"""CS404-A1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pcLXwbKViTa9qKK5Htl-gSZCitTSMxDh

### CS404 - A1 
### Dilara Tekinoğlu - 27868

- States: $(f+e)$ x 4 matrices where $f$ is the number of full bottles and $e$ is the number of empty bottles. The matrices consist of integers where a cell has -1 if it is empty, $c_i$ if it has ball with color $i$. 

- Initial State: A $(f+e)$ x 4 matrix where the first $f$ rows come from input and the last $e$ rows contain -1s.

- Successor State Function: Takes a state (matrix of  $(f+e)$ x 4) as parameter. The action is performed between two rows. The rightmost (not (-1)) value of a row is changed with the leftmost -1 value of another row (if colors match). 

- Step Cost: It is equal to 1 for each state transition (each ball move).

- Goal Test: A matrix is at goal state if $e$ many rows contains only -1s and other rows contain the same value for each of their columns.
"""

# Uniform Cost Search Implementation
# Since the cost of all actions are equal (moving one ball from one position to another position), 
# UCS is the same with BFS for this problem. Therefore, we actually implement Breadth-First Search.

class UCS_Node:
  # Initialize the class
  def __init__(self, parent:UCS_Node, state:list):
    self.state = state
    self.parent = parent

# Checks whether the state is a goal state.
def goal_test(matrix, f, e):
  if matrix.count([-1,-1,-1,-1]) != e:
    return False
  for row in matrix:
    if row != [-1,-1,-1,-1]:
      if row.count(row[0]) !=4:
        return False
  return True

# Returns a list of state of successor nodes.
def successor_function(current_state):
  children = []
  for i in range(len(current_state)):
    for j in range(len(current_state)):

      #if the same row, continue
      if i != j:
        matrix = [row[:] for row in current_state]

        #if giving row is all -1s or receiving or is full, continue
        if matrix[i].count(-1) != 4 and matrix[j].count(-1) !=0:
          idx_leftmost_minus_one = matrix[j].index(-1)
          # giving row is full.
          if matrix[i][3] != -1:
            idx_rightmost_colored = 3
          else:
            idx_rightmost_colored = matrix[i].index(-1) -1
          # if receiving row is empty bottle or colors match
          if idx_leftmost_minus_one == 0 or matrix[j][idx_leftmost_minus_one-1] == matrix[i][idx_rightmost_colored]:
            matrix[j][idx_leftmost_minus_one] = matrix[i][idx_rightmost_colored]
            matrix[i][idx_rightmost_colored] = -1
            if matrix not in children:
              children.append(matrix)
  return children

# Uniform Cost Search Algorithm
def ucs(start,f,e):
  path = []
  if goal_test(start,f,e):
    print("The puzzle is already solved.")
    return path

  frontier = []
  start_node = UCS_Node(None,start)
  frontier.append(start_node)

  explored_nodes = [start_node]

  while True:
    if len(frontier) == 0:
      return "No solution"
    
    current_node = frontier.pop(0)
    explored_nodes.append(current_node)
    children = successor_function(current_node.state)

    for child in children:
      new_born = UCS_Node(current_node, child)
      if new_born not in explored_nodes and new_born not in frontier:
        if goal_test(new_born.state,f,e):
        # This part returns the solution path by backtracking parents.
          parent_track = new_born
          while parent_track != start_node:
            path.append(parent_track.state)
            try:
              parent_track = UCS_Node(parent_track.parent.parent, parent_track.parent.state)
            except:
              parent_track = start_node
          path.reverse()
          return path
        frontier.append(new_born)

# Function for printing input in desired game format.
def print_actions(path):
  for j in range(3,-1,-1):
    row = ""
    for i in range(len(path)):
      row += str(path[i][j]) + " "
    print(row)

# Implementation of A* Search for the problem
import math
import time
from memory_profiler import profile
from memory_profiler import memory_usage

class Node:
  # Initialize the class
  def __init__(self, parent:list, state:list):
    self.state = state
    self.parent = parent
    self.g = 0
    self.h = 0 
    self.f = 0

def duplicate_check(list_to_search, node):
  for elem in list_to_search:
    if elem.state == node.state:
      return True
  return False

def modify_frontier(frontier, node):
  for elem in frontier:
    if elem.state == node.state:
      if elem.f > node.f:
        elem.f = node.f
        elem.state = node.state
        elem.parent = node.parent
        elem.g = node.g
        break

def modify_frontier_closed(frontier, explored, node):
  for i in range(len(explored)):
    elem = explored[i]
    if elem.state == node.state:
      if elem.f > node.f:
        new_node = Node(node.parent, node.state)
        new_node.f = node.f
        new_node.g = node.g
        idx = i
        explored.pop(idx)
        frontier.append(new_node)
        break

# Returns heuristic cost of a node.
def expected_cost(node):
  cost = len(node)
  for row in node:
    if row.count(row[0]) == 4:
      cost-=1
  return cost

# Returns to node that has lowest-cost in frontier
def get_lowest_cost(frontier):
  result = Node(None,None)
  result.f = math.inf
  for node in frontier:
    if node.f < result.f:
      result = node
  return result

# A* Search Algorithm
def a_star_search(start,f,e):
  start_node = Node(None,start)
  path = []
  frontier = []
  explored = []

  frontier.append(start_node)

  while True:
    if len(frontier) == 0:
      return "No Solution"
    
    selected_node = get_lowest_cost(frontier)
    frontier.remove(selected_node)
    explored.append(selected_node)

    if goal_test(selected_node.state,f,e):
      # This part returns path by backtracking parents.
      current_node = selected_node
      while current_node.parent != None:
        path.append(current_node.state)
        current_node = current_node.parent
      path.append(start_node.state)
      path.reverse()
      return path
    
    children = successor_function(selected_node.state)

    for child in children:

      child_node = Node(selected_node, child)

      if child_node not in explored:
        child_node.g = selected_node.g + 1
        child_node.h = expected_cost(child_node.state)
        child_node.f = child_node.g + child_node.h

        in_frontier = duplicate_check(frontier, child_node)
        in_explored = duplicate_check(explored, child_node)
        
        if  in_frontier == False and in_explored == False:
          frontier.append(child_node)

        # if node already in frontier, let's check and modify its cost if necessary.
        elif in_frontier:
          modify_frontier(frontier,child_node)
        
        # Re-opening node in frontier
        elif in_explored:
          modify_frontier_closed(frontier, explored, child_node)
    explored.append(selected_node)

def get_input():
  [f,e] = list(map(int, input().split()))
  mat = []
  for i in range (f):
    row = list(map(int, input().split()))
    mat.append(row)
  for i in range(e):
    mat.append([-1,-1,-1,-1])
  return [f,e,mat]

a_star_time = []
ucs_time = []

                                                                """ 
Example Input 1:      Example Input 2:      Example Input 3:

4 2                   3 1                   2 1
2 2 2 1               2 2 2 2               1 2 1 2
1 1 1 4               1 1 3 1               2 1 2 1
3 3 3 2               3 3 1 3
4 4 4 3 
                                                                """

info = get_input()

mat = info[2]
f = info[0]
e = info[1]
st = time.time()

path =ucs(mat,f,e)
print("UCS solves puzzle with", len(path), "actions")
stop = time.time()
time_ucs = stop-st
ucs_time.append(time_ucs)
print("UCS takes", stop-st, "seconds.")

st = time.time()
path = a_star_search(mat,f,e)
print("A* solves puzzle with", len(path), "actions.")
stop = time.time()
time_a_star = stop-st
a_star_time.append(time_a_star)
print("A* takes", stop-st, "seconds.")

import matplotlib.pyplot as plt

print(a_star_time)
print(ucs_time)

#Plotting results
def compare_times(a_star_time, ucs_time):
  x_axis = ["Input 1", "Input 2", "Input 3"]
  plt.plot(x_axis, a_star_time, label = "A* Search")
  plt.plot(x_axis, ucs_time, label = "UCS")
  plt.ylabel("Time in seconds")
  plt.legend()
  plt.show()

compare_times(a_star_time,ucs_time)

# We will store peak memory usages in these lists.
mem_ucs = []
mem_a_star = []

# Tracing memory usage for the same input set.
                                                                """ 
Example Input 1:      Example Input 2:      Example Input 3:

4 2                   3 1                   2 1
2 2 2 1               2 2 2 2               1 2 1 2
1 1 1 4               1 1 3 1               2 1 2 1
3 3 3 2               3 3 1 3
4 4 4 3 
                                                                """
import tracemalloc
 
info = get_input()

mat = info[2]
f = info[0]
e = info[1]

tracemalloc.start()
path =ucs(mat,f,e)
print("UCS solves puzzle with", len(path), "actions")
mem_ucs.append(tracemalloc.get_traced_memory())
tracemalloc.stop()

tracemalloc.start()
path = a_star_search(mat,f,e)
print("A* solves puzzle with", len(path), "actions.")
mem_a_star.append(tracemalloc.get_traced_memory())
tracemalloc.stop()

# We will get only peak memory usage values.
mem_peak_ucs = []
for elem in mem_ucs:
  mem_peak_ucs.append(elem[1])

mem_peak_a_star = []
for elem in mem_a_star:
  mem_peak_a_star.append(elem[1])

def compare_memory(mem_peak_a_star, mem_peak_ucs):
  x_axis = ["Input 1", "Input 2", "Input 3"]
  plt.plot(x_axis, mem_peak_a_star, label = "A* Search")
  plt.plot(x_axis, mem_peak_ucs, label = "UCS")
  plt.ylabel("Peak Memory Usage")
  plt.legend()
  plt.show()

compare_memory(mem_peak_a_star, mem_peak_ucs)