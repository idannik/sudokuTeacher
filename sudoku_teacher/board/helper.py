from typing import List, Type, TypeVar

T = TypeVar("T", bound="SubsetSubsetTreeNode")


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


def update_naked(node: OptionsPointsTreeNode, point_to_options):
    if len(node.options) == len(node.points):
        for point, options in point_to_options.items():
            if point in node.points or not options:
                continue
            options.difference_update(node.options)
        return
    for child in node.children:
        update_naked(child, point_to_options)


class PointsOptionsTreeNode(SubsetSubsetTreeNode):
    def __init__(self, points, options):
        super().__init__(points, options)

    @property
    def points(self):
        return self.id_subset

    @property
    def options(self):
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


def get_square_idx(row, col):
    return row // 3 * 3 + col // 3
