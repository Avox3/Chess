

from Tkinter import Tk, Grid, Button

from pieces import ChessPiece, Pawn, Bishop, Knight, Rook, Queen, King


class ChessBoard:

    def get_symmetric(self, point, piece_type, twice=False):
        """
        Creates pieces of both sides by piece's type and location in the board.
        :param point: the location
        :type point: tuple
        :param piece_type: type is the piece
        :type piece_type: instance of ChessPiece
        :param twice: piece exists twice in the board for each side
        """

        if piece_type.__base__ is not ChessPiece:  # check if inherit from ChessPiece
            return

        curr_pieces = []

        # set black side
        icon_path = piece_type.__name__.lower() + '_black'
        curr_pieces.append(piece_type(*point, icon_path=icon_path))

        if twice:
            row, col = point
            curr_pieces.append(piece_type(row, 7 - col, icon_path=icon_path))

        # set white side
        icon_path = piece_type.__name__.lower() + '_white'

        for piece in curr_pieces:
            row, col = piece.get_point()
            self.pieces.append(piece_type(7 - row, col, icon_path=icon_path))

        self.pieces += curr_pieces

    def set_starting_pieces(self):
        """ Sets starting pieces. """

        # first row pieces
        self.get_symmetric((0, 0), Rook, twice=True)
        self.get_symmetric((0, 1), Knight, twice=True)
        self.get_symmetric((0, 2), Bishop, twice=True)

        self.get_symmetric((0, 3), Queen)
        self.get_symmetric((0, 4), King)

        # second row pieces - pawns
        for col in xrange(4):
            self.get_symmetric((1, col), Pawn, twice=True)

    def switch_side(self):
        """ Switches side of the board. """

        for piece in self.pieces:
            row, col = piece.get_point()
            piece.set_point(7 - row, 7 - col)

        self.update_board()

    def get_piece(self, row, col):
        """
        Returns piece by location.
        :param row: x coordinate on the board
        :param col: y coordinate on the board
        :rtype: ChessPiece | None
        """

        for piece in self.pieces:
            if piece.get_point() == (row, col):
                return piece

    def clear_board(self):
        """ Clears the board from possible movements, shows only the pieces. """

        for row, col in self.possible_movements:
            square_btn = self.squares[row][col]
            square_btn.config(bg=square_btn.bg)  # default square background color

    def get_possible_movements(self, square):
        """
        Updates the piece's optional movements.
        :type square: SquareBtn
        """

        # set moving piece
        self.moving_piece = self.get_piece(*square.get_point())
        if not self.moving_piece:
            return
        self.possible_movements = self.moving_piece.get_movements(self.pieces)

    def button_command(self, point):
        """
        Handle any type of click on the board.
        :param point: location of the clicked square
        :rtype point: tuple
        """

        # clear previous click changes
        self.clear_board()

        row, col = point
        square_btn = self.squares[row][col]
        piece = self.get_piece(row, col)

        if piece and piece.is_white == self.white_turn:  # choose piece to move
            self.get_possible_movements(square_btn)

        elif (row, col) in self.possible_movements:  # move piece to destination
            self.move_piece(square_btn)

        self.update_board()

    def move_piece(self, dst_square):
        """
        Moves the piece to destination square.
        :type dst_square: SquareBtn
        """

        row, col = dst_square.get_point()
        enemy_piece = self.get_piece(row, col)
        if enemy_piece:
            self.pieces.remove(enemy_piece)

        # move piece to destination square
        self.moving_piece.set_point(*dst_square.get_point())
        self.moving_piece = None
        self.possible_movements = []

        # change turn
        self.white_turn = not self.white_turn
        self.switch_side()

    def update_board(self):
        """ Updates pieces and possible movements. """

        for row in xrange(8):
            for col in xrange(8):

                square_btn = self.squares[row][col]
                piece = self.get_piece(row, col)
                if piece:

                    square_btn.config(image=piece.icon)
                    square_btn.image = piece.icon
                else:
                    square_btn.config(image='')

                if (row, col) in self.possible_movements:
                    square_btn.config(bg="green")

    def starting(self):
        """ Creates the board's rows and columns. """

        # create pieces
        self.set_starting_pieces()
        square_style = {'borderwidth': 0, 'width': 5, 'height': 2}

        # create responsive board as 8x8 grid
        for row in xrange(8):
            row_squares = []

            Grid.rowconfigure(self.root, row, weight=1)

            for col in xrange(8):
                Grid.columnconfigure(self.root, col, weight=1)

                if (row + col) % 2 == 0:
                    square_color = 'white'
                else:
                    square_color = 'grey'

                square_btn = SquareBtn(parent=self.root, row=row, col=col, bg=square_color, **square_style)
                square_btn.grid(row=row, column=col, sticky='nsew')

                square_piece = self.get_piece(row, col)
                if square_piece:
                    square_btn.config(image=square_piece.icon)
                    square_btn.image = square_piece.icon

                square_btn.config(command=lambda x=(row, col): self.button_command(x))

                row_squares.append(square_btn)
            self.squares.append(row_squares)

    def __init__(self):

        self.root = Tk()
        self.root.title('Chess')
        self.root.geometry('600x600')

        self.pieces = []
        self.squares = []
        self.white_turn = True

        self.possible_movements = []
        self.moving_piece = None

        self.starting()

    def start(self):
        if self.root:
            self.root.mainloop()


class SquareBtn(Button):

    def __init__(self, parent, row, col, bg, *args, **kwargs):
        """
        Create square.
        :param parent: the layer on which it exists
        :param row: x coordinate on the board
        :param col: y coordinate on the board
        """

        Button.__init__(self, parent, bg=bg, *args, **kwargs)
        self.row = row
        self.col = col
        self.bg = bg

    def set_background(self, color):
        """
        Sets square's background color.
        :type color: string
        """
        self.config(bg=color)

    def get_point(self):
        """ Returns square's location. """
        return self.row, self.col
