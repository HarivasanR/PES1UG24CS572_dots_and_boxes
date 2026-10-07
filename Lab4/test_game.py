import unittest
from board import Board
from rules import valid_move, completed_boxes

class TestDotsAndBoxes(unittest.TestCase):
    def setUp(self):
        # Configured to match your 4x4 grid setup
        self.board = Board(rows=4, cols=4)

    def test_valid_horizontal_move(self):
        self.assertTrue(valid_move(self.board, "H", 0, 0))

    def test_valid_vertical_move(self):
        self.assertTrue(valid_move(self.board, "V", 0, 0))

    def test_invalid_repeated_move(self):
        # Test repeated move: add valid line once, then check valid_move returns False
        self.board.add_line("H", 0, 0, 0)
        self.assertFalse(valid_move(self.board, "H", 0, 0))

    def test_invalid_out_of_bounds_move(self):
        # Test out-of-bounds coordinates return False
        self.assertFalse(valid_move(self.board, "H", 10, 10))

    def test_box_completion(self):
        before = set(self.board.completed)
        self.board.add_line("H", 0, 0, 0)
        self.board.add_line("V", 0, 0, 0)
        self.board.add_line("V", 0, 1, 0)
        self.board.add_line("H", 1, 0, 0)
        newly_completed = completed_boxes(self.board, before)
        self.assertEqual(newly_completed, 1)
        self.assertIn((0, 0), self.board.completed)

    def test_end_of_game_condition(self):
        self.assertFalse(self.board.is_complete())
        
        # Fill all lines programmatically
        for r in range(self.board.rows + 1):
            for c in range(self.board.cols):
                if not self.board.horizontal[r][c]:
                    self.board.add_line("H", r, c, 0)
        for r in range(self.board.rows):
            for c in range(self.board.cols + 1):
                if not self.board.vertical[r][c]:
                    self.board.add_line("V", r, c, 0)
                    
        self.assertTrue(self.board.is_complete())

if __name__ == "__main__":
    unittest.main()