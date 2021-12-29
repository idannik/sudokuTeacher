import pytest

from sudoku_teacher.board.board_options_manager import BoardOptionsManager

ALL_VALS = {1, 2, 3, 4, 5, 6, 7, 8, 9}


def test_default_values():
    bom = BoardOptionsManager()
    for i in range(9):
        for j in range(9):
            assert bom.board[i][j] == 0
            assert bom.options[i][j] == ALL_VALS


@pytest.mark.parametrize("naked_subset", [{2, 3}, {1, 2, 3}, {3, 2, 5, 4}, {1, 2, 3, 4, 5, 6}])
def test_naked_pair(naked_subset):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        bom.options[0][i] = naked_subset
        bom.options[0][i] = naked_subset
    point_to_options = bom.create_points_from_row(0)
    bom.handle_naked_subset(point_to_options)
    for i in range(len(naked_subset)):
        assert point_to_options[(0, i)] == naked_subset
    for i in range(len(naked_subset), 9):
        assert point_to_options[(0, i)] == ALL_VALS - naked_subset

@pytest.mark.parametrize("naked_subset, extra", [({2, 3}, 9), ({1, 2, 3}, 9), ({3, 2, 5, 4}, 9), ({1, 2, 3, 4, 5, 6}, 9)])
def test_naked_pair_with_extra(naked_subset, extra):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        bom.options[0][i] = naked_subset | {extra}
        bom.options[0][i] = naked_subset
    point_to_options = bom.create_points_from_row(0)
    bom.handle_naked_subset(point_to_options)
    for i in range(len(naked_subset)):
        assert point_to_options[(0, i)] == naked_subset
    for i in range(len(naked_subset), 9):
        assert point_to_options[(0, i)] == ALL_VALS - naked_subset
