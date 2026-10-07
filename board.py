class Board:
    def __init__(self, rows=4, cols=4):
        self.rows = rows
        self.cols = cols
        # Horizontal lines: rows+1 rows of cols segments
        self.horizontal = [[False] * cols for _ in range(rows + 1)]
        # Vertical lines: rows rows of cols+1 segments
        self.vertical = [[False] * (cols + 1) for _ in range(rows)]
        self.completed = set()
        # Track lines drawn by each player
        self.lines_drawn = [0, 0]

    def add_line(self, orientation, row, col, player_idx=0):
        if orientation == "H":
            self.horizontal[row][col] = True
        elif orientation == "V":
            self.vertical[row][col] = True
        self.lines_drawn[player_idx] += 1
        self._update_completed()

    def _update_completed(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (
                    self.horizontal[r][c]
                    and self.horizontal[r + 1][c]
                    and self.vertical[r][c]
                    and self.vertical[r][c + 1]
                ):
                    self.completed.add((r, c))

    def is_complete(self):
        total_horizontal = (self.rows + 1) * self.cols
        total_vertical = self.rows * (self.cols + 1)
        total = total_horizontal + total_vertical
        used_horizontal = sum(sum(row) for row in self.horizontal)
        used_vertical = sum(sum(row) for row in self.vertical)
        return (used_horizontal + used_vertical) == total

    def display(self, scores, current):
        print()
        print(f"Scores: P1={scores[0]} (Lines: {self.lines_drawn[0]}) | "
              f"P2={scores[1]} (Lines: {self.lines_drawn[1]}) | Turn: P{current + 1}")

        for r in range(self.rows + 1):
            # Draw horizontal edges row
            print("o" + "".join(("───o" if self.horizontal[r][c] else "   o") for c in range(self.cols)))
            if r < self.rows:
                # Draw vertical edges row
                middle = []
                for c in range(self.cols + 1):
                    wall = "│" if self.vertical[r][c] else " "
                    middle.append(wall)
                    if c < self.cols:
                        middle.append(" " + ("X" if (r, c) in self.completed else " ") + " ")
                print("".join(middle))
        print()
