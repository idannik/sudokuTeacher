import itertools
from collections import defaultdict

from sudoku_teacher.board.helper import (
    PointsOptionsTreeNode,
    update_hidden,
    OptionsPointsTreeNode,
    update_naked,
)


class BoardGroup:
    def __init__(self, points_to_options):
        self.point_to_options = points_to_options
        self.neighbors = {}

    def add_neighbor(self, points, neighbor: "BoardGroup"):
        if not points.subset(self.point_to_options.keys()):
            return
        self.neighbors[points] = neighbor

    def handle_naked_subset(self):
        options_to_points = defaultdict(set)
        for point, options in self.point_to_options.items():
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
            update_naked(root, self.point_to_options)

    def handle_hidden_subset(self):
        options_to_points = defaultdict(set)
        for point, options in self.point_to_options.items():
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
            update_hidden(root, self.point_to_options)

    def handle_pointing_subset(self):

        for neighbor, group in self.neighbors.items():
            values = set(
                itertools.chain.from_iterable(
                    [self.point_to_options[(i, j)] for i, j in neighbor]
                )
            )
            other_neighbors = {n for n in self.neighbors if n != neighbor}
            for other in other_neighbors:
                other_values = set(
                    itertools.chain.from_iterable(
                        [self.point_to_options[(i, j)] for i, j in other]
                    )
                )
                values.difference_update(other_values)
            if values:
                group.remove_except(values, neighbor)

    def remove_except(self, values, neighbor):
        for point, value in self.point_to_options.items():
            if point in neighbor:
                continue
            self.point_to_options[point].difference_update(values)
