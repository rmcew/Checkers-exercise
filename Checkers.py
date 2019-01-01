"""
checkers.py
A simple checkers engine written in Python with the pygame 1.9.1 libraries.
Here are the rules I am using: http://boardgames.about.com/cs/checkersdraughts/ht/play_checkers.htm
I adapted some code from checkers.py found at 
http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py starting on line 159 of my program.
This is the final version of my checkers project for Programming Workshop at Marlboro College. The entire thing has been rafactored and made almost completely object oriented.
Funcitonalities include:
- Having the pieces and board drawn to the screen
- The ability to move pieces by clicking on the piece you want to move, then clicking on the square you would
  like to move to. You can change you mind about the piece you would like to move, just click on a new piece of yours.
- Knowledge of what moves are legal. When moving pieces, you'll be limited to legal moves.
- Capturing
- DOUBLE capturing etc.
- Legal move and captive piece highlighting
- Turn changes
- Automatic kinging and the ability for them to move backwords
- Automatic check for and end game. 
- A silky smoooth 60 FPS!
Everest Witman - May 2014 - Marlboro College - Programming Workshop 
"""

import pygame, sys
import math
from itertools import groupby, chain
from collections import defaultdict
from operator import itemgetter
from pygame.locals import *
import unittest

pygame.font.init()

##COLORS##
#             R    G    B 
WHITE    = (255, 255, 255)
BLUE     = (  0,   0, 255)
RED      = (255,   0,   0)
BLACK    = (  0,   0,   0)
GOLD     = (255, 215,   0)
HIGH     = (160, 190, 255)

NONE = '.'

##DIRECTIONS##
NORTHWEST = "northwest"
NORTHEAST = "northeast"
SOUTHWEST = "southwest"
SOUTHEAST = "southeast"

class Game:
	"""
	The main game control.
	"""

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		self.piece_color = RED
		self.selected_piece = None # a board location. 


	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()

	def event_loop(self):
		"""
		The event loop. This is where events are triggered 
		(like a mouse click) and then effect the game state.
		"""
		self.mouse_pos = self.graphics.board_coords(*pygame.mouse.get_pos()) # what square is the mouse in?


		for event in pygame.event.get():

			if event.type == QUIT:
				self.terminate_game()

			if event.type == MOUSEBUTTONDOWN:
				if self.board.location(*self.mouse_pos).occupant == None:
					self.board.insert_piece(*self.mouse_pos, self.piece_color)
					self.board.checkForWin()
					

				else: 
					self.board.remove_piece(*self.mouse_pos)

			if event.type == KEYDOWN:
				if event.key == pygame.K_b:
					self.graphics.draw_message("blue")
					self.piece_color = BLUE
					
				if event.key == pygame.K_r:
					self.piece_color = RED



	def update(self):
		"""Calls on the graphics class to update the game display."""
		self.graphics.update_display(self.board, self.selected_piece)

	def terminate_game(self):
		"""Quits the program and ends the game."""
		pygame.quit()
		sys.exit

	def main(self):
		""""This executes the game and controls its flow."""
		self.setup()

		while True: # main game loop
			self.event_loop()
			self.update()



class Graphics:
	def __init__(self):
		self.caption = "Checkers"
		self.fps = 60
		self.clock = pygame.time.Clock()
		self.window_size = 600
		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.background = pygame.image.load('resources/board.png')
		self.square_size = self.window_size / 8
		self.piece_size = self.square_size / 2
		self.message = False

	def setup_window(self):
		"""
		This initializes the window and sets the caption at the top.
		"""
		pygame.init()
		pygame.display.set_caption(self.caption)

	def update_display(self, board, selected_piece):
		"""
		This updates the current display.
		"""
		self.screen.blit(self.background, (0,0))

		self.draw_board_pieces(board)

		if self.message:
			self.screen.blit(self.text_surface_obj, self.text_rect_obj)

		pygame.display.update()
		self.clock.tick(self.fps)

	def draw_board_squares(self, board):
		"""
		Takes a board object and draws all of its squares to the display
		"""
		for x in range(8):
			for y in range(8):
				pygame.draw.rect(self.screen, board[x][y].color, (x * self.square_size, y * self.square_size, self.square_size, self.square_size), )
	
	def draw_board_pieces(self, board):
		"""
		Takes a board object and draws all of its pieces to the display
		"""
		for x in range(8):
			for y in range(8):
				if board.matrix[x][y].occupant != None:					
					pygame.draw.circle(self.screen, board.matrix[x][y].occupant.color, (self.pixel_coords((x,y))), math.floor(self.piece_size)) 


	def pixel_coords(self, board_coords):
		"""
		Takes in a tuple of board coordinates (x,y) 
		and returns the pixel coordinates of the center of the square at that location.
		"""
		return (math.floor(board_coords[0] * self.square_size + self.piece_size), math.floor(board_coords[1] * self.square_size + self.piece_size))

	def board_coords(self, pixel_x, pixel_y):
		"""
		Does the reverse of pixel_coords(). Takes in a tuple of of pixel coordinates and returns what square they are in.
		"""
		return (math.floor(pixel_x / self.square_size), math.floor(pixel_y / self.square_size))	


	def draw_message(self, message):
		"""
		Draws message to the screen. 
		"""
		self.message = True
		self.font_obj = pygame.font.Font('freesansbold.ttf', 44)
		self.text_surface_obj = self.font_obj.render(message, True, HIGH, BLACK)
		self.text_rect_obj = self.text_surface_obj.get_rect()
		self.text_rect_obj.center = (self.window_size / 2, self.window_size / 2)

class Board:
	def __init__(self):
		self.matrix = self.new_board()
		self.consecutive = 0
		self.win = 4 # number of pieces required to win
		self.positive_diagonals = self.pos_diagonal_list()
		self.negative_diagonals = self.neg_diagonal_list()
		
	def new_board(self):
		"""
		Create a new board matrix.
		"""

		# initialize squares and place them in matrix

		matrix = [[None] * 8 for i in range(8)]

		# The following code block has been adapted from
		# http://itgirl.dreamhosters.com/itgirlgames/games/Program%20Leaders/ClareR/Checkers/checkers.py
		for x in range(8):
			for y in range(8):
				if (x % 2 != 0) and (y % 2 == 0):
					matrix[y][x] = Square(WHITE)	
				elif (x % 2 != 0) and (y % 2 != 0):
					matrix[y][x] = Square(BLACK)
				elif (x % 2 == 0) and (y % 2 != 0):
					matrix[y][x] = Square(WHITE)
				elif (x % 2 == 0) and (y % 2 == 0): 
					matrix[y][x] = Square(BLACK)

		# initialize each square occupant to null



		return matrix

	def board_string(self, board):
		"""
		Takes a board and returns a matrix of the board space colors. Used for testing new_board()
		"""

		board_string = [[None] * 8] * 8 

		for x in range(8):
			for y in range(8):
				if board[x][y].color == WHITE:
					board_string[x][y] = "WHITE"
				else:
					board_string[x][y] = "BLACK"


		return board_string
	
	def rel(self, dir, x,y):
		"""
		Returns the coordinates one square in a different direction to (x,y).
		===DOCTESTS===
		>>> board = Board()
		>>> board.rel(NORTHWEST, (1,2))
		(0,1)
		>>> board.rel(SOUTHEAST, (3,4))
		(4,5)
		>>> board.rel(NORTHEAST, (3,6))
		(4,5)
		>>> board.rel(SOUTHWEST, (2,5))
		(1,6)
		"""
		if dir == NORTHWEST:
			return (x - 1, y - 1)
		elif dir == NORTHEAST:
			return (x + 1, y - 1)
		elif dir == SOUTHWEST:
			return (x - 1, y + 1)
		elif dir == SOUTHEAST:
			return (x + 1, y + 1)
		else:
			return 0

	def checkForWin (self):



		self.check_diagonals()
		if (self.prototype_check()):
			print("True")
			return True

		return False
		#self.checkHorizontalWin(red_pieces)
		#self.checkVerticalWin(red_pieces)
		#self.check_pos_diag_win(red_pieces)
		#self.checkPositiveDiagonalWin(red_pieces)
		#self.checkNegativeDiagonalWin(red_pieces)

	def check_diagonals(self):
		consecutive = 1
		occupantColor = None
		for y in range (3,8):
			print(self.adjacent(0, y)[1])

	def prototype_check(self):
		currentColColor = None
		consecutiveCol = 1
		currentRowColor = None
		consecutiveRow = 1

		for x in range(8):
			for y in range(8):
				if (self.matrix[x][y].occupant != None):
					if(currentColColor == self.matrix[x][y].occupant.color):
						consecutiveCol += 1
					else:
						currentColColor = self.matrix[x][y].occupant.color
						
				else:
					currentColColor = None
					consecutiveCol = 1

				if (consecutiveCol >= 4):
					return True

				if (self.matrix[y][x].occupant != None):
					if(currentRowColor == self.matrix[y][x].occupant.color):

						consecutiveRow += 1
					else:
						currentRowColor = self.matrix[y][x].occupant.color

				else:
					currentRowColor = None
					consecutiveRow = 1

				if(consecutiveRow >= 4):
					return True

			
		return False
		

	def pos_diagonal_list(self):	
		diagGroups = []
		diagGroups.append(((0,3), (1,2), (2,1), (3,0)))
		diagGroups.append(((0,4), (1,3), (2,2), (3,1), (4,0)))
		diagGroups.append(((0,5), (1,4), (2,3), (3,2), (4,1), (5,0)))
		diagGroups.append(((0,6), (1,5), (2,4), (3,3), (4,2), (5,1), (6,0)))
		diagGroups.append(((0,7), (1,6), (2,5), (3,4), (4,3), (5,2), (6,1), (7,0)))
		diagGroups.append(((1,7), (2,6), (3,5), (4,4), (5,3), (6,2), (7,1)))
		diagGroups.append(((2,7), (3,6), (4,5), (5,4), (6,3), (7,2)))
		diagGroups.append(((3,7), (4,6), (5,5), (6,4), (7,3)))
		diagGroups.append(((4,7), (5,6), (6,5), (7,4)))

		return diagGroups

	def neg_diagonal_list(self):
		diagGroups = []
		diagGroups.append(((7,3), (6,2), (5,1), (4,0)))
		diagGroups.append(((7,4), (6,3), (5,2), (4,1), (3,0)))
		diagGroups.append(((7,5), (6,4), (5,3), (4,2), (3,1), (2,0)))
		diagGroups.append(((7,6), (6,5), (5,4), (4,3), (3,2), (2,1), (1,0)))
		diagGroups.append(((7,7), (6,6), (5,5), (4,4), (3,3), (2,2), (1,1), (0,0)))
		diagGroups.append(((6,7), (5,6), (4,5), (3,4), (2,3), (1,2), (0,1)))
		diagGroups.append(((5,7), (4,6), (3,5), (2,4), (1,3), (0,2)))
		diagGroups.append(((4,7), (3,6), (2,5), (1,4), (0,3)))
		diagGroups.append(((3,7), (2,6), (1,5), (0,4)))
		
		return diagGroups





	def adjacent(self, x,y):
		"""
		Returns a list of squares locations that are adjacent (on a diagonal) to (x,y).
		"""

		return [self.rel(NORTHWEST, *(x,y)), self.rel(NORTHEAST, *(x,y)),self.rel(SOUTHWEST, *(x,y)),self.rel(SOUTHEAST, *(x,y))]

	def location(self, x,y):
		"""
		Takes a set of coordinates as arguments and returns self.matrix[x][y]
		This can be faster than writing something like self.matrix[coords[0]][coords[1]]
		"""
		return self.matrix[math.floor(x)][math.floor(y)]

	def remove_piece(self, x,y):
		"""
		Removes a piece from the board at position (x,y). 
		"""
		self.matrix[x][y].occupant = None

	def move_piece(self, start_x, start_y, end_x, end_y):
		"""
		Move a piece from (start_x, start_y) to (end_x, end_y).
		"""

		self.matrix[end_x][end_y].occupant = self.matrix[start_x][start_y].occupant
		self.remove_piece((start_x, start_y))

	def insert_piece(self, x, y, piece_color):
		"""
		Place a piece at (end_x, end_x)
		"""
		self.matrix[math.floor(x)][math.floor(y)].occupant = Piece(piece_color)

		#self.remove_piece((start_x, start_y))

	def has_piece(self, x, y):

		if (hasattr(self.matrix[x][y].occupant, 'color')):
			return True

		else:
			return False

	def is_end_square(self, coords):
		"""
		Is passed a coordinate tuple (x,y), and returns true or 
		false depending on if that square on the board is an end square.
		===DOCTESTS===
		>>> board = Board()
		>>> board.is_end_square((2,7))
		True
		>>> board.is_end_square((5,0))
		True
		>>>board.is_end_square((0,5))
		False
		"""

		if coords[1] == 0 or coords[1] == 7:
			return True
		else:
			return False

	def on_board(self, x,y):
		"""
		Checks to see if the given square (x,y) lies on the board.
		If it does, then on_board() return True. Otherwise it returns false.
		===DOCTESTS===
		>>> board = Board()
		>>> board.on_board((5,0)):
		True
		>>> board.on_board(-2, 0):
		False
		>>> board.on_board(3, 9):
		False
		"""

		if x < 0 or y < 0 or x > 7 or y > 7:
			return False
		else:
			return True


class Piece:
	def __init__(self, color, king = False):
		self.color = color
		self.king = king

class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Square object

def main():
	game = Game()
	game.main()



if __name__ == "__main__":
	main()
	unittest.main()


