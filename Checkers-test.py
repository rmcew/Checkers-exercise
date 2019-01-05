import Checkers
import unittest
import os


#os.environ["SDL_VIDEODRIVER"] = "dummy"	#creates dummy video driver so automated testing can be done

class TestCheckers(unittest.TestCase):
	def test_vertical_win(self):
		gameTest = Checkers.Game()
		gameTest.board.insert_piece(*(5,0), (255,   0,   0))
		gameTest.board.insert_piece(*(5,1), (255,   0,   0))
		gameTest.board.insert_piece(*(5,2), (255,   0,   0))
		gameTest.board.insert_piece(*(5,3), (255,   0,   0))
		

		res = gameTest.board.check_win()
		self.assertTrue(res)	

	def test_horizontal_win(self):
		gameTest = Checkers.Game()
		gameTest.board.insert_piece(*(2,5), (255,   0,   0))
		gameTest.board.insert_piece(*(3,5), (255,   0,   0))
		gameTest.board.insert_piece(*(4,5), (255,   0,   0))
		gameTest.board.insert_piece(*(5,5), (255,   0,   0))

		res = gameTest.board.check_win()
		self.assertTrue(res)

	def test_pos_diagonal_win(self):
		gameTest = Checkers.Game()
		gameTest.board.insert_piece(*(0,5), (255,   0,   0))
		gameTest.board.insert_piece(*(1,4), (255,   0,   0))
		gameTest.board.insert_piece(*(2,3), (255,   0,   0))
		gameTest.board.insert_piece(*(3,2), (255,   0,   0))

		res = gameTest.board.check_win()
		self.assertTrue(res)		

	def test_neg_diagonal_win(self):
		gameTest = Checkers.Game()
		gameTest.board.insert_piece(*(3,3), (255,   0,   0))
		gameTest.board.insert_piece(*(4,4), (255,   0,   0))
		gameTest.board.insert_piece(*(5,5), (255,   0,   0))
		gameTest.board.insert_piece(*(6,6), (255,   0,   0))

		res = gameTest.board.check_win()
		self.assertTrue(res)

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
		gameTest.board.insert_piece(*(1,3), (255,   0,   0))
		gameTest.board.insert_piece(*(4,0), (255,   0,   0))
		gameTest.board.insert_piece(*(5,0), (255,   0,   0))
		gameTest.board.insert_piece(*(6,0), (255,   0,   0))
		gameTest.board.insert_piece(*(4,1), (255,   0,   0))
		gameTest.board.insert_piece(*(5,1), (255,   0,   0))
		gameTest.board.insert_piece(*(6,1), (255,   0,   0))
		gameTest.board.insert_piece(*(1,6), (255,   0,   0))
		gameTest.board.insert_piece(*(2,5), (255,   0,   0))
		gameTest.board.insert_piece(*(4,7), (255,   0,   0))
		gameTest.board.insert_piece(*(5,7), (255,   0,   0))
		gameTest.board.insert_piece(*(6,7), (255,   0,   0))
		gameTest.board.insert_piece(*(4,6), (255,   0,   0))
		gameTest.board.insert_piece(*(5,6), (255,   0,   0))
		gameTest.board.insert_piece(*(6,6), (255,   0,   0))		

		gameTest.board.insert_piece(*(0,1), (  0,   0,   0))
		gameTest.board.insert_piece(*(0,3), (  0,   0,   0))
		gameTest.board.insert_piece(*(0,4), (  0,   0,   0))
		gameTest.board.insert_piece(*(2,2), (  0,   0,   0))
		gameTest.board.insert_piece(*(3,3), (  0,   0,   0))
		gameTest.board.insert_piece(*(4,4), (  0,   0,   0))


		res = gameTest.board.check_win()
		#gameTest.main()
		self.assertFalse(res)	

if __name__ == "__main__":
	unittest.main()
