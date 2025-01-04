import heapq 
import sys

# Define the puzzle class 
class Puzzle:
  def __init__(self, size):
    self.size = size
    self.goal_state = tuple(range(1, size * size)) + (0,) self.initial_state = None
    
  def is_solvable(self, state): inversions = 0
    for i in range(len(state)):
      for j in range(i + 1, len(state)):
        if state[i] > state[j] and state[i] != 0 and state[j] != 0:
          inversions += 1 
    return inversions % 2 == 0
      
  def get_neighbors(self, state): 
    neighbors = [] 
    blank_idx = state.index(0)
    row, col = divmod(blank_idx, self.size)
    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
      new_row, new_col = row + dr, col + dc
      if 0 <= new_row < self.size and 0 <= new_col < self.size:
        new_state = list(state)
        new_blank_idx = new_row * self.size + new_col
        new_state[blank_idx], new_state[new_blank_idx] = new_state[new_blank_idx], new_state[blank_idx] 
        neighbors.append(tuple(new_state))
    return neighbours

  def heuristic(self, state):
      # The heuristic function calculates the sum of Manhattan distances of tiles from their goal positions. 
      h=0
      for i in range(len(state)):
        if state[i] == 0: continue
          goal_row, goal_col = divmod(state[i] - 1, self.size)
        current_row, current_col = divmod(i, self.size)
        h += abs(goal_row - current_row) + abs(goal_col - current_col)
      return h
    
  def solve(self, initial_state): 
    self.initial_state = tuple(initial_state)
    if not self.is_solvable(self.initial_state):
      return None
    open_set = [(self.heuristic(self.initial_state), 0, self.initial_state)] 
    closed_set = set()
    g_scores = {self.initial_state: 0}
    came_from = {}
    while open_set:
      _, g, current_state = heapq.heappop(open_set) 
      if current_state == self.goal_state:
        path = []
        while current_state in came_from:
          path.append(current_state)
          current_state = came_from[current_state] 
        path.append(self.initial_state) 
        path.reverse()
        return path
      if current_state in closed_set: 
        continue
      closed_set.add(current_state)
      for neighbor in self.get_neighbors(current_state):
        tentative_g = g + 1
        if neighbor not in g_scores or tentative_g < g_scores[neighbor]: 
          g_scores[neighbor] = tentative_g
          f = tentative_g + self.heuristic(neighbor) 
          heapq.heappush(open_set, (f, tentative_g, neighbor)) 
          came_from[neighbor] = current_state
      return None


# Helper function to print the puzzle state 
def print_puzzle(state, size):
  for i in range(0, len(state), size):
    print(" ".join(map(str, state[i:i + size])))

try:
  size = int(input("Enter the size of the puzzle (e.g., 3 for 8-puzzle, 4 for 15-puzzle, etc.): "))
except ValueError:
  print("Invalid input. Please enter a valid integer.") 
  sys.exit(1)
if size < 2:
  print("Puzzle size must be at least 2x2.") 
  sys.exit(1)
cost=0
n = size * size
initial_state = []
print(f"Enter {n-1} numbers (0 for the blank space) separated by spaces:")


try:
user_input = input().split() 
for num in user_input:
  num = int(num)
  if num < 0 or num >= n:
    print(f"Invalid number: {num}. Please enter valid numbers.")
    sys.exit(1) 
  initial_state.append(num)
except ValueError:
  print("Invalid input. Please enter valid numbers.") 
  sys.exit(1)
puzzle = Puzzle(size)
solution = puzzle.solve(initial_state)
if solution:
  print("Solution steps:")
  for step, state in enumerate(solution):
    print(f"Step {step + 1}:") print_puzzle(state, size) 
    print()
    cost+=1
  print(f"Total Cost = ",cost) 
else:
  print("No solution found.")
