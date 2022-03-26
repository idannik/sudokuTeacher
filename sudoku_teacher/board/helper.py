from copy import deepcopy
from typing import List, Type, TypeVar

from django.contrib.sessions.backends.db import SessionStore

T = TypeVar("T", bound="SubsetSubsetTreeNode")

session = SessionStore()


class SubsetSubsetTreeNode:
    def __init__(self, id_subset, data_subset):
        self.id_subset = id_subset
        self.data_subset = data_subset
        self.children: List[Type[T]] = []

    def add_child(self, node: Type[T]):
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


class OptionsPointsTreeNode(SubsetSubsetTreeNode):
    def __init__(self, options, points):
        super().__init__(options, points)

    @property
    def options(self):
        return self.id_subset

    @property
    def points(self):
        return self.data_subset


def update_naked(node: OptionsPointsTreeNode, point_to_options, name: str):
    if len(node.options) == len(node.points):
        for point, options in point_to_options.items():
            if point in node.points or not options:
                continue
            orig_options = deepcopy(options)
            options.difference_update(node.options)
            if options != orig_options:
                update_move(point, node, options, orig_options, name, "naked")

        return
    for child in node.children:
        update_naked(child, point_to_options, name)


def update_move(point, node, new_options, orig_options, name, reason, neighbor=""):
    if new_options == orig_options:
        return
    session.setdefault("updates", list()).append(
        {
            "point": point,
            "orig_options": sorted(orig_options),
            "new_options": sorted(new_options),
            "reason": reason,
            "reason_points": sorted(node.points) if node else [],
            "reason_options": sorted(node.options) if node else [],
            "rule_loc": name,
            "neighbor": neighbor,
        }
    )


class PointsOptionsTreeNode(SubsetSubsetTreeNode):
    def __init__(self, points, options):
        super().__init__(points, options)

    @property
    def points(self):
        return self.id_subset

    @property
    def options(self):
        return self.data_subset


def update_hidden(node: PointsOptionsTreeNode, point_to_options, name):
    if len(node.points) == len(node.options):
        for point in node.id_subset:
            orig_options = deepcopy(point_to_options[point])
            new_options = orig_options.intersection(node.options)
            point_to_options[point].clear()
            point_to_options[point].update(new_options)
            update_move(point, node, new_options, orig_options, name, "hidden")

        return
    for child in node.children:
        update_hidden(child, point_to_options, name)


def get_square_idx(row, col):
    return row // 3 * 3 + col // 3


def get_row_col_from_square_id(idx):
    row = (idx // 3) * 3
    col = (idx % 3) * 3
    return col, row
