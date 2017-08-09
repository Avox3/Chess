

from Tkinter import Tk, Grid, Button

from pieces import Pawn, Bishop, Knight, Rook, Queen, King, BLACK, WHITE


class ChessBoard:

    def get_symmetric(self, point, piece, twice=False):
        """

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

        for point, piece in curr_pieces.items():
            curr_pieces[(7-point[0], point[1])] = piece.__class__(icon)

        self.pieces.update(curr_pieces)

    def set_starting_pieces(self):
        """

        :return:
        """

        # first row pieces
        self.get_symmetric((0, 0), Rook('rook_black'), twice=True)
        self.get_symmetric((0, 1), Rook('knight_black'), twice=True)
        self.get_symmetric((0, 2), Rook('bishop_black'), twice=True)

        self.get_symmetric((0, 3), Pawn('queen_black'))
        self.get_symmetric((0, 4), Pawn('king_black'))

        # second row pieces - pawns
        for col in xrange(8):
            self.get_symmetric((1, col), Pawn('pawn_black'))

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

    def clear_board(self):
        """

        :return:
        """
        for row in xrange(8):
            for col in xrange(8):
                self.squares[row][col].movement = False

    def show_possible_movements(self, piece):
        """

        :param piece:
        :return:
        """

        self.clear_board()  # clear previous possible movements

        movements = piece.get_movements()
        for (row, col) in movements:
            self.squares[row][col].movement = True

        self.update_board()

    def button_command(self, square_btn):

        if square_btn.piece:  # choose piece to move

            piece = square_btn.piece
            if not piece.is_white == self.white_turn:
                return

            self.possible_movements = piece.get_movements(square_btn.get_point(), self.squares)
            self.moving_piece = piece

            for movement in self.possible_movements:
                print 'wtf'
                self.squares[movement[0]][movement[1]].set_background('green')

        else:  # move piece to destination
            if square_btn.get_point() in self.possible_movements:
                self.move_piece(self.moving_piece, square_btn)
            else:
                self.clear_board()

        self.update_board()

    def move_piece(self, src_square, dst_square):

        dst_square.piece = src_square.piece
        src_square.piece = None

    def update_board(self):

        for row in xrange(8):

            for col in xrange(8):

                square_btn = self.squares[row][col]
                square_btn.config(command=lambda x=square_btn: self.button_command(x))

                if square_btn.piece:
                    square_btn.config(image=square_btn.piece.icon)
                    square_btn.image = square_btn.piece.icon

    def starting(self):

        self.set_starting_pieces()
        square_style = {'borderwidth': 0, 'width': 5, 'height': 2}
        row_squares = []

        # create responsive board as 8x8 grid
        for row in xrange(8):
            Grid.rowconfigure(self.root, row, weight=1)

            for col in xrange(8):
                Grid.columnconfigure(self.root, col, weight=1)

                if (9 * row + col) % 2 == 0 :
                    square_color = 'white'
                else:
                    square_color = 'grey'

                square_btn = SquareBtn(self.root, row, col, bg=square_color, **square_style)
                square_btn.grid(row=row, column=col, sticky='nsew')

                square_piece = self.pieces.get((row, col))
                if square_piece:
                    square_btn.config(image=square_piece.icon)
                    square_btn.image = square_piece.icon

                row_squares.append(square_btn)

            self.squares.append(row_squares)

    def __init__(self):

        self.root = Tk()
        self.root.title('Chess')

        self.pieces = {}
        self.squares = []
        self.white_turn = True

        self.possible_movements = []
        self.moving_piece = None

        self.starting()
        self.update_board()

    def start(self):
        if self.root:
            self.root.mainloop()


class SquareBtn(Button):

    def __init__(self, parent, row, col, piece=None, movement=False, *args, **kwargs):
        """

        :param parent:
        :param row:
        :param col:
        :type piece:
        :param piece:
        :param movement:
        :return:
        """

        Button.__init__(self, parent, *args, **kwargs)
        self.row = row
        self.col = col
        self.piece = piece
        self.movement = movement

    def set_background(self, color):
        """

        :param color:
        :return:
        """
        self.configure(bg=color)

    def get_point(self):
        """

        :return:
        """
        return [self.row, self.col]


