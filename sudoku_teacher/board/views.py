import json
from django.http import JsonResponse

# Create your views here.
from sudoku_teacher.board.sudoku_loader import Sudoku
from sudoku_teacher.board.sudoku_solver import SudokuSuggester


def get_board(request):
    b = Sudoku().board
    result = {"board": b, "pencil_marks": [[] * 9 for _ in range(9)]}
    return JsonResponse(result)


def fill_pencil_marks(request):
    data = json.loads(request.body)
    board = data["board"]
    data["pencil_marks"] = SudokuSuggester(board).get_options_list()
    return JsonResponse(data)
