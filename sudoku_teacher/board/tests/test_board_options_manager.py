import pytest

from sudoku_teacher.board.board_options_manager import BoardOptionsManager, ALL_VALS


def set_set_value(s, new_val):
    s.clear()
    if new_val:
        s.update(new_val)


def test_default_values():
    bom = BoardOptionsManager()
    for i in range(9):
        for j in range(9):
            assert bom.board[i][j] == 0
            assert bom.options[i][j] == ALL_VALS


def test_square1():
    bom = BoardOptionsManager()
    square = bom.squares[1]
    assert (0, 3) in square.point_to_options
    assert (0, 4) in square.point_to_options
    assert (0, 5) in square.point_to_options
    assert (1, 3) in square.point_to_options
    assert (1, 4) in square.point_to_options
    assert (1, 5) in square.point_to_options
    assert (2, 3) in square.point_to_options
    assert (2, 4) in square.point_to_options
    assert (2, 5) in square.point_to_options


@pytest.mark.parametrize(
    "idx, naked_subset",
    [(0, {2, 3}), (1, {1, 2, 3}), (2, {3, 2, 5, 4}), (3, {1, 2, 3, 4, 5, 6})],
)
def test_naked_pair_from_row(idx, naked_subset):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        set_set_value(bom.options[idx][i], naked_subset)

    bom.handle_naked_subset(idx, 0)

    for i in range(len(naked_subset)):
        assert bom.options[idx][i] == naked_subset
    for i in range(len(naked_subset), 9):
        assert bom.options[idx][i] == ALL_VALS - naked_subset


@pytest.mark.parametrize(
    "idx, naked_subset",
    [(0, {2, 3}), (1, {1, 2, 3}), (2, {3, 2, 5, 4}), (3, {1, 2, 3, 4, 5, 6})],
)
def test_naked_pair_from_col(idx, naked_subset):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        set_set_value(bom.options[i][idx], naked_subset)

    bom.handle_naked_subset(0, idx)

    for i in range(len(naked_subset)):
        assert bom.options[i][idx] == naked_subset
    for i in range(len(naked_subset), 9):
        assert bom.options[i][idx] == ALL_VALS - naked_subset


@pytest.mark.parametrize(
    "naked_subset, extra",
    [({2, 3}, 9), ({1, 2, 3}, 9), ({3, 2, 5, 4}, 9), ({1, 2, 3, 4, 5, 6}, 9)],
)
def test_naked_pair_fail_due_to_extra(naked_subset, extra):
    bom = BoardOptionsManager()
    for i in range(len(naked_subset)):
        set_set_value(bom.options[0][i], naked_subset)
    set_set_value(bom.options[0][0], naked_subset | {extra})

    bom.handle_naked_subset(0, 0)

    assert bom.options[0][0] == naked_subset | {extra}
    for idx in range(1, len(naked_subset)):
        assert bom.options[0][idx] == naked_subset
    for idx in range(len(naked_subset), 9):
        assert (
            bom.options[0][idx] == ALL_VALS
        )  # naked pair was not substracted because naked pair does not exists


def test_naked_pair():
    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], set())
    set_set_value(bom.options[0][1], set())
    set_set_value(bom.options[0][2], {2, 3, 4, 8})
    set_set_value(bom.options[0][3], set())
    set_set_value(bom.options[0][4], set())
    set_set_value(bom.options[0][5], {3, 4, 8})
    set_set_value(bom.options[0][6], {2, 3})
    set_set_value(bom.options[0][7], set())
    set_set_value(bom.options[0][8], {2, 3})

    bom.handle_naked_subset(0, 0)

    assert bom.options[0][0] == set()
    assert bom.options[0][1] == set()
    assert bom.options[0][2] == {4, 8}
    assert bom.options[0][3] == set()
    assert bom.options[0][4] == set()
    assert bom.options[0][5] == {4, 8}
    assert bom.options[0][6] == {2, 3}
    assert bom.options[0][7] == set()
    assert bom.options[0][8] == {2, 3}


def test_naked_triple():
    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], {7, 8, 9})
    set_set_value(bom.options[0][1], set())
    set_set_value(bom.options[0][2], {7, 8})
    set_set_value(bom.options[0][3], {3, 5, 9})
    set_set_value(bom.options[0][4], set())
    set_set_value(bom.options[0][5], {5, 6, 8, 9})
    set_set_value(bom.options[0][6], {7, 9})
    set_set_value(bom.options[0][7], set())
    set_set_value(bom.options[0][8], {3, 5, 6, 7, 8, 9})

    bom.handle_naked_subset(0, 0)
    assert bom.options[0][0] == {7, 8, 9}
    assert bom.options[0][1] == set()
    assert bom.options[0][2] == {7, 8}
    assert bom.options[0][3] == {3, 5}
    assert bom.options[0][4] == set()
    assert bom.options[0][5] == {5, 6}
    assert bom.options[0][6] == {7, 9}
    assert bom.options[0][7] == set()
    assert bom.options[0][8] == {3, 5, 6}


def test_naked_quad():
    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], {1})
    set_set_value(bom.options[0][1], {4, 5, 6})
    set_set_value(bom.options[0][2], {4, 9})
    set_set_value(bom.options[0][3], {3, 5, 6})
    set_set_value(bom.options[0][4], {3, 5, 6, 7})
    set_set_value(bom.options[0][5], {3, 5, 7})
    set_set_value(bom.options[0][6], {2, 4, 8, 9})
    set_set_value(bom.options[0][7], {2, 4})
    set_set_value(bom.options[0][8], {2, 8, 9})

    bom.handle_naked_subset(0, 0)

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
    set_set_value(bom.options[0][0], {1, 3, 7, 8})
    set_set_value(bom.options[0][1], {1, 3, 7, 8})
    set_set_value(bom.options[0][2], set())
    set_set_value(bom.options[0][3], set())
    set_set_value(bom.options[0][4], {1, 3, 5, 9})
    set_set_value(bom.options[0][5], {1, 3, 5, 8, 9})
    set_set_value(bom.options[0][6], set())
    set_set_value(bom.options[0][7], {1, 3})
    set_set_value(bom.options[0][8], {1, 8})

    bom.handle_hidden_subset(0, 0)

    assert bom.options[0][0] == {1, 3, 7, 8}
    assert bom.options[0][1] == {1, 3, 7, 8}
    assert bom.options[0][2] == set()
    assert bom.options[0][3] == set()
    assert bom.options[0][4] == {5, 9}
    assert bom.options[0][5] == {5, 9}
    assert bom.options[0][6] == set()
    assert bom.options[0][7] == {1, 3}
    assert bom.options[0][8] == {1, 8}


def test_hidden_pair1():

    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], set())
    set_set_value(bom.options[0][1], set())
    set_set_value(bom.options[0][2], {1, 5, 6, 8})
    set_set_value(bom.options[0][3], {1, 5, 6, 8})
    set_set_value(bom.options[0][4], {1, 6, 8})
    set_set_value(bom.options[0][5], {5, 6, 8})
    set_set_value(bom.options[0][6], set())
    set_set_value(bom.options[0][7], {2, 3, 5})
    set_set_value(bom.options[0][8], {2, 3, 5})

    bom.handle_hidden_subset(0, 0)

    assert bom.options[0][0] == set()
    assert bom.options[0][1] == set()
    assert bom.options[0][2] == {1, 5, 6, 8}
    assert bom.options[0][3] == {1, 5, 6, 8}
    assert bom.options[0][4] == {1, 6, 8}
    assert bom.options[0][5] == {5, 6, 8}
    assert bom.options[0][6] == set()
    assert bom.options[0][7] == {2, 3}
    assert bom.options[0][8] == {2, 3}


def test_hidden_triple0():

    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], set())
    set_set_value(bom.options[0][1], set())
    set_set_value(bom.options[0][2], {1, 2, 4, 5})
    set_set_value(bom.options[0][3], {7, 9})
    set_set_value(bom.options[0][4], {4, 6, 7})
    set_set_value(bom.options[0][5], {4, 6, 7, 9})
    set_set_value(bom.options[0][6], {1, 2, 4, 5, 6, 7})
    set_set_value(bom.options[0][7], {1, 2, 4, 6, 7, 9})
    set_set_value(bom.options[0][8], {4, 7, 9})

    bom.handle_hidden_subset(0, 0)

    assert bom.options[0][0] == set()
    assert bom.options[0][1] == set()
    assert bom.options[0][2] == {1, 2, 5}
    assert bom.options[0][3] == {7, 9}
    assert bom.options[0][4] == {4, 6, 7}
    assert bom.options[0][5] == {4, 6, 7, 9}
    assert bom.options[0][6] == {1, 2, 5}
    assert bom.options[0][7] == {1, 2}
    assert bom.options[0][8] == {4, 7, 9}


def test_hidden_triple1():
    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], {1, 3, 7, 8})
    set_set_value(bom.options[0][1], set())
    set_set_value(bom.options[0][2], {1, 2, 6, 7, 8})
    set_set_value(bom.options[0][3], {6, 7})
    set_set_value(bom.options[0][4], {2, 6, 7})
    set_set_value(bom.options[0][5], {2, 6})
    set_set_value(bom.options[0][6], {1, 2, 3, 6, 7})
    set_set_value(bom.options[0][7], set())
    set_set_value(bom.options[0][8], set())

    bom.handle_hidden_subset(0, 0)

    assert bom.options[0][0] == {1, 3, 8}
    assert bom.options[0][1] == set()
    assert bom.options[0][2] == {1, 8}
    assert bom.options[0][3] == {6, 7}
    assert bom.options[0][4] == {2, 6, 7}
    assert bom.options[0][5] == {2, 6}
    assert bom.options[0][6] == {1, 3}
    assert bom.options[0][7] == set()
    assert bom.options[0][8] == set()


def test_hidden_quad():
    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], {1, 2, 5, 6, 7})
    set_set_value(bom.options[0][1], {2, 4, 5, 6, 7})
    set_set_value(bom.options[0][2], {1, 4, 5, 6, 7, 8})
    set_set_value(bom.options[0][3], {5, 9})
    set_set_value(bom.options[0][4], {2, 4})
    set_set_value(bom.options[0][5], {7, 8})
    set_set_value(bom.options[0][6], {3, 4, 9})
    set_set_value(bom.options[0][7], {2, 4, 5})
    set_set_value(bom.options[0][8], {2, 3, 4, 5, 9})

    bom.handle_hidden_subset(0, 0)

    assert bom.options[0][0] == {1, 6, 7}
    assert bom.options[0][1] == {6, 7}
    assert bom.options[0][2] == {1, 6, 7, 8}
    assert bom.options[0][3] == {5, 9}
    assert bom.options[0][4] == {2, 4}
    assert bom.options[0][5] == {7, 8}
    assert bom.options[0][6] == {3, 4, 9}
    assert bom.options[0][7] == {2, 4, 5}
    assert bom.options[0][8] == {2, 3, 4, 5, 9}


def test_pointing_subset():
    bom = BoardOptionsManager()
    set_set_value(bom.options[0][0], {2, 3, 5})
    set_set_value(bom.options[0][1], {2, 3, 5})
    set_set_value(bom.options[0][2], {2, 3, 5})
    set_set_value(bom.options[0][3], {})
    set_set_value(bom.options[0][4], {})
    set_set_value(bom.options[0][5], {})
    set_set_value(bom.options[0][6], {})
    set_set_value(bom.options[0][7], {})
    set_set_value(bom.options[0][8], {})

    bom.handle_pointing_subset(0, 0)

    # col
    assert bom.options[0][0] == {2, 3, 5}
    assert bom.options[0][1] == {2, 3, 5}
    assert bom.options[0][2] == {2, 3, 5}
    assert bom.options[0][3] == set()
    assert bom.options[0][4] == set()
    assert bom.options[0][5] == set()
    assert bom.options[0][6] == set()
    assert bom.options[0][7] == set()
    assert bom.options[0][8] == set()

    # square
    assert bom.options[0][0] == {2, 3, 5}
    assert bom.options[0][1] == {2, 3, 5}
    assert bom.options[0][2] == {2, 3, 5}
    assert bom.options[1][0] == ALL_VALS - {2, 3, 5}
    assert bom.options[1][1] == ALL_VALS - {2, 3, 5}
    assert bom.options[1][2] == ALL_VALS - {2, 3, 5}
    assert bom.options[2][0] == ALL_VALS - {2, 3, 5}
    assert bom.options[2][1] == ALL_VALS - {2, 3, 5}
    assert bom.options[2][2] == ALL_VALS - {2, 3, 5}
