from collections import defaultdict
from copy import deepcopy
from typing import List

from prettytable import PrettyTable

from sudoku_teacher.board.board_group import BoardGroup
from sudoku_teacher.board.helper import (
    update_naked,
    update_hidden,
    OptionsPointsTreeNode,
    PointsOptionsTreeNode,
    get_square_idx,
)

ALL_VALS = frozenset(range(1, 10))


class BoardOptionsManager:
    def __init__(self, board=None, board_options=None):
        if board is None:
            board = []
            for i in range(9):
                board.append([0 for _ in range(9)])
        self.board = board
        self.options = board_options
        if self.options is None:
            self.init_board_options()
        self.rows: List[BoardGroup] = [
            self.create_board_group_from_row(row) for row in range(9)
        ]
        self.cols: List[BoardGroup] = [
            self.create_board_group_from_col(col) for col in range(9)
        ]
        self.squares: List[BoardGroup] = [
            self.create_board_group_from_square_by_idx(idx) for idx in range(9)
        ]

    def init_board_options(self):
        self.options = []
        for i in range(9):
            row = []
            for j in range(9):
                val = set()
                if self.board[i][j] == 0:
                    val = set(ALL_VALS)
                row.append(val)
            self.options.append(row)

    def handle_hidden_subset(self, row, col):
        self.rows[row].handle_hidden_subset()
        self.cols[col].handle_hidden_subset()
        square_idx = get_square_idx(row, col)
        self.squares[square_idx].handle_hidden_subset()

    def handle_naked_subset(self, row, col):
        self.rows[row].handle_naked_subset()
        self.cols[col].handle_naked_subset()
        square_idx = get_square_idx(row, col)
        self.squares[square_idx].handle_naked_subset()

    def update_board_options(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] > 0:
                    options = deepcopy(self.options)
                    self.update_board_options_according_to_value(i, j, val=board[i][j])
                    self.assert_rules()
        for i in range(9):
            self.update_board_options_according_to_row_group(i)
            self.update_board_options_according_to_col_group(i)

    def update_board_options_according_to_cell(self, row, col, val=0):
        options = deepcopy(self.options)
        self.assert_rules()

        self.update_board_options_according_to_value(row, col, val)
        options1 = deepcopy(self.options[row][col])
        self.assert_rules()
        self.update_board_options_according_to_row_group(row)
        options2 = deepcopy(self.options[row][col])
        self.assert_rules()
        options = deepcopy(self.options)

        self.update_board_options_according_to_col_group(col)
        self.assert_rules()

        self.update_board_options_according_to_square_group(row, col)
        self.assert_rules()

    def assert_rules(self):
        for i in range(9):
            for j in range(9):
                options = self.options[i][j]
                value = self.board[i][j]
                assert options or value > 0
                if len(self.options[i][j]) == 1:
                    assert self.board[i][j] == 0

    def create_board_group_from_row(self, row):
        points_to_options = {(row, col): self.options[row][col] for col in range(9)}
        return BoardGroup(points_to_options)

    def create_board_group_from_col(self, col):
        points_to_options = {(row, col): self.options[row][col] for row in range(9)}
        return BoardGroup(points_to_options)

    def create_board_group_from_square_by_idx(self, idx):
        row = (idx // 3) * 3
        col = (idx % 3) * 3
        return self.create_board_group_from_square_by_pos(row, col)

    def create_board_group_from_square_by_pos(self, row, col):
        points_to_options = {}
        square_start_row = row - (row % 3)
        square_start_col = col - (col % 3)
        for i in range(3):
            row = square_start_row + i
            for j in range(3):
                col = square_start_col + j
                points_to_options[(row, col)] = self.options[row][col]
        return BoardGroup(points_to_options)

    def update_board_options_according_to_value(self, row, col, val):
        if val == 0:
            return
        for i in range(9):
            self.options[i][col].discard(val)
            self.options[row][i].discard(val)
        square_start_row = row - (row % 3)
        square_start_col = col - (col % 3)
        for i in range(3):
            for j in range(3):
                self.options[square_start_row + i][square_start_col + j].discard(val)

    def next_step(self):
        res = set()
        for i in range(9):
            for j in range(9):
                if len(self.options[i][j]) == 1:
                    value = next(iter(self.options[i][j]))
                    res.add(((i, j), value))
                for value in self.options[i][j]:
                    if self.only_value(i, j, value):
                        res.add(((i, j), value))
        return res

    def only_value_in_row(self, row, value):
        return len([k for k in range(9) if value in self.options[row][k]]) == 1

    def only_value_in_col(self, col, value):
        return len([k for k in range(9) if value in self.options[k][col]]) == 1

    def only_value_in_square(self, row, col, value):
        square_start_row = row - (row % 3)
        square_start_col = col - (col % 3)
        return (
            len(
                [
                    (k, p)
                    for p in range(3)
                    for k in range(3)
                    if value in self.options[square_start_row + p][square_start_col + k]
                ]
            )
            == 1
        )

    def only_value(self, row, col, value):
        return (
            self.only_value_in_row(row, value)
            or self.only_value_in_col(col, value)
            or self.only_value_in_square(row, col, value)
        )

    def update_board_options_according_to_row_group(self, row):
        point_to_options = self.create_points_from_row(row)
        old_point_to_options = deepcopy(point_to_options)

        self.handle_naked_subset(point_to_options)
        self.assert_rules()

        self.handle_hidden_subset(point_to_options)
        self.assert_rules()

    def update_board_options_according_to_col_group(self, col):
        point_to_options = self.create_points_from_col(col)
        old_point_to_options = deepcopy(point_to_options)
        self.handle_naked_subset(point_to_options)
        old_point_to_options2 = deepcopy(point_to_options)

        self.assert_rules()

        self.handle_hidden_subset(point_to_options)
        self.assert_rules()

    def update_board_options_according_to_square_group(self, row, col):
        point_to_options = self.create_points_from_square(row, col)
        old_point_to_options = deepcopy(point_to_options)
        self.handle_naked_subset(point_to_options)
        old_point_to_options2 = deepcopy(point_to_options)

        self.assert_rules()

        self.handle_hidden_subset(point_to_options)
        self.assert_rules()

    def print_options(self):
        x = PrettyTable
        x.field_names = ["", 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i, row in enumerate(self.options):
            x.add_row(
                [
                    str(i + 1),
                    *[",".join([str(option) for option in options]) for options in row],
                ]
            )
        print(x)
