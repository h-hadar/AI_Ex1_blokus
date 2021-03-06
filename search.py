"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
	"""
	This class outlines the structure of a search problem, but doesn't implement
	any of the methods (in object-oriented terminology: an abstract class).

	You do not need to change anything in this class, ever.
	"""
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		util.raiseNotDefined()
	
	def is_goal_state(self, state):
		"""
		state: Search state

		Returns True if and only if the state is a valid goal state
		"""
		util.raiseNotDefined()
	
	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		util.raiseNotDefined()
	
	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		util.raiseNotDefined()


def depth_first_search(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches
	the goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
	print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
	print("Start's successors:", problem.get_successors(problem.get_start_state()))
	"""
	path = []
	if problem.is_goal_state(problem.get_start_state()):
		return path
	visited_states = set()
	visited_states.add(problem.get_start_state())
	fringe_stack = problem.get_successors(problem.get_start_state())
	
	while len(fringe_stack) != 0:
		current = fringe_stack.pop()
		if current is None:
			path.pop()
			continue
		visited_states.add(current[0])  # current[0] is the board object of this node
		if problem.is_goal_state(current[0]):
			path.append(current[1])  # current[1] is the 'move' object of this node
			return path
		successors = problem.get_successors(current[0])
		added = False
		fringe_stack.append(None)
		for child in successors:
			if child[0] not in visited_states:
				added = True
				fringe_stack.append(child)
		if added:
			path.append(current[1])
		else:
			fringe_stack.pop()  # remove the None we pushed


def breadth_first_search(problem):
	"""
	Search the shallowest nodes in the search tree first.
	"""
	path = []
	if problem.is_goal_state(problem.get_start_state()):
		return path
	visited_states = set()
	visited_states.add(problem.get_start_state())
	fringe = []
	successors = problem.get_successors(problem.get_start_state())
	for s in successors:
		fringe.append((s, None))
	while len(fringe):
		current = fringe.pop(0)  # a tuple of (child, parent_index) where child is a 3-value tuple
		if current[0][0] not in visited_states:
			path.append(current)
			visited_states.add(current[0][0])
			parent_index = len(path) - 1
			if problem.is_goal_state(current[0][0]):
				# return path
				break
			successors = problem.get_successors(current[0][0])
			for child in successors:
				if child[0] not in visited_states:
					fringe.append((child, parent_index))
	
	goal = path[-1]
	parent_index = goal[1]
	move_list = [goal[0][1]]  # goal[child][move]
	while parent_index is not None:
		cur = path[parent_index]  # a tuple of (child, parent_index) where child is a 3-value tuple
		move_list.append(cur[0][1])
		parent_index = cur[1]
	return move_list[::-1]


def uniform_cost_search(problem):
	"""
	Search the node of least total cost first.
	"""
	path = []
	if problem.is_goal_state(problem.get_start_state()):
		return path
	state_dict = dict()
	visited_states = set()
	visited_states.add(problem.get_start_state())
	fringe = util.PriorityQueue()
	successors = problem.get_successors(problem.get_start_state())
	for s in successors:
		cost = problem.get_cost_of_actions([s[1]])
		state_dict[s[0]] = (s, None, cost)
		fringe.push(s[0], cost)
	while not fringe.isEmpty():
		current = fringe.pop()  # object of type board
		if current not in visited_states:
			data_for_current = state_dict[current]  # state_dict[current] is a tuple (child, parent_index, cost_from_root)
			path.append(data_for_current)
			visited_states.add(current)
			parent_index = len(path) - 1
			if problem.is_goal_state(current):
				# return path
				break
			successors = problem.get_successors(current)
			for child in successors:
				if child[0] not in visited_states:
					cost = problem.get_cost_of_actions([child[1]]) + data_for_current[2]
					state_dict[child[0]] = (child, parent_index, cost)
					fringe.push(child[0], cost)
	
	goal = path[-1]
	parent_index = goal[1]
	move_list = [goal[0][1]]  # goal[child][move]
	while parent_index is not None:
		cur = path[parent_index]  # a tuple of (child, parent_index) where child is a 3-value tuple
		move_list.append(cur[0][1])
		parent_index = cur[1]
	return move_list[::-1]


def null_heuristic(state, problem=None):
	"""
	A heuristic function estimates the cost from the current state to the nearest
	goal in the provided SearchProblem.  This heuristic is trivial.
	"""
	return 0


def a_star_search(problem, heuristic=null_heuristic):
	"""
	Search the node that has the lowest combined cost and heuristic first.
	"""
	path = []
	if problem.is_goal_state(problem.get_start_state()):
		return path
	state_dict = dict()
	visited_states = set()
	visited_states.add(problem.get_start_state())
	fringe = util.PriorityQueue()
	successors = problem.get_successors(problem.get_start_state())
	for s in successors:
		cost = problem.get_cost_of_actions([s[1]])
		state_dict[s[0]] = (s, None, cost)
		fringe.push(s[0], cost + heuristic(s[0], problem))
	while not fringe.isEmpty():
		current = fringe.pop()  # object of type board
		if current not in visited_states:
			data_for_current = state_dict[current]  # state_dict[current] is a tuple (child, parent_index, cost_from_root)
			path.append(data_for_current)
			visited_states.add(current)
			parent_index = len(path) - 1
			if problem.is_goal_state(current):
				# return path
				break
			successors = problem.get_successors(current)
			for child in successors:
				if child[0] not in visited_states:
					cost = problem.get_cost_of_actions([child[1]]) + data_for_current[2]
					state_dict[child[0]] = (child, parent_index, cost)
					fringe.push(child[0], cost + heuristic(child[0], problem))

	goal = path[-1]
	parent_index = goal[1]
	move_list = [goal[0][1]]  # goal[child][move]
	while parent_index is not None:
		cur = path[parent_index]  # a tuple of (child, parent_index) where child is a 3-value tuple
		move_list.append(cur[0][1])
		parent_index = cur[1]
	return move_list[::-1]


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
