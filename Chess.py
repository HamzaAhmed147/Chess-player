import random as rnd
import copy

column = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


class Piece:
    def __init__(self, typ, pos):
        self.type = typ
        self.pos = pos
        self.score = 0

    def setScore(self, score):
        self.score = score


class Move:
    def __init__(self, piece, pos, kill, k_piece, qcastle=False, kcastle=False):
        self.pos = pos
        self.isKill = kill
        self.piece = piece
        self.k_piece = k_piece
        self.qCastle = qcastle
        self.kCastle = kcastle

    def show(self):
        if self.qCastle:
            return "Queen-side Castle"
        elif self.kCastle:
            return "King-side Castle"
        if self.isKill:
            return (
                    self.piece.type + " at " + self.piece.pos[0] + self.piece.pos[1] + " goes to " + self.pos[0] +
                    self.pos[
                        1] + " and kills")
        else:
            return (self.piece.type + " at " + self.piece.pos[0] + self.piece.pos[1] + " goes to "
                    + self.pos[0] + self.pos[1])


class Team:
    def __init__(self, team):
        self.pieces = []
        self.color = team
        self.initializer()
        self.check = False
        self.checkMate = False

    def initializer(self):
        if self.color == "Black":
            r2 = '7'
            r1 = '8'
        else:
            r1 = '1'
            r2 = '2'
        for col in column:
            self.pieces.append(Piece('Pawn', [col, r2]))
        self.pieces += [Piece('Rook', ['A', r1]), Piece('Rook', ['H', r1]), Piece('Knight', ['B', r1]),
                        Piece('Knight', ['G', r1]), Piece('Bishop', ['C', r1]), Piece('Bishop', ['F', r1]),
                        Piece('Queen', ['D', r1]), Piece('King', ['E', r1])]
        for piece in self.pieces:
            if piece.type == 'King':
                piece.score = 900
            elif piece.type == 'Queen':
                piece.score = 90
            elif piece.type == 'Bishop':
                piece.score = 30
            elif piece.type == 'Knight':
                piece.score = 30
            elif piece.type == 'Rook':
                piece.score = 50
            elif piece.type == 'Pawn':
                piece.score = 10

    def checkCastle(self, t):
        if t == 0:
            count = 0
            for i in self.pieces:
                if 'B' <= i.pos[0] <= 'D':
                    return False
                elif i.type == 'King' and i.pos[0] != 'E':
                    return False
                elif i.type == 'Rook' and i.pos[0] != 'A':
                    if count == 0:
                        count += 1
                    else:
                        return False
        else:
            count = 0
            for i in self.pieces:
                if 'F' <= i.pos[0] <= 'G':
                    return False
                elif i.type == 'King' and i.pos[0] != 'E':
                    return False
                elif i.type == 'Rook' and i.pos[0] != 'H':
                    if count == 0:
                        count += 1
                    else:
                        return False
        return True


class ChessBoard:
    def __init__(self):
        self.black = Team("Black")
        self.white = Team("White")
        self.move = 'White'
        self.staleMate = False

    def doRandomMoves(self, count):
        # assigning team pointer
        if self.move == 'White':
            cur = self.white
        else:
            cur = self.black
        for i in range(count):
            print(cur.color)
            p = rnd.randint(0, len(cur.pieces) - 1)
            moves = self.getPossibleMoves(cur.pieces, cur.color, p)
            if len(moves) > 0:
                m = rnd.randint(0, len(moves) - 1)
                temp = self.performMove(cur, p, moves[m].pos)
                self.set(temp)
            if cur.color == 'White':
                cur = self.black
                self.move = 'Black'
            else:
                cur = self.white
                self.move = 'White'
        print(len(self.black.pieces))
        print(len(self.white.pieces))

    def set(self, temp):
        self.white = temp.white
        self.black = temp.black
        self.move = temp.move
        self.staleMate = temp.staleMate

    def performMove(self, team, index, pos):
        temp = copy.deepcopy(self)
        if team.color == 'White':
            temp.white.pieces[index].pos = copy.deepcopy(pos)
            for piece in temp.black.pieces:
                if piece.pos[0] == pos[0] and piece.pos[1] == pos[1]:
                    if piece.type == 'King':
                        self.white.checkMate = True
                    temp.black.pieces.remove(piece)
        else:
            temp.black.pieces[index].pos = copy.deepcopy(pos)
            for piece in temp.white.pieces:
                if piece.pos[0] == pos[0] and piece.pos[1] == pos[1]:
                    if piece.type == 'King':
                        self.black.checkMate = True
                    temp.white.pieces.remove(piece)
        return temp

    def checkPerpendicular(self, t_list, team, ind):
        piece = t_list[ind]
        moves = []
        pos = copy.deepcopy(piece.pos)
        while pos[0] > 'A':
            pos[0] = chr(ord(pos[0]) - 1)
            k_piece = ['00']
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
                break
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        pos = copy.deepcopy(piece.pos)
        while pos[0] < 'H':
            pos[0] = chr(ord(pos[0]) + 1)
            k_piece = ['00']
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        pos = copy.deepcopy(piece.pos)
        while pos[1] > '1':
            k_piece = ['00']
            pos[1] = chr(ord(pos[1]) - 1)
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        pos = copy.deepcopy(piece.pos)
        while pos[1] < '8':
            pos[1] = chr(ord(pos[1]) + 1)
            k_piece = ['00']
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        return moves

    def checkDiagonal(self, t_list, team, ind):
        piece = t_list[ind]
        moves = []
        pos = copy.deepcopy(piece.pos)
        while pos[0] > 'A' and pos[1] > '1':
            pos[0] = chr(ord(pos[0]) - 1)
            pos[1] = chr(ord(pos[1]) - 1)
            k_piece = ['00']
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        pos = copy.deepcopy(piece.pos)
        while pos[0] < 'H' and pos[1] < '8':
            pos[0] = chr(ord(pos[0]) + 1)
            pos[1] = chr(ord(pos[1]) + 1)
            k_piece = ['00']
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        pos = copy.deepcopy(piece.pos)
        while pos[0] > 'A' and pos[1] < '8':
            pos[0] = chr(ord(pos[0]) - 1)
            pos[1] = chr(ord(pos[1]) + 1)
            k_piece = ['00']
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        pos = copy.deepcopy(piece.pos)
        while pos[0] < 'H' and pos[1] > '1':
            pos[0] = chr(ord(pos[0]) + 1)
            pos[1] = chr(ord(pos[1]) - 1)
            k_piece = ['00']
            if self.isEmpty(pos):
                moves.append(Move(piece, copy.deepcopy(pos), False, None))
            elif self.killMove(pos, team, k_piece):
                moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                break
            else:
                break
        return moves

    def getPossibleMoves(self, t_list, team, ind):
        piece = t_list[ind]
        moves = []
        if piece.type == 'Rook':
            # print("Rook")
            return self.checkPerpendicular(t_list, team, ind)
        elif piece.type == 'Pawn':
            if team == 'White':
                pos = copy.deepcopy(piece.pos)
                pos[1] = chr(ord(pos[1]) + 1)
                if pos[1] < '9' and self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))

                if pos[1] == '3' and self.isEmpty([pos[0], '4']):
                    moves.append(Move(piece, copy.deepcopy([pos[0], '4']), False, None))
                pos[0] = chr(ord(pos[0]) - 1)
                k_piece = ['00']
                if self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                pos[0] = chr(ord(pos[0]) + 2)
                if self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            else:
                pos = copy.deepcopy(piece.pos)
                pos[1] = chr(ord(pos[1]) - 1)
                k_piece = ['00']
                if pos[1] > '0' and self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                if pos[1] == '6' and self.isEmpty([pos[0], '5']):
                    moves.append(Move(piece, copy.deepcopy([pos[0], '5']), False, None))
                pos[0] = chr(ord(pos[0]) - 1)
                if self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
                pos[0] = chr(ord(pos[0]) + 2)
                if self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            # print("Pawn")
            return moves
        elif piece.type == 'Knight':
            pos = copy.deepcopy(piece.pos)
            # chr(ord(ch) + 3)
            pos[0] = chr(ord(pos[0]) + 1)
            pos[1] = chr(ord(pos[1]) + 2)
            if pos[0] <= 'H' and pos[1] < '9':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) + 1)
            pos[1] = chr(ord(pos[1]) - 2)
            if pos[0] <= 'H' and pos[1] >= '1':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) - 1)
            pos[1] = chr(ord(pos[1]) - 2)
            if pos[0] >= 'A' and pos[1] >= '1':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) - 1)
            pos[1] = chr(ord(pos[1]) + 2)
            if pos[0] >= 'A' and pos[1] < '9':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) + 2)
            pos[1] = chr(ord(pos[1]) + 1)
            if pos[0] <= 'H' and pos[1] < '9':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) + 2)
            pos[1] = chr(ord(pos[1]) - 1)
            if pos[0] <= 'H' and pos[1] >= '1':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) - 2)
            pos[1] = chr(ord(pos[1]) - 1)
            if pos[0] >= 'A' and pos[1] >= '1':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) - 2)
            pos[1] = chr(ord(pos[1]) + 1)
            if pos[0] >= 'A' and pos[1] < '9':
                k_piece = ['00']
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            # print("Knight")
            return moves
        elif piece.type == 'Bishop':
            # print("Bishop")
            return self.checkDiagonal(t_list, team, ind)
        elif piece.type == 'Queen':
            # print("Queen")
            return self.checkPerpendicular(t_list, team, ind) + self.checkDiagonal(t_list, team, ind)
        else:
            k_piece = ['00']
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) + 1)
            pos[1] = chr(ord(pos[1]) + 1)
            if pos[0] <= 'H' and pos[1] <= '8':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) + 1)
            pos[1] = chr(ord(pos[1]) - 1)
            if pos[0] <= 'H' and pos[1] >= '1':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) - 1)
            pos[1] = chr(ord(pos[1]) + 1)
            if pos[0] >= 'A' and pos[1] <= '8':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) - 1)
            pos[1] = chr(ord(pos[1]) - 1)
            if pos[0] >= 'A' and pos[1] >= '1':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) + 1)
            if pos[0] <= 'H':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[0] = chr(ord(pos[0]) - 1)
            if pos[0] >= 'A':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[1] += chr(ord(pos[1]) + 1)
            if pos[0] <= '8':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            pos = copy.deepcopy(piece.pos)
            pos[1] = chr(ord(pos[1]) - 1)
            if pos[1] >= '1':
                if self.isEmpty(pos):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None))
                elif self.killMove(pos, team, k_piece):
                    moves.append(Move(piece, copy.deepcopy(pos), True, k_piece))
            # print("King")
            if team == 'White':
                if self.white.checkCastle(0):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None, True))
                elif self.white.checkCastle(1):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None, False, True))
            else:
                if self.black.checkCastle(0):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None, True))
                elif self.black.checkCastle(1):
                    moves.append(Move(piece, copy.deepcopy(pos), False, None, False, True))

            return moves

    def doMove(self, color, cur, pos):
        if color == 'White':
            if cur == 'QCastle':
                self.set(self.Castle('White', 0))
                return
            elif cur == 'KCastle':
                self.set(self.Castle('White', 1))
                return
            for i in range(0, len(self.white.pieces)):
                if self.white.pieces[i].pos[0] == cur[0] and self.white.pieces[i].pos[1] == cur[1]:
                    self.white.pieces[i].pos = copy.deepcopy([pos[0], pos[1]])
                    for j in range(0, len(self.black.pieces)):
                        if self.black.pieces[j].pos[0] == pos[0] and self.black.pieces[j].pos[1] == pos[1]:
                            if self.black.pieces[j].type == 'King':
                                self.white.checkMate = True
                            self.black.pieces.pop(j)
                            break
                    self.move = 'Black'
                    return
        else:
            if cur == 'QCastle':
                self.set(self.Castle('Black', 0))
                return
            elif cur == 'KCastle':
                self.set(self.Castle('Black', 1))
                return
            for i in range(0, len(self.black.pieces)):
                if self.black.pieces[i].pos[0] == cur[0] and self.black.pieces[i].pos[1] == cur[1]:
                    self.black.pieces[i].pos = copy.deepcopy([pos[0], pos[1]])
                    for j in range(0, len(self.white.pieces)):
                        if self.white.pieces[j].pos[0] == pos[0] and self.white.pieces[j].pos[1] == pos[1]:
                            if self.white.pieces[j].type == 'King':
                                self.black.checkMate = True
                            self.white.pieces.pop(j)
                            break
                    self.move = 'White'
                    return

    def Castle(self, color, side):
        temp = copy.deepcopy(self)
        if side == 0:
            if color == 'White':
                for i in range(0, len(temp.white.pieces)):
                    if temp.white.pieces[i].type == 'King':
                        temp.white.pieces[i].pos[0] = 'C'
                    elif temp.white.pieces[i].type == 'Rook' and temp.white.pieces[i].pos[0] == 'A':
                        temp.white.pieces[i].pos[0] = 'D'
            else:
                for i in range(0, len(temp.black.pieces)):
                    if temp.black.pieces[i].type == 'King':
                        temp.black.pieces[i].pos[0] = 'C'
                    elif temp.black.pieces[i].type == 'Rook' and temp.black.pieces[i].pos[0] == 'A':
                        temp.black.pieces[i].pos[0] = 'D'
        else:
            if color == 'White':
                for i in range(0, len(temp.white.pieces)):
                    if temp.white.pieces[i].type == 'King':
                        temp.white.pieces[i].pos[0] = 'G'
                    elif temp.white.pieces[i].type == 'Rook' and temp.white.pieces[i].pos[0] == 'H':
                        temp.white.pieces[i].pos[0] = 'F'
            else:
                for i in range(0, len(temp.black.pieces)):
                    if temp.black.pieces[i].type == 'King':
                        temp.black.pieces[i].pos[0] = 'G'
                    elif temp.black.pieces[i].type == 'Rook' and temp.black.pieces[i].pos[0] == 'H':
                        temp.black.pieces[i].pos[0] = 'F'
        return temp

    def isEmpty(self, pos):
        for piece in self.black.pieces:
            if piece.pos[0] == pos[0] and piece.pos[1] == pos[1]:
                return False
        for piece in self.white.pieces:
            if piece.pos[0] == pos[0] and piece.pos[1] == pos[1]:
                return False
        return True

    def killMove(self, pos, team, k_piece):
        if team == 'Black':
            for piece in self.white.pieces:
                if piece.pos[0] == pos[0] and piece.pos[1] == pos[1]:
                    k_piece[0] = piece
                    return True
        else:
            for piece in self.black.pieces:
                if piece.pos[0] == pos[0] and piece.pos[1] == pos[1]:
                    k_piece[0] = piece
                    return True
        return False


class ChessTree:
    def __init__(self, root, height, name, move):
        self.root = root
        self.root.move = move
        self.children = []
        self.value = 0
        self.Name = name
        if self.root.move == 'White':
            for i in range(0, len(root.white.pieces)):
                self.value -= root.white.pieces[i].score
            for i in range(0, len(root.black.pieces)):
                self.value += root.black.pieces[i].score
        else:
            for i in range(0, len(root.white.pieces)):
                self.value += root.white.pieces[i].score
            for i in range(0, len(root.black.pieces)):
                self.value -= root.black.pieces[i].score
        if height > 0:
            self.generate_tree(height)

    def generate_tree(self, height):
        if self.root.move == 'White':
            for i in range(0, len(self.root.white.pieces)):
                moves = self.root.getPossibleMoves(self.root.white.pieces, 'White', i)
                for m in moves:
                    temp = ChessTree(self.root.performMove(self.root.white, i, m.pos), height - 1, 'White ' + m.show(),
                                     'Black')
                    # temp.root.move = 'Black'
                    self.children.append(temp)
        else:
            for i in range(0, len(self.root.black.pieces)):
                moves = self.root.getPossibleMoves(self.root.black.pieces, 'Black', i)
                for m in moves:
                    if m.qCastle:
                        temp = ChessTree(self.root.Castle('Black', 0), height - 1, 'Black ' + m.show(),
                                         'White')
                    elif m.kCastle:
                        temp = ChessTree(self.root.Castle('Black', 1), height - 1, 'Black ' + m.show(),
                                         'White')
                    else:
                        temp = ChessTree(self.root.performMove(self.root.black, i, m.pos), height - 1,
                                         'Black ' + m.show(), 'White')
                    # temp.root.move = 'White'
                    self.children.append(temp)


class AlphaBeta:
    # print utility value of root node (assuming it is max)
    # print names of all nodes visited during search
    def __init__(self, game_tree):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        return

    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = infinity * -1.0
        beta = infinity

        successors = self.getSuccessors(node)
        best_state = None
        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        print("AlphaBeta:  Move Value of Root Board: = " + str(best_val))
        print("AlphaBeta:  Best move is: " + best_state.Name)
        return best_state

    def max_value(self, node, alpha, beta):
        print("Min -> Move :: " + node.Name)
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity * -1.0

        successors = self.getSuccessors(node)
        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def min_value(self, node, alpha, beta):
        print("Max -> Move :: " + node.Name)
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity

        successors = self.getSuccessors(node)
        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)

        return value

    #                     #
    #   UTILITY METHODS   #
    #                     #
    def getUtility(self, node):
        assert node is not None
        if node.root.move == 'White' and node.root.white.checkMate:
            return node.value + 10000
        elif node.root.move == 'Black' and node.root.black.checkMate:
            return node.value + 10000
        else:
            return node.value

    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0

    def getSuccessors(self, node):
        assert node is not None
        return node.children


def main():
    chessboard = ChessBoard()
    # chessboard.doRandomMoves(24)
    while not chessboard.black.checkMate and not chessboard.white.checkMate:
        tree = ChessTree(chessboard, 3, "Default", chessboard.move)
        AlphaBeta(tree).alpha_beta_search(tree)
        x = input("Enter color: ")
        y = input("Enter piece position: ")
        z = input("Enter new position: ")
        chessboard.doMove(x, y, (z[0], z[1]))
        x = input("Enter color: ")
        y = input("Enter piece position: ")
        z = input("Enter new position: ")
        chessboard.doMove(x, y, (z[0], z[1]))
    # for p in chessboard.black.pieces:
    #     print(p.type + "  " + p.pos[0] + p.pos[1])
    # print("\n\n")
    # for p in chessboard.white.pieces:
    #     print(p.type + "  " + p.pos[0] + p.pos[1])


if __name__ == '__main__':
    main()
