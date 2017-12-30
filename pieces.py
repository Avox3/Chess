
import os

from PIL import ImageTk

BASE_DIR = os.path.dirname(__file__)


def get_icon_image(icon):
    """

    :param icon:
    :return:
    """

    icon_path = os.path.join(BASE_DIR, 'assets', icon) + '.png'
    if os.path.exists(icon_path):
        return ImageTk.PhotoImage(file=icon_path)

    raise Exception


def get_piece(row, col, pieces):
    for piece in pieces:
        if piece.get_point() == (row, col):
            return piece


def repeat_movement(piece, row_step, col_step, pieces):

    row, col = piece.get_point()
    movements = []
    for i in xrange(8):
        row += row_step
        col += col_step

        stranger_piece = get_piece(row, col, pieces)
        if stranger_piece:
            if piece.is_white != stranger_piece.is_white:
                movements.append((row, col))
            return movements

        movements.append((row, col))

    return movements


def clean_movements(curr_piece, movements, pieces):
    return [movement for movement in movements if 0 <= movement[0] <= 7 and 0 <= movement[1] <= 7 and
            movement not in [piece.get_point() for piece in pieces if piece.is_white == curr_piece.is_white]]


class ChessPiece(object):
    def __init__(self, row, col, icon_path):
        """
        Create piece.
        :param row: x coordinate on the board
        :param col: y coordinate on the board
        :param icon_path: piece's icon
        """

        self.row = row
        self.col = col

        self.is_white = 'white' in icon_path

        self.icon_path = icon_path
        self.icon = get_icon_image(icon_path)

    def set_point(self, row, col):
        self.row = row
        self.col = col

    def get_point(self):
        return self.row, self.col

    def get_movements(self, pieces):
        return []


class Pawn(ChessPiece):

    def get_movements(self, pieces):

        movements = [(self.row - 1, self.col)]
        if self.row == 6:  # initial location
            movements.append((self.row - 2, self.col))

        enemies = [get_piece(self.row - 1, self.col + 1, pieces), get_piece(self.row - 1, self.col - 1, pieces)]
        movements += [piece.get_point() for piece in enemies if piece]

        return clean_movements(self, movements, pieces)


class Bishop(ChessPiece):

    def get_movements(self, pieces):
        movements = repeat_movement(self, 1, 1, pieces) +\
                    repeat_movement(self, -1, -1, pieces) +\
                    repeat_movement(self, 1, -1, pieces) +\
                    repeat_movement(self, -1, 1, pieces)

        return clean_movements(self, movements, pieces)


class Knight(ChessPiece):

    def get_movements(self, pieces):

        movements = []
        steps = [-2, -1, 1, 2]

        for x_add in steps:
            for y_add in steps:
                curr_row = self.row + x_add
                curr_col = self.col + y_add
                if abs(y_add) != abs(x_add):
                    movements.append((curr_row, curr_col))

        return clean_movements(self, movements, pieces)


class Rook(ChessPiece):
    def __init__(self, row, col, icon_path):
        super(Rook, self).__init__(row, col, icon_path)
        self.moved = False

    def get_movements(self, pieces):
        movements = repeat_movement(self, 1, 0, pieces) +\
                    repeat_movement(self, -1, 0, pieces) +\
                    repeat_movement(self, 0, 1, pieces) +\
                    repeat_movement(self, 0, -1, pieces)

        return clean_movements(self, movements, pieces)


class Queen(ChessPiece):
    def get_movements(self, pieces):
        movements = repeat_movement(self, 1, 0, pieces) +\
                    repeat_movement(self, -1, 0, pieces) +\
                    repeat_movement(self, 0, 1, pieces) +\
                    repeat_movement(self, 0, -1, pieces) +\
                    repeat_movement(self, 1, 1, pieces) +\
                    repeat_movement(self, -1, -1, pieces) +\
                    repeat_movement(self, 1, -1, pieces) +\
                    repeat_movement(self, -1, 1, pieces)

        return clean_movements(self, movements, pieces)


class King(ChessPiece):

    def __init__(self, row, col, icon_path):
        super(King, self).__init__(row, col, icon_path)
        self.moved = False

    def get_threats(self):
        pass

    def get_movements(self, pieces):

        # TODO - add castling and clean threatened squares
        movements = []
        steps = [-1, 0, 1]
        for x_add in steps:
            for y_add in steps:
                curr_row = self.row + x_add
                curr_col = self.col + y_add
                movements.append((curr_row, curr_col))

        return clean_movements(self, movements, pieces)
