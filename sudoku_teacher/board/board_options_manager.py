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
            update_naked(root, point_to_options)

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
            update_hidden(root, point_to_options)

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


class SubsetSubsetTreeNode:
    def __init__(self, id_subset, data_subset):
        self.id_subset = id_subset
        self.data_subset = data_subset
        self.children: List["SubsetSubsetTreeNode"] = []

    def add_child(self, node: "SubsetSubsetTreeNode"):
        if not self.id_subset.issubset(node.id_subset):
            return False
        found_child = any([child.add_child(node) for child in self.children])
        if not found_child:
            node.data_subset.update(self.data_subset)
            self.children.append(node)
        return True

    def __str__(self):
        return f"SubsetSubsetTreeNode(id = {self.id_subset}, data = {self.data_subset})"

    def __repr__(self):
        return str(self)


class PointsOptionsTreeNode(SubsetSubsetTreeNode):
    def __init__(self, points, options):
        super().__init__(points, options)

    @property
    def points(self):
        return self.id_subset

    @property
    def options(self):
        return self.data_subset


class OptionsPointsTreeNode(SubsetSubsetTreeNode):
    def __init__(self, options, points):
        super().__init__(options, points)

    @property
    def options(self):
        return self.id_subset

    @property
    def points(self):
        return self.data_subset


def update_hidden(node: PointsOptionsTreeNode, point_to_options):
    if len(node.points) == len(node.options):
        for point in node.id_subset:
            old_val = point_to_options[point]
            new_val = old_val.intersection(node.options)
            point_to_options[point].clear()
            point_to_options[point].update(new_val)
        return
    for child in node.children:
        update_hidden(child, point_to_options)


def update_naked(node: OptionsPointsTreeNode, point_to_options):
    if len(node.options) == len(node.points):
        for point, options in point_to_options.items():
            if point in node.points or not options:
                continue
            options.difference_update(node.options)
        return
    for child in node.children:
        update_naked(child, point_to_options)
