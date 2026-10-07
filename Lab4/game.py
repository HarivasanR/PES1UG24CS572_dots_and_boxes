from board import Board
from rules import valid_move, completed_boxes

class DotsAndBoxes:
    def __init__(self):
        # Configured for 4x4 grid as tested
        self.board = Board(rows=4, cols=4)
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
            
            try:
                raw = input(f"Player {self.current + 1}, move: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nGame exited safely.")
                break

            if not raw:
                print("Empty input. Please enter a move.")
                continue

            parts = raw.upper().split()

            # Task 3 Robustness: Handle malformed commands (too many or too few arguments)
            if len(parts) != 3:
                print("Invalid format. Please use the format: [H/V] [row] [col] (e.g., H 0 1)")
                continue

            orientation, row_str, col_str = parts

            # Task 3 Robustness: Validate orientation
            if orientation not in {"H", "V"}:
                print("Invalid orientation. Must be 'H' for horizontal or 'V' for vertical.")
                continue

            # Task 3 Robustness: Safely handle non-integer or negative coordinates using try-except
            try:
                row = int(row_str)
                col = int(col_str)
            except ValueError:
                print("Invalid coordinates. Row and column must be valid integers.")
                continue

            if row < 0 or col < 0:
                print("Coordinates cannot be negative.")
                continue

            # Task 3 Robustness: Validate move boundaries and duplicate lines without corrupting board/score
            if not valid_move(self.board, orientation, row, col):
                print("Invalid or already-used move / Out of grid bounds. Try again.")
                continue

            # State update (guaranteed safe from corruption due to prior checks)
            before = set(self.board.completed)
            self.board.add_line(orientation, row, col, self.current)
            self.move_history.append(f"Player {self.current + 1}: {orientation} {row} {col}")

            newly_completed = completed_boxes(self.board, before)

            if newly_completed:
                self.scores[self.current] += newly_completed
                print(f"Player {self.current + 1} completed {newly_completed} box(es) and plays again.")
            else:
                self.current = 1 - self.current

        # End of game state
        self.board.display(self.scores, self.current)
        print("Game over!")
        
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