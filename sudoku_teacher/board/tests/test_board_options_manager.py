import pytest

from sudoku_teacher.board.board_options_manager import BoardOptionsManager, ALL_VALS


def test_default_values():
    bom = BoardOptionsManager()
    for i in range(9):
        for j in range(9):
            assert bom.board[i][j] == 0
            assert bom.options[i][j] == ALL_VALS


@pytest.mark.parametrize(
    "idx, naked_subset",
    [(0, {2, 3}), (1, {1, 2, 3}), (2, {3, 2, 5, 4}), (3, {1, 2, 3, 4, 5, 6})],
)
def test_naked_pair_from_row(idx, naked_subset):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        bom.options[idx][i] = naked_subset

    point_to_options = bom.create_points_from_row(idx)
    bom.handle_naked_subset(point_to_options)

    for i in range(len(naked_subset)):
        assert point_to_options[(idx, i)] == naked_subset
    for i in range(len(naked_subset), 9):
        assert point_to_options[(idx, i)] == ALL_VALS - naked_subset


@pytest.mark.parametrize(
    "idx, naked_subset",
    [(0, {2, 3}), (1, {1, 2, 3}), (2, {3, 2, 5, 4}), (3, {1, 2, 3, 4, 5, 6})],
)
def test_naked_pair_from_col(idx, naked_subset):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        bom.options[i][idx] = naked_subset

    point_to_options = bom.create_points_from_col(idx)
    bom.handle_naked_subset(point_to_options)

    for i in range(len(naked_subset)):
        assert point_to_options[(i, idx)] == naked_subset
    for i in range(len(naked_subset), 9):
        assert point_to_options[(i, idx)] == ALL_VALS - naked_subset


@pytest.mark.parametrize(
    "naked_subset, extra",
    [({2, 3}, 9), ({1, 2, 3}, 9), ({3, 2, 5, 4}, 9), ({1, 2, 3, 4, 5, 6}, 9)],
)
def test_naked_pair_fail_due_to_extra(naked_subset, extra):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        bom.options[0][i] = naked_subset
    bom.options[0][0] = naked_subset | {extra}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_naked_subset(point_to_options)

    assert point_to_options[(0, 0)] == naked_subset | {extra}
    for idx in range(1, len(naked_subset)):
        assert point_to_options[(0, idx)] == naked_subset
    for idx in range(len(naked_subset), 9):
        assert (
            point_to_options[(0, idx)] == ALL_VALS
        )  # naked pair was not substracted because naked pair does not exists


def test_naked_pair():
    bom = BoardOptionsManager()
    bom.options[0][0] = {}
    bom.options[0][1] = {}
    bom.options[0][2] = {2, 3, 4, 8}
    bom.options[0][3] = {}
    bom.options[0][4] = {}
    bom.options[0][5] = {3, 4, 8}
    bom.options[0][6] = {2, 3}
    bom.options[0][7] = {}
    bom.options[0][8] = {2, 3}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_naked_subset(point_to_options)
    assert bom.options[0][0] == {}
    assert bom.options[0][1] == {}
    assert bom.options[0][2] == {4, 8}
    assert bom.options[0][3] == {}
    assert bom.options[0][4] == {}
    assert bom.options[0][5] == {4, 8}
    assert bom.options[0][6] == {2, 3}
    assert bom.options[0][7] == {}
    assert bom.options[0][8] == {2, 3}


def test_naked_triple():
    bom = BoardOptionsManager()
    bom.options[0][0] = {7, 8, 9}
    bom.options[0][1] = {}
    bom.options[0][2] = {7, 8}
    bom.options[0][3] = {3, 5, 9}
    bom.options[0][4] = {}
    bom.options[0][5] = {5, 6, 8, 9}
    bom.options[0][6] = {7, 9}
    bom.options[0][7] = {}
    bom.options[0][8] = {3, 5, 6, 7, 8, 9}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_naked_subset(point_to_options)
    assert bom.options[0][0] == {7, 8, 9}
    assert bom.options[0][1] == {}
    assert bom.options[0][2] == {7, 8}
    assert bom.options[0][3] == {3, 5}
    assert bom.options[0][4] == {}
    assert bom.options[0][5] == {5, 6}
    assert bom.options[0][6] == {7, 9}
    assert bom.options[0][7] == {}
    assert bom.options[0][8] == {3, 5, 6}


def test_naked_quad():
    bom = BoardOptionsManager()
    bom.options[0][0] = {1}
    bom.options[0][1] = {4, 5, 6}
    bom.options[0][2] = {4, 9}
    bom.options[0][3] = {3, 5, 6}
    bom.options[0][4] = {3, 5, 6, 7}
    bom.options[0][5] = {3, 5, 7}
    bom.options[0][6] = {2, 4, 8, 9}
    bom.options[0][7] = {2, 4}
    bom.options[0][8] = {2, 8, 9}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_naked_subset(point_to_options)
    assert bom.options[0][0] == {1}
    assert bom.options[0][1] == {5, 6}
    assert bom.options[0][2] == {4, 9}
    assert bom.options[0][3] == {3, 5, 6}
    assert bom.options[0][4] == {3, 5, 6, 7}
    assert bom.options[0][5] == {3, 5, 7}
    assert bom.options[0][6] == {2, 4, 8, 9}
    assert bom.options[0][7] == {2, 4}
    assert bom.options[0][8] == {2, 8, 9}


def test_hidden_pair0():

    bom = BoardOptionsManager()
    bom.options[0][0] = {1, 3, 7, 8}
    bom.options[0][1] = {1, 3, 7, 8}
    bom.options[0][2] = {}
    bom.options[0][3] = {}
    bom.options[0][4] = {1, 3, 5, 9}
    bom.options[0][5] = {1, 3, 5, 8, 9}
    bom.options[0][6] = {}
    bom.options[0][7] = {1, 3}
    bom.options[0][8] = {1, 8}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_hidden_subset(point_to_options)
    assert bom.options[0][0] == {1, 3, 7, 8}
    assert bom.options[0][1] == {1, 3, 7, 8}
    assert bom.options[0][2] == {}
    assert bom.options[0][3] == {}
    assert bom.options[0][4] == {5, 9}
    assert bom.options[0][5] == {5, 9}
    assert bom.options[0][6] == {}
    assert bom.options[0][7] == {1, 3}
    assert bom.options[0][8] == {1, 8}


def test_hidden_pair1():

    bom = BoardOptionsManager()
    bom.options[0][0] = {}
    bom.options[0][1] = {}
    bom.options[0][2] = {1, 5, 6, 8}
    bom.options[0][3] = {1, 5, 6, 8}
    bom.options[0][4] = {1, 6, 8}
    bom.options[0][5] = {5, 6, 8}
    bom.options[0][6] = {}
    bom.options[0][7] = {2, 3, 5}
    bom.options[0][8] = {2, 3, 5}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_hidden_subset(point_to_options)
    assert bom.options[0][0] == {}
    assert bom.options[0][1] == {}
    assert bom.options[0][2] == {1, 5, 6, 8}
    assert bom.options[0][3] == {1, 5, 6, 8}
    assert bom.options[0][4] == {1, 6, 8}
    assert bom.options[0][5] == {5, 6, 8}
    assert bom.options[0][6] == {}
    assert bom.options[0][7] == {2, 3}
    assert bom.options[0][8] == {2, 3}


def test_hidden_triple0():

    bom = BoardOptionsManager()
    bom.options[0][0] = {}
    bom.options[0][1] = {}
    bom.options[0][2] = {1, 2, 4, 5}
    bom.options[0][3] = {7, 9}
    bom.options[0][4] = {4, 6, 7}
    bom.options[0][5] = {4, 6, 7, 9}
    bom.options[0][6] = {1, 2, 4, 5, 6, 7}
    bom.options[0][7] = {1, 2, 4, 6, 7, 9}
    bom.options[0][8] = {4, 7, 9}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_hidden_subset(point_to_options)
    assert bom.options[0][0] == {}
    assert bom.options[0][1] == {}
    assert bom.options[0][2] == {1, 2, 5}
    assert bom.options[0][3] == {7, 9}
    assert bom.options[0][4] == {4, 6, 7}
    assert bom.options[0][5] == {4, 6, 7, 9}
    assert bom.options[0][6] == {1, 2, 5}
    assert bom.options[0][7] == {1, 2}
    assert bom.options[0][8] == {4, 7, 9}


def test_hidden_triple1():
    bom = BoardOptionsManager()
    bom.options[0][0] = {1, 3, 7, 8}
    bom.options[0][1] = {}
    bom.options[0][2] = {1, 2, 6, 7, 8}
    bom.options[0][3] = {6, 7}
    bom.options[0][4] = {2, 6, 7}
    bom.options[0][5] = {2, 6}
    bom.options[0][6] = {1, 2, 3, 6, 7}
    bom.options[0][7] = {}
    bom.options[0][8] = {}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_hidden_subset(point_to_options)
    assert bom.options[0][0] == {1, 3, 8}
    assert bom.options[0][1] == {}
    assert bom.options[0][2] == {1, 8}
    assert bom.options[0][3] == {6, 7}
    assert bom.options[0][4] == {2, 6, 7}
    assert bom.options[0][5] == {2, 6}
    assert bom.options[0][6] == {1, 3}
    assert bom.options[0][7] == {}
    assert bom.options[0][8] == {}


def test_hidden_quad():
    bom = BoardOptionsManager()
    bom.options[0][0] = {1, 2, 5, 6, 7}
    bom.options[0][1] = {2, 4, 5, 6, 7}
    bom.options[0][2] = {1, 4, 5, 6, 7, 8}
    bom.options[0][3] = {5, 9}
    bom.options[0][4] = {2, 4}
    bom.options[0][5] = {7, 8}
    bom.options[0][6] = {3, 4, 9}
    bom.options[0][7] = {2, 4, 5}
    bom.options[0][8] = {2, 3, 4, 5, 9}

    point_to_options = bom.create_points_from_row(0)
    bom.handle_hidden_subset(point_to_options)
    assert bom.options[0][0] == {1, 6, 7}
    assert bom.options[0][1] == {6, 7}
    assert bom.options[0][2] == {1, 6, 7, 8}
    assert bom.options[0][3] == {5, 9}
    assert bom.options[0][4] == {2, 4}
    assert bom.options[0][5] == {7, 8}
    assert bom.options[0][6] == {3, 4, 9}
    assert bom.options[0][7] == {2, 4, 5}
    assert bom.options[0][8] == {2, 3, 4, 5, 9}
