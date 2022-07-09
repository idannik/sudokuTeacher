import json
from django.http import JsonResponse

# Create your views here.
from sudoku_teacher.board.helper import SESSION_KEY
from sudoku_teacher.board.sudoku_loader import Sudoku
from sudoku_teacher.board.board_solver import BoardSolver
from sudoku_teacher.board.helper import session


def get_board(request):
    b = Sudoku().board
    bs = BoardSolver(b)
    bs.solve_board()
    session_update_list = session.setdefault(SESSION_KEY, list())
    result = {"board": b, "solve_list": session_update_list}
    return JsonResponse(result)



