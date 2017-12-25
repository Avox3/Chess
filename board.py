

from Tkinter import Tk, Grid, Button

from pieces import Pawn, Bishop, Knight, Rook, Queen, King, BLACK, WHITE


class ChessBoard:

    def get_symmetric(self, point, piece, twice=False):
        """

        :param point:
        :param piece:
        :param twice:
        :return:
        """

        curr_pieces = {point: piece}

        if twice:
            curr_pieces[(point[0], 7-point[1])] = piece.__class__(piece.icon_path)

        if piece.is_white:
            icon = piece.icon_path.replace('white', 'black')
        else:
            icon = piece.icon_path.replace('black', 'white')

        for curr_point, curr_piece in curr_pieces.items():
            curr_pieces[(7-curr_point[0], curr_point[1])] = curr_piece.__class__(icon)

        self.pieces.update(curr_pieces)

    def set_starting_pieces(self):
        """

        :return:
        """

        # first row pieces
        self.get_symmetric((0, 0), Rook('rook_black'), twice=True)
        self.get_symmetric((0, 1), Knight('knight_black'), twice=True)
        self.get_symmetric((0, 2), Bishop('bishop_black'), twice=True)

        self.get_symmetric((0, 3), Queen('queen_black'))
        self.get_symmetric((0, 4), King('king_black'))

        # second row pieces - pawns
        for col in xrange(4):
            self.get_symmetric((1, col), Pawn('pawn_black'), twice=True)

    def reverse_board(self):
        # self.squares = [row[::-1] for row in self.squares[::-1]]
        self.pieces = {(row - 7, col - 7): piece for (row, col), piece in self.pieces.items()}
        self.update_board()

    def get_piece(self, row, col):
        """

        :param row:
        :param col:
        :return:
        """
        return self.pieces.get((row, col))

    def clear_board(self):
        """This func clears the board from possible movements, shows only the pieces."""

        for row, col in self.possible_movements:
            square_btn = self.squares[row][col]
            square_btn.config(bg=square_btn.bg)  # default square background color

    def get_possible_movements(self, square):
        """
        This func updates the piece's optional movements.
        :type square: SquareBtn
        """

        # set moving piece
        self.moving_piece = square
        self.possible_movements = self.get_piece(*square.get_point()).get_movements(square.get_point(), self.squares)

    def button_command(self, point):

        self.clear_board()

        row, col = point

        square_btn = self.squares[row][col]
        piece = square_btn.piece

        if piece and piece.is_white == self.white_turn:  # choose piece to move
            self.get_possible_movements(square_btn)

        elif square_btn.get_point() in self.possible_movements:  # move piece to destination
            self.move_piece(self.moving_piece, square_btn)

        self.update_board()

    def move_piece(self, src_square, dst_square):
        """
        This func moves the
        :param src_square:
        :param dst_square:
        :return:
        """

        # move piece from src to dst
        dst_square.piece = src_square.piece
        src_square.piece = None
        self.moving_piece = None
        self.possible_movements = []
        # change turn
        self.white_turn = not self.white_turn
        self.reverse_board()
        self.clear_board()

    def update_board(self):
        """This func updates the pieces and possible movements."""

        for row in xrange(8):
            for col in xrange(8):

                square_btn = self.squares[row][col]

                if self.get_piece(row, col):

                    print square_btn.piece.icon_path
                    square_btn.config(image=square_btn.piece.icon)
                    square_btn.image = square_btn.piece.icon
                else:
                    square_btn.config(image='')
                    square_btn.image = ''

                if (row, col) in self.possible_movements:
                    square_btn.config(bg="green")

    def starting(self):

        self.set_starting_pieces()
        square_style = {'borderwidth': 0, 'width': 5, 'height': 2}

        # create responsive board as 8x8 grid
        for row in xrange(8):
            row_squares = []

            Grid.rowconfigure(self.root, row, weight=1)

            for col in xrange(8):
                Grid.columnconfigure(self.root, col, weight=1)

                if (9 * row + col) % 2 == 0:
                    square_color = 'white'
                else:
                    square_color = 'grey'

                square_btn = SquareBtn(parent=self.root, row=row, col=col, bg=square_color, **square_style)
                square_btn.grid(row=row, column=col, sticky='nsew')

                square_piece = self.pieces.get((row, col))
                if square_piece:
                    square_btn.config(image=square_piece.icon)
                    square_btn.image = square_piece.icon
                    square_btn.piece = square_piece

                square_btn.config(command=lambda x=(row, col): self.button_command(x))

                row_squares.append(square_btn)
            self.squares.append(row_squares)

    def __init__(self):

        self.root = Tk()
        self.root.title('Chess')
        self.root.geometry('500x500')

        self.pieces = {}
        self.squares = []
        self.white_turn = True

        self.possible_movements = []
        self.moving_piece = None

        self.starting()

    def start(self):
        if self.root:
            self.root.mainloop()


class SquareBtn(Button):

    def __init__(self, parent, row, col, bg, piece=None, *args, **kwargs):
        """

        :param parent:
        :param row:
        :param col:
        :type piece:
        :return:
        """

        Button.__init__(self, parent, bg=bg, *args, **kwargs)
        self.row = row
        self.col = col
        self.bg = bg

    def set_background(self, color):
        """

        :param color:
        :return:
        """
        self.config(bg=color)

    def get_point(self):
        """

        :return:
        """
        return self.row, self.col


