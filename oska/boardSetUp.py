## Has all the classes and conversion functions

# Stores the position of a piece and its color- could have just done this in a tuple
class Piece():

    def __init__(self,color,pos1,pos2):
        self.team = color
        self.posR = pos1
        self.posC = pos2

    def __repr__(self):
        newstr = "row " + str(self.posR) + " col " + str(self.posC)
        return newstr

    def __eq__(self, other):
        return (self.posR == other.posR) and (self.posC == other.posC)


## Represents the board in a square grid in the following form:
# x x x w x x
# x x w - x x
# x w - - - b
# w - - - b x
# x x - b x x
# x x b x x x
# x represents invalid spots, - empty spots
class Board():

    def __init__(self, board, positionsW, positionsB):
        self.board = board #internal representation
        # list of pieces
        self.positionsW = positionsW
        self.positionsB = positionsB
        #the heuristic value assigned when evaluated
        self.value = None
        #size on internal representation
        self.size = len(board)
        #number of pieces
        self.peicesnum = int(len(board)/2) + 1
        #the goal positions for the board- when a piece reached goal it is removed from this list
        self.goalposW = []
        self.goalposB = []
        j = self.peicesnum - 1
        i = 0
        while j >= 0:
            self.goalposB.append(Piece('w', i, j))
            i += 1
            j -= 1
        j = self.peicesnum - 2
        i = len(board)-1
        while j < len(board):
            self.goalposW.append(Piece('b', i, j))
            i -= 1
            j += 1

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    # win is the winner of the board if one is found.
    def staticBoardEval(self,min, win = ''):
        # updates the value of the board
        # maximize for white, minimize for black
        # -20 if Black wins
        # 20 if white wins
        # B and W are given scores and at the end wscore-bscore is returned
        # if a piece has not made it across, goal is to get a piece across: quantify this as the number of pieces still in the game
        # if piece has made it across, the goal is to make sure opponent doesnt make more pieces across
            # so lose points for having more active pieces
        # give points for reaching the goal(scale to the number of pieces so that when the score doesn't
        # become negative when you subtract points for having active pieces

        #TODO: draw case
        if win == 'w':
            self.value = 20
        elif win == 'b':
            self.value = -20
        elif win == 'draw':
            if min:
                self.value = -19
            else:
                self.value = 19
        else:
            piecesMadeB = self.peicesnum - len(self.goalposB)
            piecesMadeW = self.peicesnum - len(self.goalposW)
            valueB = (piecesMadeB*self.peicesnum)
            valueW = (piecesMadeW*self.peicesnum)
            # dont want these effects to cancel out
            if piecesMadeW > 0:
                valueW -= len(self.positionsW) - piecesMadeW
            else:
                valueW += len(self.positionsW)
            if piecesMadeB > 0:
                valueB -= len(self.positionsW) - piecesMadeW
            else:
                valueB += len(self.positionsB)
            self.value = valueW - valueB


    def updateH(self,h):
        self.h = h

    def __repr__(self):
        newStr = ''
        for i in self.board:
            for j in i:
                newStr += j + ' '
            newStr +=  '\n'
        return newStr




# convert list of strings to instance of Board class
def toBoard(stringL):
    peicesnum = len(stringL[0])
    boardsize = (peicesnum - 2) + peicesnum
    board = [['x'] * boardsize for k in range(boardsize)]
    stringLiter = 0
    ii = peicesnum - 1
    jj = 0
    positionW = []
    positionB = []
    while stringLiter <= len(stringL) / 2:
        i = ii
        j = jj
        for b in stringL[stringLiter]:
            board[i][j] = b
            if b == 'w' or b == 'W':
                positionW.append(Piece('w', i, j))
            elif b == 'b' or b == 'W':
                positionB.append(Piece('b', i, j))
            j += 1
            i -= 1
        stringLiter += 1
        jj += 1
    ii = peicesnum
    jj = peicesnum - 2
    while stringLiter < len(stringL):
        i = ii
        j = jj
        for b in stringL[stringLiter]:
            board[i][j] = b
            if b == 'w' or b == 'W':
                positionW.append(Piece('w', i, j))
            elif b == 'b' or b == 'W':
                positionB.append(Piece('b', i, j))
            i -= 1
            j += 1
        ii += 1
        stringLiter += 1
    return Board(board, positionW, positionB)

# convert instance of board to list of strings
def boardtoString(board):
    stringL = []
    boardL = board.board
    piecesnum = int((board.size/2) + 1)
    i = piecesnum-1
    jj = 0
    k = piecesnum
    istop = 0
    while k > 1:
        j = jj
        newstr = ""
        while i >= istop:
            newstr = newstr + boardL[i][j]
            i -= 1
            j += 1
        stringL.append(newstr)
        istop += 1
        jj +=1
        i = piecesnum - 1
        k -= 1
    i = piecesnum-2
    jj = piecesnum
    istop = piecesnum
    while jj < board.size:
        j = jj
        newstr = ""
        while i <= istop:
            newstr = newstr + boardL[i][j]
            i += 1
            j -= 1
        newstr = newstr[::-1]
        stringL.append(newstr)
        i = piecesnum-2
        istop += 1
        jj += 1
    return stringL

'''string1a = ['wwww','---','--','---','bbbb']
string1 = ['wwwww', '----','---','--','---','----','bbbbb']
string3 = ['wwwwwW', '--jk-','--f-','---','-a','-s-','--2-','-v---','bbbBbb']
#moveList = movegen(['-----w','-----','-ww-','-b-','-b','w--','w-w-','--b--', '--b-bb'],'w')
a = toBoard(string1a)
b = toBoard(string1)
a.value = 1
b.value = 1
c = 2
print(max(a,b))
'''