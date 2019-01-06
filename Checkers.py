"""
checkers.py
A sandbox checkers board where you can place checkers anywhere and the program will check if there are 4 of the same colors in a row vertically, horizontally, or diagonally.
I adapted some code from checkers.py found at:
https://github.com/everestwitman/Pygame-Checkers/blob/master/checkers.py

Ross McEwen - January 2019
"""

import pygame, sys
import math
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


class Game:
	"""
	The main game control.
	"""

	def __init__(self):
		self.graphics = Graphics()
		self.board = Board()
		self.piece_color = RED
		self.game_won = False


	def setup(self):
		"""Draws the window and board at the beginning of the game"""
		self.graphics.setup_window()

	def reset(self):
		self.graphics = Graphics()
		self.board = Board()
		self.piece_color = RED
		self.game_won = False

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
				if (self.game_won):
					self.reset()
					continue

				if(self.graphics.message):
					self.graphics.message = False
				if self.board.location(*self.mouse_pos).occupant == None:
					self.board.insert_piece(*self.mouse_pos, self.piece_color)
					
					if(self.board.check_win()):
						if(self.piece_color == RED):
							message_string = "Red Wins! Click to reset"
						elif(self.piece_color == BLACK):
							message_string = "Black Wins! Click to reset"
						
						self.game_won = True
						self.graphics.draw_message(message_string)
										

				else: 
					self.board.remove_piece(*self.mouse_pos)

			if event.type == KEYDOWN:
				if event.key == pygame.K_b:
					self.graphics.draw_message("Black")
					self.piece_color = BLACK
					
				if event.key == pygame.K_r:
					self.graphics.draw_message("Red")
					self.piece_color = RED



	def update(self):
		"""Calls on the graphics class to update the game display."""
		self.graphics.update_display(self.board)

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
		self.fps = 30
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

	def update_display(self, board):
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
		self.positive_diagonals = self.get_pos_diagonals()
		self.negative_diagonals = self.get_neg_diagonals()		
		
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
	


	def check_win(self):
		"""
		Calls appropriate functions to check for horizontal, vertical, or
		diagonal wins. Returns true if any of these return true
		"""
		
		if (self.check_col_row_win()):
			return True
		elif (self.check_diagional_win(self.positive_diagonals)):
			return True
		elif (self.check_diagional_win(self.negative_diagonals)):
			return True

		return False


	def check_col_row_win(self):
		"""
		Iterates through occupied squares and counts the number of consecutive
		same-colored squares. Returns true if it finds 4 or more consecutive in 
		a single row or column
		"""

		for x in range(8):
			currentRowColor = None
			consecutiveRow = 1			
			currentColColor = None
			consecutiveCol = 1					
			for y in range(8):
		
				"""
				Column Check
				"""
				if (self.matrix[x][y].is_occupied()):
					if(currentColColor == self.matrix[x][y].occupant.color):
						consecutiveCol += 1					

					else:
						currentColColor = self.matrix[x][y].occupant.color
						consecutiveCol = 1
						
				else:
					currentColColor = None
					consecutiveCol = 1

				if (consecutiveCol >= 4):
					return True

				"""
				Row Check
				"""
				if (self.matrix[y][x].is_occupied()):
					if(currentRowColor == self.matrix[y][x].occupant.color):
						consecutiveRow += 1

					else:
						currentRowColor = self.matrix[y][x].occupant.color
						consecutiveRow = 1

				else:
					currentRowColor = None
					consecutiveRow = 1

				if(consecutiveRow >= 4):
					return True

		return False


	def check_diagional_win(self, diagonals):
		"""
		Iterates through list of diagonals. Returns True if four consecutive diagonal tiles have the same color
		"""


		for diagonal in diagonals:
			consecutive = 1
			currentColor = None			
			for coords in diagonal:
				x = coords[0]
				y = coords[1]


				if(self.matrix[x][y].is_occupied()):
					if(currentColor == self.matrix[x][y].occupant.color):	
						consecutive += 1

					else:
						currentColor = self.matrix[x][y].occupant.color
						consecutive = 1

				else:
					currentColor = None
					consecutive = 1

				if(consecutive >= 4):
					return True

		return False						


	def get_pos_diagonals(self):
		"""
		Returns a list of positive diagonals separated into groups
		"""
		diagGroups = []

		for y in range(3,8):
			x = 0

			currentGroup = []
			while(self.is_end_square(x, y) == False):
				currentGroup.append((x,y))
				x += 1
				y -= 1
			diagGroups.append((currentGroup))

		for x in range(1,5):
			y = 7
			currentGroup = []
			while(self.is_end_square(x, y) == False):
				currentGroup.append((x,y))
				x += 1
				y -= 1

			diagGroups.append((currentGroup))

		return diagGroups

	def get_neg_diagonals(self):
		"""
		Returns a list of positive diagonals separated into groups
		"""		
		diagGroups = []

		for y in range(0,4):
			x = 0

			currentGroup = []
			while(self.is_end_square(x, y) == False):
				currentGroup.append((x,y))
				x += 1
				y += 1

			diagGroups.append((currentGroup))

		for x in range(1,5):
			y = 0
			currentGroup = []
			while(self.is_end_square(x, y) == False):
				currentGroup.append((x,y))
				x += 1
				y += 1

			diagGroups.append((currentGroup))
		return diagGroups


	def is_end_square(self, x, y):
		"""
		Returns true if the square at the provided (x,y) coordinates is on the edge of the board
		"""
		if((x < 0 or y < 0) or (x >= 8 or y >= 8)):
			return True

		else:
			return False


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


	def insert_piece(self, x, y, piece_color):
		"""
		Place a piece at (end_x, end_x)
		"""
		self.matrix[math.floor(x)][math.floor(y)].occupant = Piece(piece_color)


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
	def __init__(self, color):
		self.color = color
		
class Square:
	def __init__(self, color, occupant = None):
		self.color = color # color is either BLACK or WHITE
		self.occupant = occupant # occupant is a Piece object


	def is_occupied(self):
		"""
		Returns True if square at provided (x,y) coordinates is occupied
		"""

		if(self.occupant == None):
			return False

		return True



def main():
	game = Game()
	game.main()



if __name__ == "__main__":
	main()


