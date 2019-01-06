import Checkers
import unittest
import os


os.environ["SDL_VIDEODRIVER"] = "dummy"	#creates dummy video driver so automated testing can be done

class TestCheckers(unittest.TestCase):
	gameTest = Checkers.Game()

	def setUp(self):
		pass

	def test_vertical_win(self):
		__class__.gameTest.board.insert_piece(*(5,0), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,1), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,2), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,3), (255,   0,   0))

		res = __class__.gameTest.board.check_win()
		self.assertTrue(res)	

		__class__.gameTest.reset()

	def test_horizontal_win(self):
		__class__.gameTest.board.insert_piece(*(2,5), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(3,5), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,5), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,5), (255,   0,   0))

		res = __class__.gameTest.board.check_win()
		self.assertTrue(res)

		__class__.gameTest.reset()

	def test_pos_diagonal_win(self):
		__class__.gameTest.board.insert_piece(*(0,5), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(1,4), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(2,3), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(3,2), (255,   0,   0))

		res = __class__.gameTest.board.check_win()
		self.assertTrue(res)		

		__class__.gameTest.reset()

	def test_neg_diagonal_win(self):
		__class__.gameTest.board.insert_piece(*(3,3), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,4), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,5), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(6,6), (255,   0,   0))

		res = __class__.gameTest.board.check_win()
		self.assertTrue(res)

		__class__.gameTest.reset()

	def test_no_win(self):
		__class__.gameTest.board.insert_piece(*(0,0), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(0,2), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(0,5), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(0,6), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(0,7), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(1,1), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,5), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(1,3), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,0), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,0), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(6,0), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,1), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,1), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(6,1), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(1,6), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,7), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,7), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(6,7), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,6), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(5,6), (255,   0,   0))
		__class__.gameTest.board.insert_piece(*(6,6), (255,   0,   0))		

		__class__.gameTest.board.insert_piece(*(0,1), (  0,   0,   0))
		__class__.gameTest.board.insert_piece(*(0,3), (  0,   0,   0))
		__class__.gameTest.board.insert_piece(*(0,4), (  0,   0,   0))
		__class__.gameTest.board.insert_piece(*(2,2), (  0,   0,   0))
		__class__.gameTest.board.insert_piece(*(3,3), (  0,   0,   0))
		__class__.gameTest.board.insert_piece(*(4,4), (  0,   0,   0))


		res = __class__.gameTest.board.check_win()
		#__class__.gameTest.main()
		self.assertFalse(res)	

		__class__.gameTest.reset()
		#def test_horiz_wrap(self):
			#__class__.gameTest = Checkers.Game()

if __name__ == "__main__":
	unittest.main()
