

from Tkinter import Tk, Grid, Entry, Button, END

from pieces import Pawn, Bishop, Knight, Rook, Queen, King, BLACK, WHITE


class ChessBoard:

    @staticmethod
    def get_pieces():

        starting_pieces = []

        for col in xrange(8):
            starting_pieces.append(Pawn(1, col, 'pawn_black', WHITE))
            starting_pieces.append(Pawn(6, col, 'pawn_white', BLACK))

        # first_row = [Rook, Knight, Bishop, King, Queen]
        # first_row += first_row[:3]
        #
        # for col in xrange(len(first_row)):
        #     starting_pieces.append(first_row[col](col, 0, 'rook_black'))
        #     starting_pieces.append(piece(row, 0, 'rook_black'))

        return starting_pieces

    @staticmethod
    def is_square_used(pieces, x, y):
        """

        :param pieces:
        :param x:
        :param y:
        :return:
        """
        for piece in pieces:
            if piece.x == x and piece.y == y:
                return piece
        return False

    def __init__(self):

        self.root = Tk()
        self.root.title('Chess2')

        square_style = {'borderwidth': 0, 'width': 5, 'height': 2}

        self.squares = self.get_pieces()

        # create responsive board as 8x8 grid
        for r in range(8):
            Grid.rowconfigure(self.root, r, weight=1)

            for c in range(8):
                Grid.columnconfigure(self.root, c, weight=1)

                square_color = 'white' if ((9 * r + c) % 2 == 0) else 'grey'
                # command=lambda x=1: self.action(x)
                btn = Button(self.root, bg=square_color, **square_style)
                btn.grid(row=r, column=c, sticky='nsew')

                piece = self.is_square_used(self.squares, r, c)
                if piece:
                    btn.config(image=piece.icon)
                    btn.image = piece.icon

    def start(self):
        if self.root:
            self.root.mainloop()
