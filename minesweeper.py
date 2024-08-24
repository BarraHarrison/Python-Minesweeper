import random
import re

# Create a board to represent the game
class Board:
    def __init__(self, dim_size, num_bombs):
        # Keep track of the parameters above
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # Plant the bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()

        # Initialize a set to keep track of which locations we have already covered
        self.dug = set()  # dig at 0, 0... then self.dug = {(0,0)}

    def make_new_board(self):
        # This function constructs a new board with bombs
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        # Plant bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row = loc // self.dim_size
            col = loc % self.dim_size

            if board[row][col] == "*":
                # This means we have already planted a bomb there
                continue

            board[row][col] = "*"  # plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        # After planting bombs, assign a number 0-8 for all the empty spaces, which represents
        # how many neighboring bombs there are. We can precompute these values and avoid having to
        # do it on the fly during gameplay.
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    # If this is already a bomb, then we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        # Let's iterate through each of the neighboring positions and sum the number of bombs
        num_neighboring_bombs = 0
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if r == row and c == col:
                    # our original location
                    continue
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1

        return num_neighboring_bombs

    def dig(self, row, col):
        # Dig at that location
        # Return True if successful dig, False if bomb is dug up
        self.dug.add((row, col))  # keep track that we dug here

        if self.board[row][col] == "*":
            return False
        elif self.board[row][col] > 0:
            return True

        # self.board[row][col] == 0, so we need to dig recursively
        for r in range(max(0, row - 1), min(self.dim_size - 1, row + 1) + 1):
            for c in range(max(0, col - 1), min(self.dim_size - 1, col + 1) + 1):
                if (r, c) in self.dug:
                    continue  # don't dig where you have already dug
                self.dig(r, c)

        # If the initial dig did not hit a bomb, we should be okay
        return True

    def __str__(self):
        # Create a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = " "
        # Put this together in a string
        string_rep = ""
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        indices = [i for i in range(self.dim_size)]
        indices_row = "   "
        cells = []
        for idx, col in enumerate(indices):
            format_str = "%-" + str(widths[idx]) + "s"
            cells.append(format_str % (col))
        indices_row += "  ".join(cells)
        indices_row += "  \n"

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f"{i} |"
            cells = []
            for idx, col in enumerate(row):
                format_str = "%-" + str(widths[idx]) + "s"
                cells.append(format_str % (col))
            string_rep += "  ".join(cells)
            string_rep += "  |\n"

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + "-" * str_len + "\n" + string_rep + "-" * str_len

        return string_rep


# Play the game
def play(dim_size=10, num_bombs=10):
    # Step 1: Create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    # Step 2: Show the user the board and ask for where they want to dig
    # Step 3: If the location is a bomb, show that the game is over
    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(",(\\s)*", input("Where would you like to dig? Input as row,col: "))  # "0, 3"
        try:
            row, col = int(user_input[0]), int(user_input[-1])
            if row < 0 or row >= dim_size or col < 0 or col >= dim_size:
                raise ValueError
        except ValueError:
            print("Invalid location. Try again.")
            continue

        # If it's a valid location, dig
        if not board.dig(row, col):
            # bomb dug
            print("Game Over!")
            board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
            print(board)
            break  # game over
        if len(board.dug) == board.dim_size ** 2 - num_bombs:
            print("Congratulations! You've won!")
            break

if __name__ == '__main__':
    play()
