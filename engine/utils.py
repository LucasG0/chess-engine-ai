from chess.engine.position import Position
from termcolor import colored
import colorama
import numpy as np

def number(char):
    if char == 'a':
        return 0
    elif char == 'b':
        return 1
    elif char == 'c':
        return 2
    elif char == 'd':
        return 3
    elif char == 'e':
        return 4
    elif char == 'f':
        return 5
    elif char == 'g':
        return 6
    elif char == 'h':
        return 7
    else:
        return None

def ask():
    move = input()
    if len(move) != 4:
        return None, None
    from_x = number(move[0])
    if from_x == None:
        return None, None
    if not(move[1].isdigit()) or int(move[1]) >= 8:
        return None, None
    from_y = 8-int(move[1])
    to_x = number(move[2])
    if to_x == None:
        return None, None
    if not(move[3].isdigit()) or int(move[3]) >= 8:
        return None, None
    to_y = 8-int(move[3])

    return Position(from_x,from_y), Position(to_x,to_y)

def ask_test(move):
    from_x = number(move[0])
    from_y = 8-int(move[1])
    to_x = number(move[2])
    to_y = 8-int(move[3])
    if len(move) > 4 and move[4] != "q":
        bad_prom = True
    else:
        bad_prom = False
    return Position(from_x,from_y), Position(to_x,to_y), bad_prom

def show(config):
    board = config.board
    colorama.init()
    print("")
    print("     A   B   C   D   E   F   G   H")
    print("")
    for i in range(8):
        print("   ---------------------------------")
        print(str(8-i) + "  | ", end='')
        for j in range(8):
            piece = board[j][i].piece
            if piece != None:
                if piece.color:
                    color = 'white'
                else:
                    color = 'blue'
                print(colored(piece.name, color), end='')
                print(" | ", end='')
            else:
                print(" " + " | ", end='')
        print("  " + str(8-i))
    print("   ---------------------------------")
    print("")
    print("     A   B   C   D   E   F   G   H")
    print("")
    if config.player:
        print("                WHITES TURN")
    else:
        print("                BLACKS TURN")

def show_threat(config):
    board = config.board
    print("                THREATS")
    print("")
    print("     A    B    C    D    E    F    G    H ")
    print("")
    for i in range(8):
        print("   ---------------------------------------")
        print(str(8-i) + "  | ", end='')
        for j in range(8):
            char = ""
            if board[j][i].white_threat:
                char += "W"
            else:
                char += " "
            if board[j][i].black_threat:
                char += "B"
            else:
                char += " "
            print(char, end='')
            print(" | ", end='')
        print("  " + str(8-i))
    print("   ---------------------------------------")
    print("")
    print("     A   B   C   D   E   F   G   H")
    print("")

def show_winner(winner):
    print(winner)
    if winner == 1:
        print("WHITE PLAYER WON")
    elif winner == -1:
        print("BLACK PLAYER WON")
    else:
        print("IT'S A DRAW")

def encode(config):
    res = np.zeros((8,8,25),np.bool_)
    if config.player:
        for i in range(8):
            for j in range(8):
                if not(config.board[j][i].is_empty()):
                    piece = config.board[j][i].piece
                    if piece:
                        if piece.color:
                            res[j][i][piece.encode-1] = 1
                        else:
                            res[j][i][piece.encode+5] = 1
                    res[j][i][12] = int(config.player)
                    res[j][i][13] = int(config.state.white_queen_castle)
                    res[j][i][14] = int(config.state.white_king_castle)
                    res[j][i][15] = int(config.state.black_queen_castle)
                    res[j][i][16] = int(config.state.black_king_castle)
                    if config.state.ep_col != -1:
                        res[j][i][17+config.state.ep_col] = 1
    else:
        for i in range(8):
            for j in range(8):
                if not(config.board[7-j][7-i].is_empty()):
                    piece = config.board[7-j][7-i].piece
                    if piece:
                        if piece.color:
                            res[j][i][piece.encode-1] = 1
                        else:
                            res[j][i][piece.encode+5] = 1
                    res[j][i][12] = int(config.player)
                    res[j][i][13] = int(config.state.black_king_castle)
                    res[j][i][14] = int(config.state.black_queen_castle)
                    res[j][i][15] = int(config.state.white_king_castle)
                    res[j][i][16] = int(config.state.white_queen_castle)
                    if config.state.ep_col != -1:
                        res[j][i][17+config.state.ep_col] = 1
    return res
