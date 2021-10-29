import os


from config.settings.base import STATICFILES_DIRS

LEVEL = "medium"
LEVEL_PATH = os.path.join(STATICFILES_DIRS[0], "sudoku", "{level}")
SUDOKU_ID = 0


class Sudoku:
    def __init__(self):
        self.board = []
        dir_path = LEVEL_PATH.format(level=LEVEL)
        with open(os.path.join(dir_path, f"{SUDOKU_ID}.txt")) as f:
            lines = f.read().splitlines()
            for i in range(9):
                self.board.append([])
                for j in range(9):
                    self.board[-1].append(int(lines[i][j]))
