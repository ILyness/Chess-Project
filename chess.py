from graphics import *
import time
import random

### Each instance of this class is a square on the board, which keeps track of where it is,
### whether its' empty or not, and which piece is in it. The draw method draws it on the board,
### the place and remove method place and remove pieces from the square respectively, and the 
### highlight and unhighlight draw a circle and undraw it to show the sqaure as a possible move
### for a piece. The str method is for testing purposes.
class Square:

    def __init__(self, pt, col, board):
        self.board = board
        self.col = col
        self.location = Rectangle(pt, Point(pt.getX() + 60,pt.getY() + 60))
        self.center = self.location.getCenter()
        self.empty = True
        self.piece = []
        self.circle = Circle(self.center, 8)
        self.circle.setFill("grey")

    def draw(self):
        self.location.setFill(self.col)
        self.location.draw(self.board)

    def place(self, piece):
        if self.empty == True:
            self.piece.append(piece)
            self.empty = False
        else:
            self.piece[0].capture()
            self.piece.pop()
            self.piece.append(piece)

    def remove(self):
        self.piece.pop()
        self.empty = True

    def highlight(self):
        self.circle.draw(self.board)

    def unhighlight(self):
        self.circle.undraw()

    def __str__(self):
        # if self.empty == False:
        #     return f"{(self.center.getY() // 60) + 1}, {(self.center.getX() // 60) + 1}, {self.piece[0]}"
        # else:
        #     return f"{(self.center.getY() // 60) + 1}, {(self.center.getX() // 60) + 1}, empty"
        return f"{(self.center.getY() // 60) + 1}, {(self.center.getX() // 60) + 1}, {self.empty}"
        
### The board class isn't strictly necessary, but it keeps track of all the pieces and squares,
### and creates the window and all the squares for the board when initialized.
class Board:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.win = GraphWin("Chess Board",480,480)
        self.squares = []
        self.pieces = []
        x = 0
        y = 0
        alt = 0
        for t in range(8):
            rank = []
            for k in range(8):
                if alt % 2 == 0:
                    square = Square(Point(x,y), "white", self.win)
                    square.draw()
                    rank.append(square)
                if alt % 2 == 1:
                    square = Square(Point(x,y), "green", self.win)
                    square.draw()
                    rank.append(square)
                x += 60
                alt += 1
            self.squares.append(rank)
            alt += 1
            x = 0
            y += 60

    def __str__(self):
        string = ""
        for i in range(8):
            for j in range(8):

                string = string + str(self.squares[i][j]) +  " | "
            string = string + "\n"
        return string
            
            

### The piece class does the lion's share of the work for the game. It gets assigned a color and type and
### knows which player and board it belongs to. The place method creates the image of the piece and assigns 
### it to a square on the board. The checkVision, checkpawnVision, checkkingVision, checkRank, checkFile,
### checkDiagonals, and checkHops method work together to generate all the squares a piece can move to based
### on its type. The checkfalseVision and fixVision methods then find illegal moves that didn't consider
### checks, pins, etc and removes them. The select and unselect method highlight and unhighlight the
### available squares for the piece to move to, and the move method moves the image of the piece and 
### updates the location of the piece for itself and the involved squares. All piece images are from
### Wikimedia Commons. 
### They can be found here: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
class Piece:

    def __init__(self, board, type, player):
        self.player = player
        self.type = type
        self.board = board
        self.color = player.color
        board.pieces.append(self)
        player.pieces.append(self)
        self.vision = []
        #self.falseVision = []
        self.moved = False
        if type == "king":
            self.player.king = self
            self.points = 1000
        elif type == "queen":
            self.points = 9
        elif type == "rook":
            self.points = 5
        elif type == "knight" or type == "bishop":
            self.points = 3
        elif type == "pawn":
            self.points = 1


    def place(self, square):
        self.square = square
        self.square.place(self)
        if self.type == "queen":
            if self.color == "white":
                self.img = Image(self.square.center, "whitequeen.png")
            else:
                self.img = Image(self.square.center, "blackqueen.png")
        if self.type == "king":
            if self.color == "white":
                self.img = Image(self.square.center, "whiteking.png")
            else:
                self.img = Image(self.square.center, "blackking.png")
        if self.type == "rook":
            if self.color == "white":
                self.img = Image(self.square.center, "whiterook.png")
            else:
                self.img = Image(self.square.center, "blackrook.png")
        if self.type == "knight":
            if self.color == "white":
                self.img = Image(self.square.center, "whiteknight.png")
            else:
                self.img = Image(self.square.center, "blackknight.png")
        if self.type == "bishop":
            if self.color == "white":
                self.img = Image(self.square.center, "whitebishop.png")
            else:
                self.img = Image(self.square.center, "blackbishop.png")
        if self.type == "pawn":
            if self.color == "white":
                self.img = Image(self.square.center, "whitepawn.png")
            else:
                self.img = Image(self.square.center, "blackpawn.png")
        self.img.draw(self.board.win)
        #self.vision = [] 

    def move(self, square):
        self.square.remove()
        self.img.move(square.center.getX() - self.square.center.getX(), square.center.getY() - self.square.center.getY())
        square.place(self)
        self.square = square
        if self.type == "pawn":
            r = int((self.square.center.getY() - 30) // 60)
            if self.player.side == 0:
                if r == 0:
                    self.type = "queen"
                    self.points = 9
                    self.img.undraw()
                    self.img = Image(self.square.center, "whitequeen.png")
                    self.img.draw(self.board.win)
                    #self.place(self.square)
                    #self.board.pieces.append(self)
            else:
                if r == 7:
                    self.type = "queen"
                    self.points = 9
                    self.img.undraw()
                    self.img = Image(self.square.center, "blackqueen.png")
                    self.img.draw(self.board.win)
                    #self.place(self.square)
                    #self.board.pieces.append(self)
        if self.type == "king" and self.moved == False:
            if self.square == self.board.squares[7][2]:
                self.board.squares[7][0].piece[0].move(self.board.squares[7][3])
            if self.square == self.board.squares[7][6]:
                self.board.squares[7][7].piece[0].move(self.board.squares[7][5])
            if self.square == self.board.squares[0][2]:
                self.board.squares[0][0].piece[0].move(self.board.squares[0][3])
            if self.square == self.board.squares[0][6]:
                self.board.squares[0][7].piece[0].move(self.board.squares[0][5])
        if self.moved == False:
            self.moved = True


    def checkMove(self, square):
        s = self.square
        self.square.piece.remove(self)
        if self.square.piece == []:
            self.square.empty = True
        self.square = square
        square.piece.insert(0, self)
        square.empty = False
        i = 0
        #while square not in self.falseVision and i < len(self.board.pieces):
        while square in self.vision and i < len(self.board.pieces):
            p = self.board.pieces[i]
            if p.color != self.color and p.square != self.square:
                v = p.vision.copy()
                p.checkVision()
                if self.player.king.square in p.vision:
                    #self.falseVision.append(square)
                    self.vision.remove(square)
                p.vision = v
            i += 1
        if self.type == "king" and self.moved == False and square in self.vision:
        #if self.type == "king" and self.moved == False and self.player.check == True:
            # if square == self.board.squares[7][2] or square == self.board.squares[7][6] or square == self.board.squares[0][2] or square == self.board.squares[0][6]:
            #     #self.falseVision.append(square)
            #     self.vision.remove(square)
        #if self.type == "king" and self.moved == False:
            if square == self.board.squares[7][2]:
                if self.player.check == True or self.board.squares[7][3] not in self.vision:
                    self.vision.remove(square)
            elif square == self.board.squares[7][6]:
                if self.player.check == True or self.board.squares[7][5] not in self.vision:
                    self.vision.remove(square)
            elif square == self.board.squares[0][2]:
                if self.player.check == True or self.board.squares[0][3] not in self.vision:
                    self.vision.remove(square)
            elif square == self.board.squares[0][6]:
                if self.player.check == True or self.board.squares[0][5] not in self.vision:
                    self.vision.remove(square)  
        self.square = s
        self.square.piece.insert(0, self)
        self.square.empty = False
        #self.square.place(self)
        square.piece.remove(self)
        if square.piece == []:
            square.empty = True
        # for p in self.board.pieces:
        #     p.checkVision()
       

    def checkRank(self, r, f):
        # r = int((self.square.center.getY() - 30) // 60)
        # f = self.board.squares[r].index(self.square)
        k = f - 1
        while  k >= 0  and self.board.squares[r][k].empty == True:
            self.vision.append(self.board.squares[r][k])
            k += -1
        if k >= 0 and self.color != self.board.squares[r][k].piece[0].color:
            self.vision.append(self.board.squares[r][k])
        q = f + 1
        while q <= 7 and self.board.squares[r][q].empty == True:
            self.vision.append(self.board.squares[r][q])
            q += 1
        if q <= 7 and self.color != self.board.squares[r][q].piece[0].color:
            self.vision.append(self.board.squares[r][q])

    def checkFile(self, r, f):
        # r = int((self.square.center.getY() - 30) // 60)
        # f = self.board.squares[r].index(self.square)
        k = r - 1
        while  k >= 0 and self.board.squares[k][f].empty == True:
            self.vision.append(self.board.squares[k][f])
            k += -1
        if k >= 0 and self.color != self.board.squares[k][f].piece[0].color:
            self.vision.append(self.board.squares[k][f])
        q = r + 1
        while  q <= 7 and self.board.squares[q][f].empty == True:
            self.vision.append(self.board.squares[q][f])
            q += 1
        if q  <= 7 and self.color != self.board.squares[q][f].piece[0].color:
            self.vision.append(self.board.squares[q][f])

    def checkDiagonals(self, r, f):
        # r = int((self.square.center.getY() - 30) // 60)
        # f = self.board.squares[r].index(self.square)
        a = 0
        b = 0
        for _ in range(2):
            for _ in range(2):
                if a % 2 == 0:
                    dk = -1
                else:
                    dk = 1
                if b % 2 == 0:
                    dq = -1
                else:
                    dq = 1
                k = r + dk
                q = f + dq
                while k >= 0 and q >= 0 and k<= 7 and q <= 7 and self.board.squares[k][q].empty == True:
                    self.vision.append(self.board.squares[k][q])
                    k += dk
                    q += dq
                if k >= 0 and q >= 0 and k <= 7 and q <= 7 and self.color != self.board.squares[k][q].piece[0].color:
                    self.vision.append(self.board.squares[k][q])
                a += 1
            b += 1

    def checkHops(self, r, f):
        # r = int((self.square.center.getY() - 30) // 60)
        # f = self.board.squares[r].index(self.square)
        a = 0
        b = 0
        for _ in range(2):
            for _ in range(2):
                if a % 2 == 0:
                    dk = -2
                else:
                    dk = 2
                if b % 2 == 0:
                    dq = -1
                else:
                    dq = 1
                k = r + dk
                q = f + dq
                if k >= 0 and q >= 0 and k <= 7 and q <= 7 and (self.board.squares[k][q].empty == True or self.color != self.board.squares[k][q].piece[0].color):
                    self.vision.append(self.board.squares[k][q])
                a += 1
            b += 1
        for _ in range(2):
            for _ in range(2):
                if a % 2 == 0:
                    dk = -1
                else:
                    dk = 1
                if b % 2 == 0:
                    dq = -2
                else:
                    dq = 2
                k = r + dk
                q = f + dq
                if k >= 0 and q >= 0 and k <= 7 and q <= 7 and (self.board.squares[k][q].empty == True or self.color != self.board.squares[k][q].piece[0].color):
                    self.vision.append(self.board.squares[k][q])
                a += 1
            b += 1

    def checkvisionKing(self, r, f):
        r = int((self.square.center.getY() - 30) // 60)
        f = self.board.squares[r].index(self.square)
        a = 0
        b = 0
        for _ in range(2):
            for _ in range(2):
                if a % 2 == 0:
                    dk = -1
                else:
                    dk = 1
                if b % 2 == 0:
                    dq = -1
                else:
                    dq = 1
                k = r + dk
                q = f + dq
                if k >= 0 and q >= 0 and k <= 7 and q <= 7 and (self.board.squares[k][q].empty == True or self.color != self.board.squares[k][q].piece[0].color):
                    self.vision.append(self.board.squares[k][q])
                a += 1
            b += 1
        k = r + 1
        q = f
        if k >= 0 and q >= 0 and k <= 7 and q <= 7 and (self.board.squares[k][q].empty == True or self.color != self.board.squares[k][q].piece[0].color):
                    self.vision.append(self.board.squares[k][q])
        k = r - 1
        if k >= 0 and q >= 0 and k <= 7 and q <= 7 and (self.board.squares[k][q].empty == True or self.color != self.board.squares[k][q].piece[0].color):
                    self.vision.append(self.board.squares[k][q])
        k = r
        q = f + 1
        if k >= 0 and q >= 0 and k <= 7 and q <= 7 and (self.board.squares[k][q].empty == True or self.color != self.board.squares[k][q].piece[0].color):
                    self.vision.append(self.board.squares[k][q])
        q = f - 1
        if k >= 0 and q >= 0 and k <= 7 and q <= 7 and (self.board.squares[k][q].empty == True or self.color != self.board.squares[k][q].piece[0].color):
                    self.vision.append(self.board.squares[k][q])
        if self.moved == False:
            if self.player.side == 0:
                sq = self.board.squares[7][0]
                if sq.empty == False and sq.piece[0].moved == False and self.board.squares[7][3] in sq.piece[0].vision:
                    self.vision.append(self.board.squares[7][2])
                sq = self.board.squares[7][7]
                if sq.empty == False and sq.piece[0].moved == False and self.board.squares[7][5] in sq.piece[0].vision:
                    self.vision.append(self.board.squares[7][6])
            else:
                sq = self.board.squares[0][0]
                if sq.empty == False and sq.piece[0].moved == False and self.board.squares[0][3] in sq.piece[0].vision:
                    self.vision.append(self.board.squares[0][2])
                sq = self.board.squares[0][7]
                if sq.empty == False and sq.piece[0].moved == False and self.board.squares[0][5] in sq.piece[0].vision:
                    self.vision.append(self.board.squares[0][6])
                     

    def checkvisionPawn(self, r, f):
        # r = int((self.square.center.getY() - 30) // 60) 
        # f = self.board.squares[r].index(self.square)
        if self.player.side == 0:
            p = r - 1
            if r == 6:
                while p >= r - 2 and self.board.squares[p][f].empty == True:
                    self.vision.append(self.board.squares[p][f])
                    p += -1
            else:
                if self.board.squares[p][f].empty == True:
                    self.vision.append(self.board.squares[p][f]) 
            p = r - 1
        else: 
            p = r + 1
            if r == 1:
                while p <= r + 2 and self.board.squares[p][f].empty == True:
                    self.vision.append(self.board.squares[p][f])
                    p += 1
            else:
                if self.board.squares[p][f].empty == True:
                    self.vision.append(self.board.squares[p][f])
            p = r + 1
        a = 0
        for _ in range(2):
            if a % 2 == 0:
                q = f + 1
            else:
                q = f - 1
            if 0 <= q and q <= 7 and self.board.squares[p][q].empty == False and self.board.squares[p][q].piece[0].color != self.color:
                self.vision.append(self.board.squares[p][q])
            a += 1
       

    def checkVision(self):
        self.vision.clear()
        r = int((self.square.center.getY() - 30) // 60) 
        f = self.board.squares[r].index(self.square)
        if self.type == "queen":
            self.checkRank(r, f)
            self.checkFile(r, f)
            self.checkDiagonals(r, f)
        if self.type == "rook":
            self.checkRank(r, f)
            self.checkFile(r ,f)
        if self.type == "bishop":
            self.checkDiagonals(r, f)
        if self.type == "knight":
            self.checkHops(r, f)
        if self.type == "king":
            self.checkvisionKing(r, f)
        if self.type == "pawn":
            self.checkvisionPawn(r, f)

    def checkfalseVision(self):
        vision = self.vision.copy()
        for sq in vision:
            self.checkMove(sq)


    def select(self):
        for sq in self.vision:
            sq.highlight()
    

    def unselect(self):
        for sq in self.vision:
            sq.unhighlight()

    def capture(self):
        self.img.undraw()
        self.vision.clear()
        self.board.pieces.remove(self)
        self.player.pieces.remove(self)

    def fixVision(self):
        for s in self.falseVision:
            self.vision.remove(s)
        self.falseVision.clear()

    ####Experiment, untested
    def filterVision(self):
        if self.type == "pawn":
            for s in self.vision:
                r = random.randint(0,1)
                if s.empty == True and r == 0:
                    self.vision.remove(s)
        elif self.type == "king":
            for s in self.vision:
                r == random.randint(0,2)
                if abs(s.square.center.getY() // 60 - self.square.getY() // 60) < 2 and r != 0:
                    self.vision.remove(s)
        else:
            for s in self.vision:
                d = 0
                a = 0
                for p in self.player.pieces:
                    if s in p.vision:
                        d += 1
                    
    def __str__(self):
        return f"{self.color} {self.type}"

### The HumanPlayer simply gets a color and a list of pieces it has. The checkMaterial method is simply
### to count material points to help the AI make decisions. The takeTurn method selects a given piece when
### its square is clicked, and then if a legal square is clicked it will move the piece. If not it will
### unselect it and wait for another move to be made. After the move is made, it updates the vision of all
### the pieces.
class HumanPlayer:

    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.check = False

    def checkMaterial(self):
        self.material = 0
        for p in self.pieces:
            if p.square.piece.index(p) == 0:
                self.material += p.points             

    def takeTurn(self):
        if self.game.gameOver == False:
            self.game.turn = self
            self.check = False
            choosePiece = True
            while choosePiece:
                selectPt = self.board.win.getMouse()
                r = int(selectPt.getY() // 60)
                f = int(selectPt.getX() // 60)
                if self.board.squares[r][f].empty == False and self.board.squares[r][f].piece[0] in self.pieces:
                    piece = self.board.squares[r][f].piece[0]
                    piece.select()
                    movePt = self.board.win.getMouse()
                    r = int(movePt.getY() // 60)
                    f = int(movePt.getX() // 60)
                    if self.board.squares[r][f] in piece.vision:
                        piece.unselect()
                        piece.move(self.board.squares[r][f])
                        choosePiece = False
                    else:
                        piece.unselect()
            for p in self.board.pieces:
                p.checkVision()
            for p in self.board.pieces:
                if p.type != "king":
                    if self.game.player1.king.square in p.vision:
                        self.game.player1.check = True
                    if self.game.player2.king.square in p.vision:
                        self.game.player2.check = True
            for p in self.board.pieces:
                p.checkfalseVision()
            # for p in self.board.pieces:
            #     p.fixVision()
            self.game.checkGameOver()

### The ComputerPlayer is still under construction. It has a similar setup as the HumanPlayer and 
### also has the checkMaterial method, but it has a different takeTurn method. The key is the tryMove
### method, which uses recursion to try all possible moves up to a certain depth, and evaluate the
### material for each side along the way. It then uses the calculateMove method to filter through
### this permutation list generated and use the material count to choose a best move. It's still a
### little buggy and quite slow, but it's getting there.        
class ComputerPlayer:

    def __init__(self, color):
        self.color = color
        self.pieces = []
        self.check = False
        self.moves = {}

    def checkMaterial(self):
        self.material = 0
        for p in self.pieces:
            if p.square.piece.index(p) == 0:
                self.material += p.points

    # def tryMove(self, depth, move_list, mat_list, piece, square):
    #     if depth < 2:
    #         if depth % 2 == 0:
    #             for p1 in self.pieces:
    #                 if p1.square.piece.index(p1) == 0:
    #                     v = p1.vision.copy()
    #                     for sq1 in v:
    #                         s1 = p1.square
    #                         p1.square.piece.remove(p1)
    #                         if p1.square.piece == []:
    #                             p1.square.empty = True
    #                         p1.square = sq1
    #                         sq1.piece.insert(0, p1)
    #                         sq1.empty = False
    #                         self.checkMaterial() 
    #                         self.game.player1.checkMaterial()
    #                         mat = self.material - self.game.player1.material
    #                         if piece == None:
    #                             move_list[(p1, sq1)] = [[mat]]
    #                         else:
    #                             if mat_list in move_list[(piece, square)]:
    #                                 move_list[(piece, square)].remove(mat_list)
    #                             ##########
    #                             add = True
    #                             for seq in move_list[(piece, square)]:
    #                                 # if seq == mat_list:
    #                                 #     move_list[(piece, square)].remove(mat_list)
    #                                 # else:
    #                                 if mat < seq[depth]:
    #                                     add = False
    #                                 elif mat > seq[depth]:
    #                                     move_list[(piece, square)].remove(seq)
    #                             if add == True:
    #                                 new_list = mat_list.copy()
    #                                 new_list.append(mat)
    #                                 move_list[(piece, square)].append(new_list)
    #                             ##########
    #                         ##########
    #                         if depth < 1:
    #                         ###
    #                             for pc in self.board.pieces:
    #                                 if pc.square.piece.index(pc) == 0:
    #                                     pc.checkVision()
    #                                 else:
    #                                     pc.vision = []
    #                             for pc in self.board.pieces:
    #                                 if pc.square.piece.index(pc) == 0:
    #                                     pc.checkfalseVision()
    #                         # for pc in self.board.pieces:
    #                         #     if pc.square.piece.index(pc) == 0:
    #                         #         pc.fixVision()
    #                             if piece == None:
    #                                 self.tryMove(depth + 1, move_list, [mat], p1, sq1)
    #                             ###
    #                             elif add == True:
    #                             ###
    #                                 self.tryMove(depth + 1, move_list, new_list, piece, square)
    #                         ##########                                                          
    #                         p1.square = s1
    #                         p1.square.piece.insert(0, p1)
    #                         p1.square.empty = False
    #                         sq1.piece.remove(p1)
    #                         if sq1.piece == []:
    #                             sq1.empty = True
    #                         for pc in self.board.pieces:
    #                             if pc.square.piece.index(pc) == 0:
    #                                 pc.checkVision()
    #                             else:
    #                                 pc.vision = []
    #                         for pc in self.board.pieces:
    #                             if pc.square.piece.index(pc) == 0:
    #                                 pc.checkfalseVision()
    #                         # for pc in self.board.pieces:
    #                         #     if pc.square.piece.index(pc) == 0:
    #                         #         pc.fixVision()
    #         else:
    #             for p in self.game.player1.pieces:
    #                 if p.square.piece.index(p) == 0:
    #                     w = p.vision.copy()
    #                     for sq in w:
    #                         s = p.square
    #                         p.square.piece.remove(p)
    #                         if p.square.piece == []:
    #                             p.square.empty = True
    #                         p.square = sq
    #                         sq.piece.insert(0, p)
    #                         sq.empty = False
    #                         self.checkMaterial() 
    #                         self.game.player1.checkMaterial()
    #                         mat = self.material - self.game.player1.material
    #                         if mat_list in move_list[(piece, square)]:
    #                             move_list[(piece, square)].remove(mat_list)
    #                         ##########
    #                         add = True
    #                         for seq in move_list[(piece, square)]:
    #                             # if seq == mat_list:
    #                             #     move_list[(piece, square)].remove(mat_list)
    #                             # else:
    #                             if mat > seq[depth]:
    #                                 add = False
    #                             elif mat < seq[depth]:
    #                                 move_list[(piece, square)].remove(seq)
    #                         if add == True:
    #                             new_list = mat_list.copy()
    #                             new_list.append(mat)
    #                             move_list[(piece, square)].append(new_list)
    #                         ##########
    #                         ##########
    #                         if depth < 1:
    #                         ###
    #                             for pc in self.board.pieces:
    #                                 if pc.square.piece.index(pc) == 0:
    #                                     pc.checkVision()
    #                                 else:
    #                                     pc.vision = []
    #                             for pc in self.board.pieces:
    #                                 if pc.square.piece.index(pc) == 0:
    #                                     pc.checkfalseVision()
    #                         # for pc in self.board.pieces:
    #                         #     if pc.square.piece.index(pc) == 0:
    #                         #         pc.fixVision()
    #                             if add == True:
    #                                 self.tryMove(depth + 1, move_list, new_list, piece, square)
    #                         ##########                                                         
    #                         p.square = s
    #                         p.square.piece.insert(0, p)
    #                         p.square.empty = False
    #                         sq.piece.remove(p)
    #                         if sq.piece == []:
    #                             sq.empty = True
    #                         for pc in self.board.pieces:
    #                             if pc.square.piece.index(pc) == 0:
    #                                 pc.checkVision()
    #                             else:
    #                                 pc.vision = []
    #                         for pc in self.board.pieces:
    #                             if pc.square.piece.index(pc) == 0:
    #                                 pc.checkfalseVision()
    #                         # for pc in self.board.pieces:
    #                         #     if pc.square.piece.index(pc) == 0:
    #                         #         pc.fixVision()                   
    #     return move_list
    
    def calculateMaterial(self, maxDepth, currentDepth, piece, square):
        # print("Before", piece, square)
        # print(self.board)
        # print(piece, "moving from", piece.square, "to", square)
        time.sleep(.05)
        if piece.square.piece.index(piece) == 0:
            originalSquare = piece.square
            originalSquare.piece.remove(piece)
            # if originalSquare.piece == []:
            originalSquare.empty = True
            piece.square = square
            square.piece.insert(0, piece)
            square.empty = False
            piece.img.move(square.center.getX() - originalSquare.center.getX(), square.center.getY() - originalSquare.center.getY())

            promoted = False
            if piece.type == "pawn":
                r = int((piece.square.center.getY() - 30) // 60)
                if r == 0 or r == 7:
                    promoted = True
                    piece.type = "queen"
                    piece.points = 9

            self.checkMaterial()
            self.game.player1.checkMaterial()
            # print(self.material)
            # print(self.game.player1.material)
            materialAdvantage = self.material - self.game.player1.material
            # self.game.wintext.setText("Material Advantage:" + str(materialAdvantage))
            # self.game.wintext.draw(self.board.win)
            # print("Piece:",piece,"Current square:",square, "MaterialAdvantage:", materialAdvantage)
            # print("After", piece, square)
            # print(self.board)
            # print("original square:", originalSquare, "current square:", square, "piece is on", piece.square)
            # print()
            time.sleep(.05)
            # self.game.wintext.undraw()
            if currentDepth == maxDepth or (materialAdvantage <= -900 or materialAdvantage >= 900):
                square.piece.remove(piece)
                if square.piece == []:
                    square.empty = True
                piece.img.move(originalSquare.center.getX() - piece.square.center.getX(), originalSquare.center.getY() - piece.square.center.getY())
                piece.square = originalSquare
                originalSquare.piece.insert(0, piece)
                originalSquare.empty = False

                if promoted == True:
                    piece.type = "pawn"
                    piece.points = 1

                return [materialAdvantage, (piece, square)]
                #return materialAdvantage
            else:
                for pc in self.board.pieces:
                    if pc.square.piece.index(pc) == 0:
                        pc.checkVision()
                    else:
                        pc.vision = []
                if currentDepth % 2 == 0:
                    materialAdvantage = [-1000]
                    for nextPiece in self.pieces:
                        rootVision = nextPiece.vision.copy()
                        for nextSquare in rootVision:
                            currentMaterial = self.calculateMaterial(maxDepth, currentDepth + 1, nextPiece, nextSquare)
                            if currentMaterial != None and currentMaterial[0] > materialAdvantage[0]:
                                materialAdvantage = currentMaterial
                    square.piece.remove(piece)
                    if square.piece == []:
                        square.empty = True
                    piece.img.move(originalSquare.center.getX() - piece.square.center.getX(), originalSquare.center.getY() - piece.square.center.getY())
                    piece.square = originalSquare
                    originalSquare.piece.insert(0, piece)
                    originalSquare.empty = False

                    if promoted == True:
                        piece.type = "pawn"
                        piece.points = 1

                    materialAdvantage.append((piece, square))
                    return materialAdvantage
                else:
                    materialAdvantage = [1000]
                    for nextPiece in self.board.player1.pieces:
                        rootVision = nextPiece.vision.copy()
                        for nextSquare in rootVision:
                            currentMaterial = self.calculateMaterial(maxDepth, currentDepth + 1, nextPiece, nextSquare)
                            if currentMaterial != None and currentMaterial[0] < materialAdvantage[0]:
                                materialAdvantage = currentMaterial
                    # self.game.wintext.setText("Final Advantage:" + str(materialAdvantage[0]))
                    # self.game.wintext.draw(self.board.win)
                    # time.sleep(0.5)
                    # self.game.wintext.undraw()
                    square.piece.remove(piece)
                    if square.piece == []:
                        square.empty = True
                    piece.img.move(originalSquare.center.getX() - piece.square.center.getX(), originalSquare.center.getY() - piece.square.center.getY())
                    piece.square = originalSquare
                    originalSquare.piece.insert(0, piece)
                    originalSquare.empty = False

                    if promoted == True:
                        piece.type = "pawn"
                        piece.points = 1

                    materialAdvantage.append((piece, square))
                    return materialAdvantage

        else:
            return None


    
    def calculateMove(self):
        self.moves.clear()
        t0 = time.time()
        # self.moves = self.tryMove(0, self.moves, None, None, None)
        for piece in self.pieces:
            piece.checkVision()
            piece.checkfalseVision()
            rootVision = piece.vision.copy()
            for square in rootVision:
                material = self.calculateMaterial(4, 1, piece, square)
                # print("Piece:",piece,"Square:",square,"Material:",material)
                self.moves[(piece,square)] = material
        t1 = time.time()
        print(f"tryMove runtime (full): {t1-t0}")
        print(f"Dictionary Length: {len(self.moves)}")
        # print(self.moves)
        # for key in self.moves.keys():
        #     print(f"{key[0]}, {key[1]}: {self.moves[key]}")
        bestMoves = []
        bestmoveMat = -1000
        for k in self.moves.keys():
            best_mat = self.moves[k][0]
            # for seq in self.moves[k]:
            #     if seq[1] < best_mat:
            #         best_mat = seq[1]
            # self.moves[k] = best_mat
            ##########
            # for seq in self.moves[k]:
            #     if seq[1] > best_mat:
            #         c = self.moves[k].count(seq)
            #         for _ in range(c):
            #             self.moves[k].remove(seq)
            # best_mat2 = self.moves[k][0][2]
            # for seq in self.moves[k]:
            #     if seq[2] > best_mat2:
            #         best_mat2 = seq[2]
            # self.moves[k] = best_mat2
            ##########
            if best_mat > bestmoveMat:
                bestmoveMat = best_mat
        for k in self.moves.keys():
            if self.moves[k][0] == bestmoveMat:
                bestMoves.append(k)
        l = len(bestMoves)
        # t2 = time.time()
        # print(f"calculateMove runtime: {t2-t1}")
        if l > 1:
            i = random.randint(0, l-1)
            print(self.moves[bestMoves[i]])
            return bestMoves[i]
        else:
            print(self.moves[bestMoves[0]])
            return bestMoves[0]



            

    def takeTurn(self):
        # for piece in self.pieces:
            # print("Piece:", piece)
            # print("Squares:")
            # for square in piece.vision:
            #     print(square)
        if self.game.gameOver == False:
            self.game.turn = self
            self.check = False
            move = self.calculateMove()
            print("Best Move Sequence:")
            for i in range(3):
                print(self.moves[move][3-i][0], self.moves[move][3-i][1])
            print("Resulting Material:", self.moves[move][0])
            move[0].move(move[1])
            for p in self.board.pieces:
                p.checkVision()
            for p in self.board.pieces:
                if p.type != "king":
                    if self.game.player1.king.square in p.vision:
                        self.game.player1.check = True
                    if self.game.player2.king.square in p.vision:
                        self.game.player2.check = True
            for p in self.board.pieces:
                p.checkfalseVision()
            # for p in self.board.pieces:
            #     p.fixVision()
            self.game.checkGameOver()


### The Game Class keeps track of the players. The start method generates a board and places all 32
### pieces on it, and then starts the game loop where each player takes turns. The checkgameOver method
### identifies the end of a game by looking to see if a player has any legal moves and if they are in
### check or not, resulting in checkmate or stalemate respectively. This gameEnd method generates a
### quick message and then closes the board.
class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.gameOver = False
        player1.game = self
        player2.game = self
        self.wintext = Text(Point(240,240), "")
        self.wintext.setSize(30)
        self.wintext.setTextColor("red")

    def start(self):
        self.player1.side = 0
        self.player2.side = 1
        self.board = Board(self.player1, self.player2)
        for i in range(8):
            pawn = Piece(self.board, "pawn", self.player1)
            pawn.place(self.board.squares[6][i])
        for i in range(8):
            pawn = Piece(self.board, "pawn", self.player2)
            pawn.place(self.board.squares[1][i])
        a = 0
        b = 0    
        for _ in range(2):
            for _ in range(2):
                if a % 2 == 0:
                    r = 0
                    player = self.player2
                else:
                    r = 7
                    player = self.player1
                if b % 2 == 0:
                    f = 0
                else: 
                    f = 7
                rook = Piece(self.board, "rook", player)
                rook.place(self.board.squares[r][f])
                b += 1
            a += 1
        for _ in range(2):
            for _ in range(2):
                if a % 2 == 0:
                    r = 0
                    player = self.player2
                else:
                    r = 7
                    player = self.player1
                if b % 2 == 0:
                    f = 1
                else: 
                    f = 6
                rook = Piece(self.board, "knight", player)
                rook.place(self.board.squares[r][f])
                b += 1
            a += 1
        for _ in range(2):
            for _ in range(2):
                if a % 2 == 0:
                    r = 0
                    player = self.player2
                else:
                    r = 7
                    player = self.player1
                if b % 2 == 0:
                    f = 2
                else: 
                    f = 5
                rook = Piece(self.board, "bishop", player)
                rook.place(self.board.squares[r][f])
                b += 1
            a += 1
        f = 3
        for _ in range(2):
            if a % 2 == 0:
                r = 0
                player = self.player2
            else: 
                r = 7
                player = self.player1
            queen = Piece(self.board, "queen", player)
            queen.place(self.board.squares[r][f])
            a += 1
        f = 4
        for _ in range(2):
            if a % 2 == 0:
                r = 0
                player = self.player2
            else: 
                r = 7
                player = self.player1
            king = Piece(self.board, "king", player)
            king.place(self.board.squares[r][f])
            a += 1

            

        self.player1.board = self.board
        self.player2.board = self.board
        for p in self.board.pieces:
            p.checkVision()

        while not self.gameOver:
            self.player1.checkMaterial()
            self.player2.checkMaterial()
            # print("Player 1 Material:",self.player1.material)
            # print("Player 2 Material:",self.player2.material)
            self.player1.takeTurn()
            self.player2.takeTurn()

        self.endGame()
        time.sleep(3)
        self.board.win.close()


    def checkGameOver(self):
        if self.turn == self.player2:
            a = True
            j = 0
            while a and j < len(self.player1.pieces):
                if self.player1.pieces[j].vision != []:
                    a = False
                j += 1
            if a:
                if self.player1.check == True:
                    self.gameOver = True
                    self.winner = self.player2.color
                else:
                    self.gameOver = True
                    self.winner = None
        if self.turn == self.player1:            
            a = True
            j = 0
            while a and j < len(self.player2.pieces):
                if self.player2.pieces[j].vision != []:
                    a = False
                j += 1
            if a:
                if self.player2.check == True:
                    self.gameOver = True
                    self.winner = self.player1.color
                else:
                    self.gameOver = True
                    self.winner = None

    def endGame(self):
        if self.winner == "white":
            self.wintext.setText("White wins by checkmate!")
        if self.winner == "black":
            self.wintext.setText("Black wins by checkmate!")
        if self.winner == "none":
            self.wintext.setText("Draw by stalemate")
        self.wintext.draw(self.board.win)






       



       


        
                





        

       



        



