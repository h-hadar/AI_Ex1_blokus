import math

from board import Board
from search import SearchProblem, ucs
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
		"*** YOUR CODE HERE ***"
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
		"*** YOUR CODE HERE ***"
		sum = 0
		for move in actions:
			sum += len(move.orientation)
		return sum
	

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
	"*** YOUR CODE HERE ***"
	if problem.is_goal_state(state):  # to save up the extra calculations in the case of a goal state.
		return 0
	corners = problem.corners
	board_matrix = state.state
	# create a set of all locations where tiles can be begin
	legal_spots = set()
	board_w = problem.board_w
	for x in range(board_w):
		board_h = problem.board_h
		for y in range(board_h):
			if board_matrix[x][y] == -1:
				horizontal_free = (x-1 < 0 or board_matrix[x-1][y] == -1) and (x + 1 == board_w or
																			   board_matrix[x+1][y] == -1)
				vertical_free = (y - 1 < 0 or board_matrix[x][y-1] == -1) and (y + 1 == board_h or
																			   board_matrix[x][y + 1] == -1)
				if horizontal_free and vertical_free:
					diagonal_taken = False
					if x-1 >= 0 and y-1>=0 : diagonal_taken = diagonal_taken or board_matrix[x-1][y-1] == 0
					if x-1 >= 0 and y+1 < board_h: diagonal_taken = diagonal_taken or board_matrix[x - 1][y + 1] == 0
					if x+1 <board_w and y+1 <board_h: diagonal_taken = diagonal_taken or board_matrix[x + 1][y + 1]== 0
					if x+1 <board_w and y-1 >=0: diagonal_taken = diagonal_taken or board_matrix[x + 1][y - 1]== 0
					if diagonal_taken:
						legal_spots.add((x,y))
	
	min_of_corner_distances = math.inf
	# because we know this is not a goal state, there should be at least one corner with non-zero distance
	for corner_x, corner_y in corners:
		if board_matrix[corner_x][corner_y] == 0:  # this corner is already covered
			continue
		dist_to_corner = math.inf
		for (x,y) in legal_spots:
			dist = abs(corner_x - x) + abs(corner_y - y)
			dist_to_corner = min(dist_to_corner, dist)
		min_of_corner_distances = min(min_of_corner_distances, dist_to_corner)
	return min_of_corner_distances


class BlokusCoverProblem(SearchProblem):
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
		self.targets = targets.copy()
		self.expanded = 0
		"*** YOUR CODE HERE ***"
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board
	
	def is_goal_state(self, state):
		"*** YOUR CODE HERE ***"
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
		# Note that for the search problem, there is only one player - #0
		self.expanded = self.expanded + 1
		return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]
	
	def get_cost_of_actions(self, actions):
		"""
		actions: A list of actions to take

		This method returns the total cost of a particular sequence of actions.  The sequence must
		be composed of legal moves
		"""
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()


def blokus_cover_heuristic(state, problem):
	"*** YOUR CODE HERE ***"
	


class ClosestLocationSearch:
	"""
	In this problem you have to cover all given positions on the board,
	but the objective is speed, not optimality.
	"""
	
	def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
		self.expanded = 0
		self.targets = targets.copy()
		"*** YOUR CODE HERE ***"
	
	def get_start_state(self):
		"""
		Returns the start state for the search problem
		"""
		return self.board
	
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
		"*** YOUR CODE HERE ***"
		util.raiseNotDefined()


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
