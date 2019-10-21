import sys
from chess.engine.pieces.pawn import Pawn
from chess.engine.pieces.knight import Knight
from chess.engine.pieces.bishop import Bishop
from chess.engine.pieces.rook import Rook
from chess.engine.pieces.queen import Queen
from chess.engine.pieces.king import King
from chess.engine.square import Square
from chess.engine.state import State
from chess.engine.position import Position
from chess.engine.moves.standard_move import StandardMove
from chess.engine.moves.passing import Passing
from chess.engine.moves.castling import Castling
from chess.engine.moves.promotion import Promotion
from chess.engine.utils import *
import csv
import numpy as np
import random
import time

class Config(object):
    def __init__(self):
        # True : White turn  False : Black turn
        self.player = True
        # 2D array which contains 8*8 squares
        self.board = self.init_board()
        self.state = State()
        self.update_threats()

    def reset(self):
        self.player = True
        self.board = self.init_board()
        self.state = State()

    def init_board(self):
        board = [[0 for i in range(8)] for j in range(8)]
        for i in range(0,8):
            board[i][1] = Square(Pawn(False))
            board[i][2] = Square(None)
            board[i][3] = Square(None)
            board[i][4] = Square(None)
            board[i][5] = Square(None)
            board[i][6] = Square(Pawn(True))
        board[0][0] = Square(Rook(False))
        board[1][0] = Square(Knight(False))
        board[2][0] = Square(Bishop(False))
        board[3][0] = Square(Queen(False))
        board[4][0] = Square(King(False))
        board[5][0] = Square(Bishop(False))
        board[6][0] = Square(Knight(False))
        board[7][0] = Square(Rook(False))
        board[0][7] = Square(Rook(True))
        board[1][7] = Square(Knight(True))
        board[2][7] = Square(Bishop(True))
        board[3][7] = Square(Queen(True))
        board[4][7] = Square(King(True))
        board[5][7] = Square(Bishop(True))
        board[6][7] = Square(Knight(True))
        board[7][7] = Square(Rook(True))
        return board

    def set_state(self, previous):
        self.state.black_king_castle = previous.black_king_castle
        self.state.black_queen_castle = previous.black_queen_castle
        self.state.white_king_castle = previous.white_king_castle
        self.state.white_queen_castle = previous.white_queen_castle
        self.state.ep_col = previous.ep_col
        self.state.fifty_moves_rules = previous.fifty_moves_rules
        for i in range(5):
            self.state.white_history[i] = previous.white_history[i]
            self.state.black_history[i] = previous.black_history[i]


    # Update castling rights, fifty moves rule, en passant and history.
    def update_state(self, move):
        encode = abs(move.moving_piece.encode)
        from_x = move.start.x
        from_y = move.start.y
        to_x = move.dest.x
        to_y = move.dest.y
        # update castling
        if self.player:
            if encode == 6:
                self.state.white_king_castle = False
                self.state.white_queen_castle = False
            elif encode == 4:
                if from_x == 0:
                    self.state.white_queen_castle = False
                elif from_x == 7:
                    self.state.white_king_castle = False
            if to_x == 0 and to_y == 0:
                    self.state.black_queen_castle = False
            elif to_x == 7 and to_y == 0:
                    self.state.black_king_castle = False
            for i in range(4,0,-1):
                self.state.white_history[i] = self.state.white_history[i-1]
            self.state.white_history[0] = self.hashh()
        else:
            if encode == 6:
                self.state.black_king_castle = False
                self.state.black_queen_castle = False
            elif encode == 4:
                if from_x == 0:
                    self.state.black_queen_castle = False
                elif from_x == 7:
                    self.state.black_king_castle = False
            if to_x == 0 and to_y == 7:
                    self.state.white_queen_castle = False
            elif to_x == 7 and to_y == 7:
                    self.state.white_king_castle = False
            for i in range(4,0,-1):
                self.state.black_history[i] = self.state.black_history[i-1]
            self.state.black_history[0] = self.hashh()
        # update ep state
        if encode == 1 and abs(to_y-from_y) == 2:
            self.state.ep_col = from_x
        else:
            self.state.ep_col = -1
        # update fifty moves rules
        if move.deleted_piece is None and abs(move.moving_piece.encode) != 1:
            self.state.fifty_moves_rules += 1
        else:
            self.state.fifty_moves_rules = 0

    def update_threats(self):
        pieces = []
        for i in range(8):
            for j in range(8):
                self.board[i][j].reset_threat()
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece != None:
                    posList = piece.get_threats_pos(i,j,self)
                    for pos in posList:
                        self.board[pos.x][pos.y].set_threat(piece.color)

    # Return an array representing both white and black threats.
    def threats_array(self):
        res = np.zeros((8,8))
        for i in range(8):
            for j in range(8):
                black_threat = self.board[i][j].is_threat(False)
                white_threat = self.board[i][j].is_threat(True)
                if black_threat and white_threat:
                    res[i][j] = 2
                elif white_threat:
                    res[i][j] = 1
                elif black_threat:
                    res[i][j] = -1
        return res

    def set_threats(self,array):
        for i in range(8):
            for j in range(8):
                self.board[i][j].reset_threat()
        for i in range(8):
            for j in range(8):
                square = self.board[i][j]
                threats = array[i][j]
                if threats == 2:
                    square.set_threat(False)
                    square.set_threat(True)
                elif threats == 1:
                    square.set_threat(True)
                elif threats == -1:
                    square.set_threat(False)

    # Indicate if player is check. Kings could be stored to avoid searching them.
    def is_check(self, player):
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece != None and abs(piece.encode) == 6 and piece.color == player:
                    return self.board[i][j].is_threat(not(player))


    # If valid, play the movement specified by start and dest positions.
    def try_play(self, start, dest):
        if start == None or dest == None:
            return False
        move = self.get_pseudo_legal_move(start,dest)
        if move and move.is_legal(self):
            self.apply_move(move,True)
            return True
        return False

    # If valid, returns a pseudo legal move from chess.engine.start and dest positions.
    def get_pseudo_legal_move(self, start, dest):
        x1 = start.x
        y1 = start.y
        x2 = dest.x
        y2 = dest.y
        res = True
        move = None
        while True:
            if x1 < 0 or x1 > 7 or y1 < 0 or y1 > 7:
                print("Invalid start square")
                res = False
                break
            start_square = self.board[x1][y1]
            dest_square = self.board[x2][y2]
            if start_square.is_empty():
                print("Empty start square")
                res = False
                break
            moving_piece = start_square.piece
            if moving_piece.color != self.player :
                print("Start square contains an opponent piece")
                res = False
                break
            if x2 < 0 or x2 > 7 or y2 < 0 or y2 > 7:
                print("Invalid destination square")
                res = False
                break
            if not(dest_square.is_empty()) and dest_square.piece.color == self.player :
                print("Destination square contains an ally piece ")
                res = False
                break
            if not(moving_piece.can_pseudo_move(start, dest, self)) :
                print("Destination square can not be reached by the piece")
                res = False
                break
            move = self.create_move(start,dest,moving_piece)
            break
        return move

    # Returns a pseudo legal move from chess.engine.start and dest positions.
    def create_move(self, start, dest, moving_piece):
        encode = abs(self.board[start.x][start.y].piece.encode)
        if encode == 6 and abs(start.x-dest.x) > 1:
            if dest.x == 2:
                return Castling(start,dest, moving_piece, self.board[0][dest.y].piece)
            elif dest.x == 6:
                return Castling(start,dest, moving_piece, self.board[7][dest.y].piece)
        elif encode == 1 and dest.y%7 == 0:
            return Promotion(start,dest,moving_piece)
        elif encode == 1 and self.board[dest.x][dest.y].is_empty() and start.x != dest.x:
            return Passing(start,dest,moving_piece)
        else:
            return StandardMove(start,dest,moving_piece)

    # Return the list of legal moves for the current player.
    def get_legal_moves(self):
        moves = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j].piece
                if piece != None and piece.color == self.player:
                    posList = piece.get_pseudo_legal_pos(i,j,self)
                    # loop on the possible positions (pseudoLegalMoves) of a piece
                    for pos in posList:
                        move = self.create_move(Position(i,j),pos,piece)
                        if move.is_legal(self):
                            moves.append(move)
        return moves

    # Return winner of the game and list of legal moves if the game is not over.
    def winner(self):
        if self.state.fifty_moves_rules > 50:
            return 0, None
        elif self.state.white_history[4] == self.state.white_history[2] and self.state.white_history[2] == self.state.white_history[0]:
            return 0, None
        elif self.state.black_history[4] == self.state.black_history[2] and self.state.black_history[2] == self.state.black_history[0]:
            return 0, None
        moves = self.get_legal_moves()
        if len(moves) == 0:
            if self.is_check(self.player):
                if self.player:
                    return 1, moves
                else:
                    return -1, moves
            else:
                return 0, None
        else:
            return None, moves

    # Remember current state, apply the move and update config's state
    # The move is not "real" if it is called in is_legal, because it is canceled after.
    def apply_move(self,move,real):
        if not(real):
            move.previous_state = State(self.state)
            move.previous_threats = self.threats_array()
        move.apply(self)
        self.update_state(move)
        self.update_threats()
        if real:
            self.player = not(self.player)

    # Cancel a move and restore last state.
    def cancel_move(self,move):
        move.cancel(self)
        self.set_state(move.previous_state)
        self.set_threats(move.previous_threats)
        move.previous_state = None
        move.previous_threats = None

    # Allows to hash an array representation of the configuration. Used for three repetitions rule.
    def hashh(self):
        res = np.zeros((397))
        index = 0
        for i in range(8):
            for j in range(8):
                if not(self.board[j][i].is_empty()):
                    piece = self.board[j][i].piece
                    res[index+piece.encode-1] = np.sign(piece.encode)
                index += 6
        res[index] = self.player
        index += 1
        res[index] += self.state.black_king_castle
        index += 1
        res[index] += self.state.black_queen_castle
        index += 1
        res[index] += self.state.white_king_castle
        index += 1
        res[index] += self.state.white_queen_castle
        index += 1
        if self.state.ep_col != -1:
            res[index+self.state.ep_col] = 1
        res.flags.writeable = False
        return hash(res.data.tobytes())
