"""
Support code for the Chess Game
Assignment 1
Semester 2, 2021
CSSE1001/CSSE7030
"""
from typing import Optional, Tuple

BLACK_PAWN = "p"
BLACK_ROOK = "r"
BLACK_KNIGHT = "n"
BLACK_BISHOP = "b"
BLACK_KING = "k"
BLACK_QUEEN = "q"

WHITE_PAWN = "P"
WHITE_ROOK = "R"
WHITE_KNIGHT = "N"
WHITE_BISHOP = "B"
WHITE_KING = "K"
WHITE_QUEEN = "Q"

EMPTY = "."

BLACK_PIECES = (
    BLACK_ROOK,
    BLACK_KNIGHT,
    BLACK_BISHOP,
    BLACK_QUEEN,
    BLACK_KING,
    BLACK_BISHOP,
    BLACK_KNIGHT,
    BLACK_ROOK,
    BLACK_PAWN,
)

WHITE_PIECES = (
    WHITE_ROOK,
    WHITE_KNIGHT,
    WHITE_BISHOP,
    WHITE_QUEEN,
    WHITE_KING,
    WHITE_BISHOP,
    WHITE_KNIGHT,
    WHITE_ROOK,
    WHITE_PAWN,
)

BOARD_SIZE = 8
HELP_MESSAGE = (
    "\nWelcome to Chess!\nWhen it's your turn, enter one of the"
    + " following:\n1) 'h' or 'H': Print the help menu\n2) 'q' or 'Q': Quit "
    + "the game\n3) position1 position2: The positions (as letterNumber) to "
    + "move from and to respectively.\n"
)

# Direction deltas that pieces can move in
ROOK_DELTAS = ((0, 1), (1, 0), (0, -1), (-1, 0))
BISHOP_DELTAS = ((-1, -1), (1, 1), (-1, 1), (1, -1))
QUEEN_DELTAS = KING_DELTAS = ROOK_DELTAS + BISHOP_DELTAS
KNIGHT_DELTAS = (
    (1, 2),
    (2, 1),
    (-2, 1),
    (1, -2),
    (-1, 2),
    (2, -1),
    (-1, -2),
    (-2, -1),
)

# Type aliases
Board = Tuple[str, str, str, str, str, str, str, str]
Position = Tuple[int, int]
Move = Tuple[Position, Position]


def pawn_attacking_deltas(
    is_white: bool,
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Return the deltas, which when added to a pawn's position, give the
    positions it would be attacking, given the supplied pawn's colour.

    Parameters:
        is_white (bool): True iff the pawn is white.

    Returns:
        (tuple<tuple<int, int>>): The corresponding attacking deltas.
    """
    if is_white:
        return ((-1, -1), (-1, 1))
    return ((1, -1), (1, 1))


def out_of_bounds(position: Position) -> bool:
    """Determines whether the given position exists on the board.

    Parameters:
        position (Position): The (row, col) position to be checked.

    Returns:
        (bool): True iff the position is out of bounds.
    """
    row, col = position
    return row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE


def piece_at_position(position: Position, board: Board) -> str:
    """Determines the piece (character) at the given position on the board.

    Parameters:
        position (Position): The (row, col) position.
        board (Board): The current board state.

    Returns:
        (str): The character at the position in the board state.
    """
    row, col = position
    return board[row][col]


def valid_position_format(position: str) -> bool:
    """(bool) Returns True iff position in in the correct form.

    Parameters:
        position (str): A position in a raw string format.

    Examples:
        >>> valid_position_format("h2")
        True
        >>> valid_position_format("h4")
        True
    """
    if len(position) != 2:
        return False

    return "a" <= position[0].lower() <= "h" and "1" <= position[1] <= "8"


def valid_move_format(move: str) -> bool:
    """(bool) Returns True iff move is in the correct form.

    Parameters:
        move (str): The raw input from the user.

    Examples:
        >>> valid_move_format("h2 h4")
        True
    """
    origin, _, destination = move.partition(" ")

    return valid_position_format(origin) and valid_position_format(destination)


def find_piece(piece: str, board: Board) -> Optional[Position]:
    """Returns the position of the piece in the board. If the piece is
        non-unique, the first one found (lowest row, lowest col) will be
        returned. If the piece cannot be found on the board, None is returned.

    Parameters:
        piece (str): The character we are looking for.
        board (Board): The current board state.

    Returns:
        (Position | None): The position of piece in the board.
    """
    for row, row_str in enumerate(board):
        for col, square in enumerate(row_str):
            if square == piece:
                return (row, col)
    return None


def get_pawn_moves(
    position: Position, board: Board, piece: str
) -> Tuple[Position, ...]:
    """Returns the valid moves for the pawn at the given position on board.

    Parameters:
        position (Position): The (row, col) position to move from.
        board (Board): The current board state.
        piece (str): WHITE_PAWN or BLACK_PAWN, depending on the colour of pawn.

    Returns:
        (tuple<Position>): A tuple of all the (row, col) positions
                                  reachable by the piece at position.
    """
    moves: Tuple[Position, ...] = ()

    # Movement direction depends on piece colour
    if piece == WHITE_PAWN:
        start_row = 6
        other_pieces = BLACK_PIECES
        direction = -1
    else:
        start_row = 1
        other_pieces = WHITE_PIECES
        direction = 1

    # Four cases to check
    forward_move = position[0] + direction, position[1]
    diag_left_move = position[0] + direction, position[1] - 1
    diag_right_move = position[0] + direction, position[1] + 1
    start_move = position[0] + 2 * direction, position[1]

    # Check validity for each move
    if not out_of_bounds(forward_move):
        piece_at_move = piece_at_position(forward_move, board)
        if piece_at_move == EMPTY:
            moves += (forward_move,)

    for move in (diag_left_move, diag_right_move):
        if not out_of_bounds(move):
            piece_at_move = piece_at_position(move, board)
            if piece_at_move in other_pieces:
                moves += (move,)

    if not out_of_bounds(start_move) and position[0] == start_row:
        piece_at_middle = piece_at_position(forward_move, board)
        piece_at_move = piece_at_position(start_move, board)
        if piece_at_middle == EMPTY and piece_at_move == EMPTY:
            moves += (start_move,)

    return moves


def get_possible_moves(
    position: Position, board: Board
) -> Tuple[Position, ...]:
    """Returns all of the positions reachable in one move by the piece at
        the given position.

    Parameters:
        position (Position): The (row, col) position to move from.
        board (Board): The current board state.

    Returns:
        (tuple<Position>): A tuple of all the (row, col) positions
                                  reachable by the piece at position.
    """
    piece = piece_at_position(position, board)
    moves: Tuple[Position, ...] = ()

    if piece == EMPTY:
        return moves  # no piece here, so no valid moves

    # Pawns
    if piece in (WHITE_PAWN, BLACK_PAWN):
        return get_pawn_moves(position, board, piece)

    # Non extendable paths: king, knight
    if piece in (BLACK_KING, WHITE_KING, BLACK_KNIGHT, WHITE_KNIGHT):
        deltas: Tuple[Position, ...] = (
            KING_DELTAS if piece in (BLACK_KING, WHITE_KING) else KNIGHT_DELTAS
        )

        for d_row, d_col in deltas:
            candidate_position = position[0] + d_row, position[1] + d_col

            if out_of_bounds(candidate_position):
                continue

            candidate_row, candidate_column = candidate_position
            piece_at_candidate = board[candidate_row][candidate_column]
            if piece_at_candidate == EMPTY:
                moves += (candidate_position,)
            elif (piece in BLACK_PIECES) is not (
                piece_at_candidate in BLACK_PIECES
            ):
                # The pieces are different colours
                # so we can take it by moving here.
                moves += (candidate_position,)

    # Extendable paths: rook, bishop, queen
    if piece in (
        WHITE_ROOK,
        BLACK_ROOK,
        WHITE_BISHOP,
        BLACK_BISHOP,
        WHITE_QUEEN,
        BLACK_QUEEN,
    ):
        if piece in (WHITE_ROOK, BLACK_ROOK):
            deltas = ROOK_DELTAS
        elif piece in (BLACK_BISHOP, WHITE_BISHOP):
            deltas = BISHOP_DELTAS
        else:
            deltas = QUEEN_DELTAS

        for delta in deltas:
            d_row, d_col = delta
            candidate_position = position
            # Follow the direction out until either dimension is out of bounds
            while True:
                candidate_position = (
                    candidate_position[0] + d_row,
                    candidate_position[1] + d_col,
                )

                if out_of_bounds(candidate_position):
                    break

                # Make sure there's nothing blocking the square
                candidate_row, candidate_column = candidate_position
                piece_at_candidate = board[candidate_row][candidate_column]
                if piece_at_candidate == EMPTY:
                    moves += (candidate_position,)
                elif (piece in BLACK_PIECES) is not (
                    piece_at_candidate in BLACK_PIECES
                ):
                    # We can move here to take the piece
                    # but we can't move through it
                    moves += (candidate_position,)
                    break
                else:
                    break  # One of our own pieces is blocking

    return moves


def is_in_check(board: Board, whites_turn: bool) -> bool:
    """Determine if the player whose turn it is, is in check.

    Parameters:
        board (Board): The current board state
        whites_turn (bool): True iff it's white's turn.

    Returns:
        (bool): True iff the current player is in check.
    """
    king = WHITE_KING if whites_turn else BLACK_KING
    king_position = find_piece(king, board)
    enemy_pieces = BLACK_PIECES if whites_turn else WHITE_PIECES

    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            position = (i, j)
            if piece in enemy_pieces and king_position in get_possible_moves(
                position, board
            ):
                return True
    return False
