
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


class ChessPiece(object):
    def __init__(self, x, y, icon):
        self.x = x
        self.y = y

        self.icon = get_icon_image(icon)


class Pawn(ChessPiece):

    def __init__(self, x, y, icon, side):
        super(Pawn, self).__init__(x, y, icon)

        self.side = side

        # self.icon = ImageTk.PhotoImage(file=os.path.join(BASE_DIR, ''))

    def get_movements(self):
        movements = []

        if self.side == WHITE:
            if


class Bishop(ChessPiece):

    def __init__(self, x, y, icon):
        super(Bishop, self).__init__(x, y, icon)


class Knight(ChessPiece):

    def __init__(self, x, y, icon):
        super(Knight, self).__init__(x, y, icon)


class Rook(ChessPiece):
    def __init__(self, x, y, icon):
        super(Rook, self).__init__(x, y, icon)


class Queen(ChessPiece):
    def __init__(self, x, y, icon):
        super(Queen, self).__init__(x, y, icon)


class King(ChessPiece):
    def __init__(self, x, y, icon):
        super(King, self).__init__(x, y, icon)
