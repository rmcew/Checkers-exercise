import Checkers
import unittest
import os


os.environ["SDL_VIDEODRIVER"] = "dummy"

class TestCheckers(unittest.TestCase):
	def test_vertical_win(self):
		gameTest = Checkers.Game()
		gameTest.board.insert_piece(*(5,0), (255,   0,   0))
		gameTest.board.insert_piece(*(5,1), (255,   0,   0))
		gameTest.board.insert_piece(*(5,2), (255,   0,   0))
		gameTest.board.insert_piece(*(5,3), (255,   0,   0))
		

		res = gameTest.board.check_win()
		#gameTest.main()
		self.assertTrue(res)	

	def test_horizontal_win(self):
		gameTest = Checkers.Game()
		gameTest.board.insert_piece(*(2,5), (255,   0,   0))
		gameTest.board.insert_piece(*(3,5), (255,   0,   0))
		gameTest.board.insert_piece(*(4,5), (255,   0,   0))
		gameTest.board.insert_piece(*(5,5), (255,   0,   0))

		res = gameTest.board.check_win()
		self.assertTrue(res)
	#def test_pos_diagonal_win(self):
		#gameTest = Checkers.Game():
		#gameTest.board.insert_piece(*(0,3), (255,   0,   0))

		

	def test_no_win(self):
		gameTest = Checkers.Game()
		gameTest.board.insert_piece(*(0,0), (255,   0,   0))
		gameTest.board.insert_piece(*(0,2), (255,   0,   0))
		gameTest.board.insert_piece(*(0,5), (255,   0,   0))
		gameTest.board.insert_piece(*(0,6), (255,   0,   0))
		gameTest.board.insert_piece(*(0,7), (255,   0,   0))
		gameTest.board.insert_piece(*(1,1), (255,   0,   0))
		gameTest.board.insert_piece(*(4,5), (255,   0,   0))
		gameTest.board.insert_piece(*(2,5), (255,   0,   0))


		res = gameTest.board.check_win()
		#gameTest.main()
		self.assertFalse(res)	

if __name__ == "__main__":
	unittest.main()
