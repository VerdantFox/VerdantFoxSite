import random


def set_game():
    p1 = Player("red", "player 1", turn=True)
    p2 = Player("blue", "robot")
    board = Grid(p1, p2)
    robot = AI(ai=p2, opponent=p1, grid=board, Grid=Grid)
    message = None
    error = None
    deactivate = False
    restart = False
    p1_col = None
    p1_row = None
    p2_col = None
    p2_row = None
    p1_move_msg = None
    p2_move_msg = None
    return (
        p1,
        p2,
        board,
        robot,
        message,
        error,
        deactivate,
        restart,
        p1_col,
        p1_row,
        p2_col,
        p2_row,
        p1_move_msg,
        p2_move_msg,
    )


class Player:
    def __init__(self, color, name, turn=False):
        self.color = color
        self.name = name
        self.won = False
        self.turn = turn


class AI:
    def __init__(self, ai, opponent, grid, Grid):
        self.ai = ai
        self.color = ai.color
        self.opponent = opponent
        self.opponent_color = self.opponent.color
        # Actual game board
        self.grid = grid
        # 7 test game boards for looking 1 move into the future
        self.grid_list = []
        for i in range(7):
            self.grid_list.append(Grid(opponent, ai))

    def decide_move(self):
        self.set_test_grids()
        self.make_all_legal_moves(self.opponent)
        col_4_opponent = self.four_in_row()
        self.set_test_grids()
        self.make_all_legal_moves(self.ai)
        col_4_ai = self.four_in_row()
        col_random = self.move_random()

        if col_4_ai is not None:
            print("Winning the game!")
            return col_4_ai
        elif col_4_opponent is not None:
            print("col_4_opponent condition met")
            return col_4_opponent
        else:
            print("Making a random move")
            return col_random

    # Win the game or block game win if possible
    def four_in_row(self):
        for column, test_grid in enumerate(self.grid_list):
            check_win = test_grid.check_winner()
            if check_win:
                return column
            else:
                pass
        return None

    # Make random legal move move
    def move_random(self):
        available_columns = []
        for column in range(7):
            legal_column = self.grid.check_bottom(column)
            if legal_column is not None:
                available_columns.append(column)
        return random.choice(available_columns)

    # Set test grid to real grid
    def set_test_grids(self):
        for test_grid in self.grid_list:
            for row in range(6):
                for column in range(7):
                    test_grid.grid[row][column] = self.grid.grid[row][column]

    # Make all legal moves for given player (AI or opponent)
    def make_all_legal_moves(self, player):
        for column, test_grid in enumerate(self.grid_list):
            row = test_grid.check_bottom(column)
            if row is not None:
                test_grid.change_color(row, column, player.color)
            else:
                pass


class Grid:
    def __init__(self, player1, player2):
        # Create connect 4 grid system
        grid = []
        for i in range(6):
            grid.append([])

        for row in grid:
            for j in range(7):
                row.append("empty")
        self.grid = grid
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        # Was getting weird results using range(7)
        self.columns = [0, 1, 2, 3, 4, 5, 6]

    def show_grid(self):
        print("[   0        1        2        3        4        5        6   ]")
        for row in self.grid:
            print(row)

    # Change color of a circle
    def change_color(self, row, column, color):
        self.grid[row][column] = color

    def change_win_colors(self, win_coordinates, color):
        win_color = f"{color}-green"
        for coord in win_coordinates:
            self.grid[coord[0]][coord[1]] = win_color

    # Change player's turn
    def change_turn(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        elif self.current_player == self.player2:
            self.current_player = self.player1

    # Report the current color of a circle
    def report_color(self, row, column):
        try:
            return self.grid[row][column]
        # Any out of range index counts as empty
        except IndexError:
            return "empty"

    # Check for bottom of column
    def check_bottom(self, column):
        for rev_row in range(7):
            if self.grid[5 - rev_row][column] == "empty":
                return 5 - rev_row
        # Row is full
        return None

    # Check if 4 circles' colors' match
    def check_match4(self, color1, color2, color3, color4):
        if color1 == color2 == color3 == color4 != "empty":
            return True
        else:
            return False

    # Check for winner
    def check_winner(self):
        horizontal_win = self.horizontal_win_check()
        veritcal_win = self.vertical_win_check()
        diagonal_win = self.diagonal_win_check()
        if horizontal_win:
            print(horizontal_win)
            return horizontal_win
        elif veritcal_win:
            print(veritcal_win)
            return veritcal_win
        elif diagonal_win:
            print(diagonal_win)
            return diagonal_win
        else:
            return None

    # Check horizontal win
    def horizontal_win_check(self):
        for row in range(6):
            for col in range(4):
                if self.check_match4(
                    self.report_color(row, col),
                    self.report_color(row, col + 1),
                    self.report_color(row, col + 2),
                    self.report_color(row, col + 3),
                ):
                    return (row, col), (row, col + 1), (row, col + 2), (row, col + 3)
                else:
                    pass

    # Check vertical win
    def vertical_win_check(self):
        for col in range(7):
            for row in range(3):
                if self.check_match4(
                    self.report_color(row, col),
                    self.report_color(row + 1, col),
                    self.report_color(row + 2, col),
                    self.report_color(row + 3, col),
                ):
                    return (row, col), (row + 1, col), (row + 2, col), (row + 3, col)
                else:
                    pass

    # Check diagonal win
    def diagonal_win_check(self):
        for row in range(3):
            for col in range(4):
                if self.check_match4(
                    self.report_color(row, col),
                    self.report_color(row + 1, col + 1),
                    self.report_color(row + 2, col + 2),
                    self.report_color(row + 3, col + 3),
                ):
                    return (
                        (row, col),
                        (row + 1, col + 1),
                        (row + 2, col + 2),
                        (row + 3, col + 3),
                    )
        for row in range(3, 6):
            for col in range(4):
                if self.check_match4(
                    self.report_color(row, col),
                    self.report_color(row - 1, col + 1),
                    self.report_color(row - 2, col + 2),
                    self.report_color(row - 3, col + 3),
                ):
                    return (
                        (row, col),
                        (row - 1, col + 1),
                        (row - 2, col + 2),
                        (row - 3, col + 3),
                    )
                else:
                    pass


if __name__ == "__main__":
    (
        p1,
        p2,
        board,
        robot,
        message,
        error,
        deactivate,
        restart,
        p1_col,
        p1_row,
        p2_col,
        p2_row,
        p1_move_msg,
        p2_move_msg,
    ) = set_game()

    board.show_grid()

    while True:
        print(f"{board.current_player.name} ({board.current_player.color})'s " f"turn.")
        # Initialize row and column choices to None
        row_choice, column_choice = None, None
        # Get column choice from player
        while column_choice is None:
            if board.current_player == p1:
                try:
                    column_choice = int(
                        input(
                            f"{board.current_player.color}, "
                            f"please select a column_choice: "
                        )
                    )
                    if 0 <= column_choice <= 6:
                        print(column_choice)
                        row_choice = board.check_bottom(column_choice)
                        print(row_choice)
                        if row_choice is None:
                            print(f"column_choice {column_choice} is full")
                            column_choice = None
                    else:
                        print(
                            "column_choice number must be an integer " "between 0 and 6"
                        )
                        column_choice = None
                except ValueError:
                    print("Must input integer for column_choice number")
            elif board.current_player == p2:
                column_choice = robot.decide_move()
                row_choice = board.check_bottom(column_choice)

        print()
        print(f"{board.current_player.color} played in column {column_choice}")
        board.change_color(row_choice, column_choice, board.current_player.color)
        winner = board.check_winner()
        board.show_grid()

        if winner:
            print(f"{board.current_player.color} got a {winner}.")
            break
        else:
            board.change_turn()
