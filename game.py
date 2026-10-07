from board import Board
from rules import valid_move, completed_boxes

class DotsAndBoxes:
    def __init__(self):
        self.board = Board()
        self.current = 0
        self.scores = [0, 0]
        self.move_history = []

    def run(self):
        print("Dots and Boxes")
        print("Enter moves as H row col or V row col.")
        print("Rows and columns start at 0.")
        print("Example: H 0 1")

        while not self.board.is_complete():
            self.board.display(self.scores, self.current)
            raw = input(f"Player {self.current + 1}, move: ").strip().upper()
            parts = raw.split()

            if len(parts) != 3:
                print("Invalid format. Use: [H/V] [row] [col]")
                continue

            orientation, row, col = parts
            if orientation not in {"H", "V"}:
                print("Invalid orientation. Must be 'H' or 'V'.")
                continue

            if not row.isdigit() or not col.isdigit():
                print("Row and column must be numbers.")
                continue

            row, col = int(row), int(col)
            if not valid_move(self.board, orientation, row, col):
                print("Invalid or already-used move.")
                continue

            before = set(self.board.completed)
            
            # Task 2: Pass current player index to track lines in board module
            self.board.add_line(orientation, row, col, self.current)
            self.move_history.append(f"Player {self.current + 1}: {orientation} {row} {col}")

            newly_completed = completed_boxes(self.board, before)

            if newly_completed:
                self.scores[self.current] += newly_completed
                print(f"Player {self.current + 1} completed {newly_completed} box(es) and plays again.")
            else:
                self.current = 1 - self.current

        self.board.display(self.scores, self.current)
        print("Game over!")
        
        # Display match statistics summary
        print("\n--- Match Statistics & Summary ---")
        print(f"Total Lines Drawn -> P1: {self.board.lines_drawn[0]}, P2: {self.board.lines_drawn[1]}")
        print("\nMove History:")
        for move in self.move_history:
            print(move)
        print("-" * 34)

        if self.scores[0] == self.scores[1]:
            print("The game is a draw.")
        else:
            winner = 1 if self.scores[0] > self.scores[1] else 2
            print(f"Player {winner} wins!")