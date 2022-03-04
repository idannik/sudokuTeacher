from collections import defaultdict, Set
from copy import deepcopy
from typing import FrozenSet, List, Optional, MutableSet

from prettytable import PrettyTable

ALL_VALS = frozenset(range(1, 10))


def sort_items_according_to_key_lengh(key):
    length = len(key[0])
    return length, key


class BoardOptionsManager:
    def __init__(self, board=None, board_options=None):
        if board is None:
            board = []
            for i in range(9):
                board.append([0 for _ in range(9)])
        if board_options is None:
            board_options = []
            for i in range(9):
                board_options.append([set(ALL_VALS) for _ in range(9)])
        self.board = board
        self.options = board_options

    def init_board_options(self, board):
        for i in range(9):
            row = []
            for j in range(9):
                val = set()
                if board[i][j] == 0:
                    val = {1, 2, 3, 4, 5, 6, 7, 8, 9}
                row.append(val)
            self.options.append(row)

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

    def create_points_from_row(self, row):
        return {(row, col): self.options[row][col] for col in range(9)}

    def create_points_from_col(self, col):
        return {(row, col): self.options[row][col] for row in range(9)}

    def create_points_from_square(self, row, col):
        res = {}
        square_start_row = row - (row % 3)
        square_start_col = col - (col % 3)
        for i in range(3):
            row = square_start_row + i
            for j in range(3):
                col = square_start_col + j
                res[(row, col)] = self.options[row][col]
        return res

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

    def handle_naked_subset(self, point_to_options):
        options_to_points = defaultdict(set)
        for point, options in point_to_options.items():
            if len(options) <= 1:
                continue
            sorted_options = frozenset(options)
            options_to_points[sorted_options].add(point)
        roots = []
        for option_subset in sorted(options_to_points, key=lambda x: (len(x), x)):
            points_subset = options_to_points[option_subset]
            node = OptionsPointsTreeNode(option_subset, points_subset)
            found_root = any([root.add_child(node) for root in roots])
            if not found_root:
                roots.append(node)
        for root in roots:
            root.update_naked(point_to_options)

    def handle_hidden_subset(self, point_to_options):
        options_to_points = defaultdict(set)
        for point, options in point_to_options.items():
            for option in options:
                options_to_points[option].add(point)
        points_subset_to_option_subset = defaultdict(set)

        for val, points in options_to_points.items():
            key = frozenset(points)
            points_subset_to_option_subset[key].add(val)

        roots = []
        for point_subset in sorted(
            points_subset_to_option_subset, key=lambda x: (len(x), x)
        ):
            options_subset = points_subset_to_option_subset[point_subset]
            node = PointsOptionsTreeNode(point_subset, options_subset)
            found_root = any([root.add_child(node) for root in roots])
            if not found_root:
                roots.append(node)
        for root in roots:
            root.update_hidden(point_to_options)

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


class PointsOptionsTreeNode:
    def __init__(self, points: FrozenSet[int], options: MutableSet[int]):
        self.points: FrozenSet[int] = points
        self.options: MutableSet[int] = options
        self.children: List["PointsOptionsTreeNode"] = []
        self.parent: Optional["PointsOptionsTreeNode"] = None

    def add_child(self, node: "PointsOptionsTreeNode"):
        if not self.points.issubset(node.points):
            return False
        found_child = any([child.add_child(node) for child in self.children])
        if not found_child:
            node.options.update(self.options)
            self.children.append(node)
            node.parent = self
        return True

    def update_hidden(self, point_to_options):
        if len(self.options) == len(self.points):
            for point in self.points:
                old_val = point_to_options[point]
                new_val = old_val.intersection(self.options)
                point_to_options[point].clear()
                point_to_options[point].update(new_val)
            return
        for child in self.children:
            child.update_hidden(point_to_options)

    def __str__(self):
        return f"SubsetTreeNode(points = {self.points}, options = {self.options})"

    def __repr__(self):
        return str(self)


class OptionsPointsTreeNode:
    def __init__(self, options: FrozenSet[int], points: MutableSet[int]):
        self.options: FrozenSet[int] = options
        self.points: MutableSet[int] = points
        self.children: List["OptionsPointsTreeNode"] = []
        self.parent: Optional["OptionsPointsTreeNode"] = None

    def add_child(self, node: "OptionsPointsTreeNode"):
        if not self.options.issubset(node.options):
            return False
        found_child = any([child.add_child(node) for child in self.children])
        if not found_child:
            node.points.update(self.points)
            self.children.append(node)
            node.parent = self
        return True

    def update_naked(self, point_to_options):
        if len(self.options) == len(self.points):
            for point, options in point_to_options.items():
                if point in self.points or not options:
                    continue
                options.difference_update(self.options)
            return
        for child in self.children:
            child.update_naked(point_to_options)

    def __str__(self):
        return f"SubsetTreeNode(points = {self.points}, options = {self.options})"

    def __repr__(self):
        return str(self)
