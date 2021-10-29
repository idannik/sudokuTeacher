from copy import deepcopy

from .board_options_manager import BoardOptionsManager


class SudokuSuggester:
    def __init__(self, board, board_options_handler=None):
        self.board = board
        self.solved = False
        self.options_handler = board_options_handler or BoardOptionsManager(self.board)
        self.options_handler.init_board_options(self.board)
        self.options_handler.update_board_options(self.board)

    def stringify(self):
        return "".join(
            [str(self.board[i][j]) for i in range(9) for j in range(9)]
        ).replace("0", ".")

    @property
    def options(self):
        return self.options_handler.options

    def solve(self):
        while True:
            next_steps = self.options_handler.next_step()
            if not next_steps:
                return
            for (i, j), val in next_steps:
                self.options_handler.options[i][j] = set()
                self.board[i][j] = val
                yield self
                self.update_board_options_according_to_cell(i, j)

    def update_board_options_according_to_cell(self, row, col):
        val = self.board[row][col]
        return self.options_handler.update_board_options_according_to_cell(
            row, col, val
        )

    def print_options(self):
        self.options_handler.print_options()

    def get_options_list(self):
        options = deepcopy(self.options)
        for i in range(9):
            for j in range(9):
                options[i][j] = list(options[i][j])
        return options
