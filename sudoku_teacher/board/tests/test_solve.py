import pytest

from sudoku_teacher.board.board_options_manager import BoardOptionsManager, ALL_VALS
from sudoku_teacher.board.helper import session_update_list
from sudoku_teacher.board.sudoku_loader import Sudoku


@pytest.mark.parametrize(
    "row, col, value",
    [(5, 6, 7), (3, 0, 3), (2, 7, 8), (1, 1, 9), (8, 5, 9)],
)
def test_eliminate_options_according_to_board(row, col, value):
    session_update_list.clear()
    board = []
    for i in range(9):
        board.append([0 for _ in range(9)])
    board[row][col] = value
    bom = BoardOptionsManager(board)
    bom.eliminate_options_according_to_board()

    new_options = ALL_VALS - {value}
    for i in range(9):
        if i != col:
            assert bom.options[row][i] == new_options

        if i != row:
            assert bom.options[i][col] == new_options

    for point, values in bom.get_square_points_to_options(row, col).items():
        if point != (row, col):
            assert bom.options[point[0]][point[1]] == new_options
    assert session_update_list
    for reason in session_update_list:
        assert reason["point"] != (row, col)


def test_solve0():
    session_update_list.clear()
    board = Sudoku().board
    bom = BoardOptionsManager(board)
    bom.solve_board()
    a=2
