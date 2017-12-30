
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

    def get_movements(self, all_squares):
        return []


class Pawn(ChessPiece):

    def get_movements(self, all_squares):

        movements = [(self.row - 1, self.col)]
        if self.row == 6:  # initial location
            movements.append((self.row - 2, self.col))

        return movements


class Bishop(ChessPiece):

    def get_movements(self, all_squares):
        return []


class Knight(ChessPiece):

    def get_movements(self, all_squares):
        return []


class Rook(ChessPiece):

    def get_movements(self, all_squares):
        return []


class Queen(ChessPiece):

    def get_movements(self, all_squares):
        return []


class King(ChessPiece):

    def __init__(self, row, col, icon_path):
        super(King, self).__init__(row, col, icon_path)
        self.moved = False

    def get_movements(self, all_squares):
        return []
