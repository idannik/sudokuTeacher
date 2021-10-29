from django.urls import path

from sudoku_teacher.board.views import get_board, fill_pencil_marks

app_name = "board"

urlpatterns = [
    path("get_board/", view=get_board, name="get_board"),
    path("fill_pencil_marks/", view=fill_pencil_marks, name="fill_pencil_marks"),
]
