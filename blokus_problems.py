import math

from board import Board
from search import SearchProblem, ucs, a_star_search
import util



class BlokusFillProblem(SearchProblem):
	"""
	A one-player Blokus game as a search problem.
	This problem is implemented for you. You should NOT change it!
	"""
	
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
		self.board = Board(board_w, board_h, 1, piece_list, starting_point)
		self.expanded = 0
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board
	
	def is_goal_state(self, state):
		"""
		state: Search state
		Returns True if and only if the state is a valid goal state
		"""
		return not any(state.pieces[0])
	
	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		# Note that for the search problem, there is only one player - #0
		self.expanded = self.expanded + 1
		return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]
	
	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
		self.board = Board(board_w, board_h, 1, piece_list, starting_point)
		self.starting_point = starting_point
		self.piece_list = piece_list
		self.board_h = board_h
		self.board_w = board_w
		self.expanded = 0
		self.corners = {(board_w - 1, board_h - 1), (board_w - 1, 0), (0, board_h - 1), (0, 0)}
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board
	
	def is_goal_state(self, state):
		board_array = state.state
		for x, y in self.corners:
			if board_array[x][y] == -1:
				return False
		return True
	
	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		# Note that for the search problem, there is only one player - #0
		self.expanded = self.expanded + 1
		return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]
	
	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		sum_of_actions = 0
		for move in actions:
			sum_of_actions += len(move.orientation)
		return sum_of_actions


def blokus_corners_heuristic(state, problem):
	"""
	Your heuristic for the BlokusCornersProblem goes here.

	This heuristic must be consistent to ensure correctness.  First, try to come up
	with an admissible heuristic; almost all admissible heuristics will be consistent
	as well.

	If using A* ever finds a solution that is worse uniform cost search finds,
	your heuristic is *not* consistent, and probably not admissible!  On the other hand,
	inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
	"""
	corners = problem.corners
	board_matrix = state.state
	uncovered_corners = 0
	pieces = problem.piece_list.pieces
	min_piece_size = math.inf
	for p in pieces:
		min_piece_size = min(min_piece_size, p.num_tiles)
	# because we know this is not a goal state, there should be at least one uncovered corner
	for corner_x, corner_y in corners:
		if board_matrix[corner_x][corner_y] == 0:  # this corner is already covered
			continue
		uncovered_corners += 1
	mult_factor = min(min_piece_size, (min(problem.board_h, problem.board_w) + 1) / 2.0)
	return mult_factor * uncovered_corners


# def blokus_corners_heuristic_1(state, problem):
# 	"""
# 	Your heuristic for the BlokusCornersProblem goes here.
#
# 	This heuristic must be consistent to ensure correctness.  First, try to come up
# 	with an admissible heuristic; almost all admissible heuristics will be consistent
# 	as well.
#
# 	If using A* ever finds a solution that is worse uniform cost search finds,
# 	your heuristic is *not* consistent, and probably not admissible!  On the other hand,
# 	inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
# 	"""
# 	if problem.is_goal_state(state):  # to save up the extra calculations in the case of a goal state.
# 		return 0
# 	corners = problem.corners
# 	board_matrix = state.state
# 	# create a set of all locations where tiles can begin
# 	legal_spots = set()
# 	board_w = problem.board_w
# 	for x in range(board_w):
# 		board_h = problem.board_h
# 		for y in range(board_h):
# 			if board_matrix[x][y] == -1:
# 				horizontal_free = (x-1 < 0 or board_matrix[x-1][y] == -1) and (x + 1 == board_w or
# 																			   board_matrix[x+1][y] == -1)
# 				vertical_free = (y - 1 < 0 or board_matrix[x][y-1] == -1) and (y + 1 == board_h or
# 																			   board_matrix[x][y + 1] == -1)
# 				if horizontal_free and vertical_free:
# 					diagonal_taken = False
# 					if x-1 >= 0 and y-1>=0 : diagonal_taken = diagonal_taken or board_matrix[x-1][y-1] == 0
# 					if x-1 >= 0 and y+1 < board_h: diagonal_taken = diagonal_taken or board_matrix[x - 1][y + 1] == 0
# 					if x+1 <board_w and y+1 <board_h: diagonal_taken = diagonal_taken or board_matrix[x + 1][y + 1]== 0
# 					if x+1 <board_w and y-1 >=0: diagonal_taken = diagonal_taken or board_matrix[x + 1][y - 1]== 0
# 					if diagonal_taken:
# 						legal_spots.add((x,y))
#
# 	sum_of_corner_distances = 0
# 	max_of_corner_distances = -math.inf
# 	uncovered_corners = 0
# 	# because we know this is not a goal state, there should be at least one uncovered corner
# 	for (corner_x, corner_y) in corners:
# 		if board_matrix[corner_x][corner_y] == 0:  # this corner is already covered
# 			continue
# 		uncovered_corners += 1
# 		dist_to_corner = math.inf
# 		for (x, y) in legal_spots:
# 			dist = min(abs(corner_x - x), abs(corner_y - y))
# 			dist_to_corner = min(dist_to_corner, dist)
# 		sum_of_corner_distances = sum_of_corner_distances + dist_to_corner
# 		max_of_corner_distances = max(max_of_corner_distances, dist_to_corner)
# 	return sum_of_corner_distances


class BlokusCoverProblem(SearchProblem):
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
		self.board = Board(board_w, board_h, 1, piece_list, starting_point)
		self.board_h = board_h
		self.board_w = board_w
		self.targets = targets.copy()
		self.expanded = 0
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board
	
	def is_goal_state(self, state):
		board_array = state.state
		for x, y in self.targets:
			if board_array[x][y] == -1:
				return False
		return True
	
	def get_successors(self, state):
		"""
		state: Search state

		For a given state, this should return a list of triples,
		(successor, action, stepCost), where 'successor' is a
		successor to the current state, 'action' is the action
		required to get there, and 'stepCost' is the incremental
		cost of expanding to that successor
		"""
		# Note that for the search problem, there is only one player - #0
		self.expanded = self.expanded + 1
		return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]
	
	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		sum_of_actions = 0
		for move in actions:
			sum_of_actions += len(move.orientation)
		return sum_of_actions


def blokus_cover_heuristic(state, problem):
	targets = problem.targets
	board_matrix = state.state
	uncovered_targets = 0
	# pieces = problem.piece_list.pieces
	# min_piece_size = math.inf
	# for p in pieces:
	# 	min_piece_size = min(min_piece_size, p.num_tiles)
	# because we know this is not a goal state, there should be at least one uncovered corner
	for x, y in targets:
		if board_matrix[x][y] == 0:  # this corner is already covered
			continue
		uncovered_targets += 1
	# mult_factor = min(min_piece_size, (min(problem.board_h, problem.board_w) + 1) / 2.0)
	mult_factor = 1
	return mult_factor * uncovered_targets


class ClosestLocationSearch:
	"""
	In this problem you have to cover all given positions on the board,
	but the objective is speed, not optimality.
	"""
	
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
		self.expanded = 0
		self.starting_point = starting_point
		self.targets = targets.copy()
		self.piece_list = piece_list
		self.board = Board(board_w, board_h, 1, piece_list, starting_point)
		self.board_h = board_h
		self.board_w = board_w
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board
	
	def is_goal_state(self, state):
		board_array = state.state
		for x, y in self.targets:
			if board_array[x][y] == -1:
				return False
		return True
	
	def closest_target(self, state):
		is_start_state = state.state[self.starting_point[0]][self.starting_point[1]] == -1
		closest = (-1, -1)
		best_dist = math.inf
		for target in self.targets:
			dist = self.distance_to_target(target, state, is_start_state)
			if 0 < dist < best_dist:
				best_dist = dist
				closest = target
		return closest, best_dist
	
	
	def distance_to_target(self, target, state, is_start_state=False):
		if is_start_state:
			return abs(target[0] - self.starting_point[0]) + abs(self.starting_point[1] - target[1])
		board = state.state
		best_dist = math.inf
		for x in range(self.board_w):
			for y in range(self.board_h):
				if board[x][y] == 0:
					dist = abs(target[0] - x) + abs(target[1] - y)
					best_dist = min(best_dist, dist)
		return best_dist
	
	def solve(self):
		"""
		This method should return a sequence of actions that covers all target locations on the board.
		This time we trade optimality for speed.
		Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest
		uncovered location.
		You may define helpful functions as you wish.

		Probably a good way to start, would be something like this --

		current_state = self.board.__copy__()
		backtrace = []

		while ....

			actions = set of actions that covers the closets uncovered target location
			add actions to backtrace

		return backtrace
		"""
		current_state = self.board.__copy__()
		backtrace = []
		problem = BlokusCoverProblem(self.board_w, self.board_h, self.piece_list, self.starting_point, self.targets)
		
		def heuristic(state, problem):
			return self.closest_target(state)[1]
		
		return a_star_search(problem, heuristic)
		#
		# next_target = self.closest_target(current_state, is_start_state=True)
		#
		# while next_target != (-1, -1):  # while there are uncovered targets
		# 	successors = [(current_state.do_move(0, move), move, move.piece.get_num_tiles()) for move in \
		# 				  	current_state.get_legal_moves(0)]
		# 	successors.sort(key=lambda x: self.distance_to_target(next_target, x[0]))
		# 	for suc in successors:
		# 		pass
		# 	# found_successor = False
		# 	# successor_state = None
		# 	# for s in successors:
		# 	# 	if s[0].state[next_target[0]][next_target[1]] == 0:
		# 	# 		backtrace.append(s[1])
		# 	# 		found_successor = True
		# 	# 		successor_state = s[0]
		# 	# 		break
		# 	# if found_successor:
		# 	# 	next_target = self.closest_target(successor_state)
		# 	# else:
	#
	# def solve_helper(self, targets, state, is_start_state=False):
	# 	current_state = state.__copy__()
	# 	next_target = self.closest_target(current_state, is_start_state)
	# 	if next_target != (-1, -1):  # while there are uncovered targets
	# 		return []
	# 	successors = [(current_state.do_move(0, move), move, move.piece.get_num_tiles()) for move in \
	# 					current_state.get_legal_moves(0)]
	# 	successors.sort(key=lambda x: self.distance_to_target(next_target, x[0]))
	# 	for suc in successors:
	# 		if()


class MiniContestSearch:
	"""
	Implement your contest entry here
	"""
	
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
		self.targets = targets.copy()
		"*** YOUR CODE HERE ***"
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board
	
	def solve(self):
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()
