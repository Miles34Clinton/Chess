
"""
Chess Game
Assignment 1
Semester 2, 2021
CSSE1001/CSSE7030
"""

from typing import Optional, Tuple

from a1_support import *

# Replace these <strings> with your name, student number and email address.
__author__ = "<boxiang yang>, <46440266>"
__email__ = "<boxiang_yang@uqconnect.edu.au>"


def initial_state() -> Board:
    """Return the board state for a new game.
    Parameters：
        None
    
    Returns:
        (Board): The initial state Board Tuple.
    """
    return (
        'rnbqkbnr',
        'pppppppp',
        '........',
        '........',
        '........',
        '........',
        'PPPPPPPP',
        'RNBQKBNR',
    )
   

def print_board(board: Board) -> None:
    """Print a human-readable board.  
    Parameters：
        board(Board): Board tuple.
    
    Returns:
        (None)
    """
    for index,string in enumerate(board):
        string = string + '  ' + str(8 - index) 
        print(string)
    print('')
    print("abcdefgh")


def square_to_position(square: str) -> Position:
    """Convert chess notation to its(row, col).
    Parameters：
        square(str): Chess notation such as 'a1','e2'.
    
    Returns:
        (Position): Position tuple.
    
    Examples:
        >>> square_to_position('a1')
        (7, 0)
    """
    col = square[0]
    row = square[1]
    row = 8 - int(row)
    col = ord(col) - ord('a')
    return (row, col)
    

def process_move(user_input: str) -> Move:
    """Validte and Convert user_input to (Position, Position).
    Parameters：
        user_input(str): user input string such as 'a1 e2'.
    
    Returns:
        (Move): Move tuple.
    
    Examples:
        >>> process_move('e2 e4')
        ((6, 4), (4, 4))
    """
    square1,square2 = user_input.split()
    return (square_to_position(square1), square_to_position(square2))


def change_position(board: Board, position: Position, character: str) -> Board:
    """Change the character on the position to the charater which is given.
    Parameters：
        board(Board): Board tuple.
        position(Position): The position of charater which will be changed.
        character(str): given character.
    
    Returns:
        (Board): changed board tuple.
    """
    num1 = position[0]
    num2 = position[1]
    line = board[num1][:num2] + character + board[num1][num2 + 1:]
    board_new = board[:num1] + (line, ) + board[num1 + 1:]
    return board_new


def clear_position(board: Board, position: Position) -> Board:
    """Change the character on the position to EMPTY.
    Parameters：
        board(Board): Board tuple.
        position(Position): The position of charater which will be changed.
    
    Returns:
        (Board): changed board tuple.
    """
    return change_position(board, position, EMPTY) 


def update_board(board: Board, move: Move) -> Board:
    """After a moving, make a updated version board. 
    Parameters：
        board(Board): Board tuple.
        move(Move): Move tuple.
    
    Returns:
        (Board): updated version board.
    """  
    origin, destination = move
    board = change_position(board, destination, piece_at_position(origin, board))
    return clear_position(board, origin)


def is_current_players_piece(piece: str, whites_turn: bool) -> bool:
    """Check whether the piece belongs to the current player.
    Parameters：
        piece(str): Piece character.
        whites_turn(bool): current player.
    
    Returns:
        (bool): Whether the piece belongs to the current player.
    """  
    if piece in WHITE_PIECES and whites_turn == True:
        return True
    elif piece in BLACK_PIECES and whites_turn == False:
        return True
    else:
        return False
    

def is_move_valid(move: Move, board: Board, whites_turn: bool) -> bool:
    """Verify that the movement of the chess piece is feasible.
    Parameters：
        move(Move): Move tuple.
        board(Board): Board tuple.
        whites_turn(bool): current player.

    Returns:
        (bool): Whether the move of the chess piece effective.    
    """ 
    origin, destination = move
    positions_are_exist = not out_of_bounds(origin) and not out_of_bounds(destination)
    positions_are_different = not (origin == destination)
    origin_piece = piece_at_position(origin, board)
    destination_piece = piece_at_position(destination, board)
    is_valid_in_chess_rule = destination in get_possible_moves(origin, board)
    if positions_are_exist:
        updated_board = update_board(board, move)
    else:
        return False
    '''print(positions_are_different)
    print(is_current_players_piece(origin_piece, whites_turn))
    print(not is_current_players_piece(destination_piece, whites_turn))
    print(is_valid_in_chess_rule)
    print(not is_in_check(updated_board, whites_turn))'''
    return positions_are_different \
        and is_current_players_piece(origin_piece, whites_turn) \
        and not is_current_players_piece(destination_piece, whites_turn) \
        and is_valid_in_chess_rule \
        and not is_in_check(updated_board, whites_turn)
    

def can_move(board: Board, whites_turn: bool) -> bool:
    """Verify that the chess piece can still move under the condition of being checked.
    Parameters：
        board(Board): Board tuple.
        whites_turn(bool): current player.

    Returns:
        (bool): Whether the chess piece can move while being checked.    
    """ 
    company_pieces = WHITE_PIECES if whites_turn else BLACK_PIECES
    for i, row in enumerate(board):
        for j, piece in enumerate(row):
            origin = (i, j)
            if piece in company_pieces:
                destinations = get_possible_moves(origin, board)
                for destination in destinations:
                    move = (origin, destination)
                    new_board = update_board(board, move)
                    if not is_in_check(new_board, whites_turn):
                        return True
                    else:
                        pass
    return False


def is_stalemate(board: Board, whites_turn: bool) -> bool:
    """Check if the chess piece is stalemate.
    Parameters：
        board(Board): Board tuple.
        whites_turn(bool): current player.

    Returns:
        (bool): Whether the chess piece cannot move without being checked.     
    """ 
    if not is_in_check(board, whites_turn) and not can_move(board, whites_turn):
        return True
    else:
        return False


def check_game_over(board: Board, whites_turn: bool) -> bool:
    """Check if the chess piece is over.
    Parameters：
        board(Board): Board tuple.
        whites_turn(bool): current player.

    Returns:
        (bool): Whether the game is over, if not, determine which side of the chess piece is being checked.
    """ 
    if whites_turn is True:
        current_piece = "White"
    else:
        current_piece = "Black"
    if is_in_check(board, whites_turn) and not can_move(board, whites_turn):
        print('\nCheckmate')
        return True
    elif is_stalemate(board, whites_turn):
        print('\nStalemate')
        return True
    elif is_in_check(board, whites_turn) and can_move(board, whites_turn):
        print(f'\n{current_piece} is in check')
        return False
    else:
        return False
    

def main():
    """Entry point to gameplay"""  
    whites_turn = True 
    board = initial_state ()
    print_board(board)
    while True:
        currenr_player = 'White' if whites_turn else 'Black'
        command = input(f"\n{currenr_player}'s move: ")
        command = command.lower()
        if command == "h":
            print("\nWelcome to Chess!")
            print("When it's your turn, enter one of the following:")
            print("1) 'h' or 'H': Print the help menu")
            print("2) 'q' or 'Q': Quit the game")
            print("3) position1 position2: The positions (as letterNumber) to move from and to respectively.\n")
            print_board(board)
            continue
        elif command == "q":
            next_command = input("Are you sure you want to quit? ")
            next_command = next_command.lower()
            if next_command == "y":
                break
            else:
                print_board(board) 
                continue
        elif valid_move_format(command):
            move = process_move(command)
            if is_move_valid(move, board, whites_turn):
                board = update_board(board, move)
                whites_turn = not whites_turn
                print_board(board)
                if check_game_over(board, whites_turn):
                    break 
                else:
                    pass
            else:
                print("Invalid move\n")
                print_board(board)
        else:
            print("Invalid move\n")
            print_board(board)
        

if __name__ == "__main__":
    main()
