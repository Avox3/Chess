
import os

from PIL import ImageTk

BASE_DIR = os.path.dirname(__file__)

WHITE = 0
BLACK = 1


def get_icon_image(icon):
    """

    :param icon:
    :return:
    """

    icon_path = os.path.join(BASE_DIR, 'assets', icon) + '.png'
    if os.path.exists(icon_path):
        return ImageTk.PhotoImage(file=icon_path)

    raise Exception


def reverse_board(squares):
    squares = squares[::-1]


class ChessPiece(object):
    def __init__(self, icon_path):
        """

        :param icon:
        :param is_white:
        :return:
        """

        self.is_white = 'white' in icon_path
        self.icon_path = icon_path
        self.icon = get_icon_image(icon_path)
        self.row = -1
        self.col = -1

    def get_movements(self, square, all_squares):
        self.row, self.col = square
        return [(5, 5)]


class Pawn(ChessPiece):

    def get_movements(self, square, all_squares):
        super(Pawn, self).get_movements(square, all_squares)

        movements = [(square[0] - 1, square[1])]
        if square[0] == 6:  # initial location
            movements.append((square[0] - 2, square[1]))

        return movements


class Bishop(ChessPiece):

    def get_movements(self, square, all_squares):
        return []


class Knight(ChessPiece):

    def get_movements(self, square, all_squares):
        return []


class Rook(ChessPiece):

    def get_movements(self, square, all_squares):
        return []


class Queen(ChessPiece):

    def get_movements(self, square, all_squares):
        return []


class King(ChessPiece):

    def __init__(self, icon):
        super(King, self).__init__(icon)
        self.moved = False

    def get_movements(self, square, all_squares):
        return []
