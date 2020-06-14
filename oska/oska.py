#Assignment 3 p1
'''
- move gen
- static board evaluation
- minimax control
- output in string
- I assume that white always move downward and black always moves up
'''

import copy
import boardSetUp as bs
import math
thing = []

# generates moves: takes in the string representation and the color to move
# returns a list of boards in string form. If no moves can be made, it returns the string that was passed in
def movegen(stringL,color):
    newBoards = moveGenR(bs.toBoard(stringL), color)
    newStates = []
    for i in newBoards:
        newStates.append(bs.boardtoString(i))
    return newStates

# where most of the move generation happens
# takes in aboard instance and returns a list of board instances for the new moves
def moveGenR(board,color):
    thing.append(1)
    newMoves = []
    if color == 'w':
        for piece in range(len(board.positionsW)):
            i = board.positionsW[piece].posR
            j = board.positionsW[piece].posC
            if i + 1 < len(board.board) and j + 1 < len(board.board):
                leftmove = board.board[i+1][j]
                rightmove = board.board[i][j+1]
                if leftmove == '-':
                    newBoard = copy.deepcopy(board)
                    newBoard.board[i+1][j] = 'w'
                    newBoard.board[i][j] = '-'
                    newBoard.positionsW[piece].posR = i+1
                    newMoves.append(newBoard)
                elif i+2<len(board.board) and leftmove == 'b' and board.board[i+2][j] == '-':
                    newBoard = copy.deepcopy(board)
                    newBoard.board[i + 1][j] = '-'
                    newBoard.board[i + 2][j] = 'w'
                    newBoard.board[i][j] = '-'
                    newBoard.positionsW[piece].posR = i + 2
                    for k in range(len(newBoard.positionsB)):
                         if newBoard.positionsB[k].posR == i+1 and newBoard.positionsB[k].posC == j:
                            newBoard.positionsB.pop(k)
                            break
                    newMoves.append(newBoard)
                if rightmove == '-':
                    newBoard = copy.deepcopy(board)
                    newBoard.board[i][j+1] = 'w'
                    newBoard.board[i][j] = '-'
                    newBoard.positionsW[piece].posC = j + 1
                    newMoves.append(newBoard)
                elif j+2<len(board.board) and rightmove == 'b' and board.board[i][j+2] == '-':
                    newBoard = copy.deepcopy(board)
                    newBoard.board[i][j+1] = '-'
                    newBoard.board[i][j+2] = 'w'
                    newBoard.board[i][j] = '-'
                    newBoard.positionsW[piece].posC = j + 2
                    for k in range(len(newBoard.positionsB)):
                        if newBoard.positionsB[k].posR == i and newBoard.positionsB[k].posC == j+1:
                            newBoard.positionsB.pop(k)
                            break
                    newMoves.append(newBoard)
    else:
        for piece in range(len(board.positionsB)):
            i = board.positionsB[piece].posR
            j = board.positionsB[piece].posC
            leftmove = board.board[i][j-1]
            rightmove = board.board[i-1][j]
            if rightmove == '-':
                newBoard = copy.deepcopy(board)
                newBoard.board[i-1][j] = 'b'
                newBoard.board[i][j] = '-'
                newBoard.positionsB[piece].posR = i-1
                newMoves.append(newBoard)
            elif i-2<len(board.board) and rightmove == 'w' and board.board[i-2][j] == '-':
                newBoard = copy.deepcopy(board)
                newBoard.board[i-1][j] = '-'
                newBoard.board[i-2][j] = 'b'
                newBoard.board[i][j] = '-'
                newBoard.positionsB[piece].posR = i-2
                for k in range(len(newBoard.positionsW)):
                     if newBoard.positionsW[k].posR == i-1 and newBoard.positionsW[k].posC == j:
                        newBoard.positionsW.pop(k)
                        break
                newMoves.append(newBoard)
            if leftmove == '-':
                newBoard = copy.deepcopy(board)
                newBoard.board[i][j-1] = 'b'
                newBoard.board[i][j] = '-'
                newBoard.positionsB[piece].posC = j-1
                newMoves.append(newBoard)
            elif leftmove == 'w' and board.board[i][j-2] == '-':
                newBoard = copy.deepcopy(board)
                newBoard.board[i][j-1] = '-'
                newBoard.board[i][j-2] = 'b'
                newBoard.board[i][j] = '-'
                newBoard.positionsB[piece].posC = j-2
                for k in range(len(newBoard.positionsW)):
                    if newBoard.positionsW[k].posR == i and newBoard.positionsW[k].posC == j-1:
                        newBoard.positionsW.pop(k)
                        break
                newMoves.append(newBoard)
    if newMoves == []:
        return [board]
    return newMoves





# passes a board to minimax and returns a list of strings
def oskaplayer(stringL,color,depth):
    inBoard = bs.toBoard(stringL)
    # white maximizes
    # black minimizes
    outBoard = minmax(inBoard, depth, color)
    return bs.boardtoString(outBoard)





## followed pseudocode from the text book
# Takes in a board, depth and color and applies minimax.

def minmax(inBoard,depth,color):

    childNodes = moveGenR(inBoard,color)
    if color == 'w':
        for child in childNodes:
            minMoves(child,depth-1,'b')
        return max(childNodes)
    else:
        for child in childNodes:
            maxMoves(child,depth-1,'w')
        return min(childNodes)


# finds the max eval
def maxMoves(inBoard,depth,color):
    end, win = gameEnd(inBoard)
    if end:
        #print('here')
        inBoard.staticBoardEval(False, win)
        return inBoard
    childNodes = moveGenR(inBoard, color)
    if depth == 0 or childNodes == []:
        inBoard.staticBoardEval(False)
        return inBoard
    else:
        greatestval = -math.inf
        for child in childNodes:
            greatestval = max(greatestval, minMoves(child, depth - 1, 'b').value)
            inBoard.value = greatestval
        return inBoard

# finds the min eval
def minMoves(inBoard,depth,color):
    end, win = gameEnd(inBoard)
    if end:
        #print('here')
        inBoard.staticBoardEval(True, win)
        return inBoard
    childNodes = moveGenR(inBoard,color)
    if depth == 0 or childNodes==[]:
        inBoard.staticBoardEval(True)
        return inBoard
    else:
        leastval = math.inf
        for child in childNodes:
            leastval = min(leastval, maxMoves(child, depth - 1, 'w').value)
            inBoard.value = leastval
        return inBoard


# used to see if the has ended and returns a tuple of a boolean value and the winner if applicable
# also where a piece is removed from goalpos if a piece has reached a goal value
def gameEnd(inBoard):

    if inBoard.positionsW == []:
        return True, 'b'
    elif  inBoard.positionsB == []:
        return True, 'w'
    peicesMadeW = 0
    for i in inBoard.positionsW:
        for j in inBoard.goalposW:
            if i == j:
                inBoard.goalposW.remove(j)
                peicesMadeW += 1
    if peicesMadeW != len(inBoard.positionsW):
        peicesMadeW = False
    peicesMadeB = 0
    for i in inBoard.positionsB:
        for j in inBoard.goalposB:
            if i == j:
                inBoard.goalposB.remove(j)
                peicesMadeB += 1
    if peicesMadeB != len(inBoard.positionsB):
        peicesMadeB = False
    if peicesMadeB != False and peicesMadeW != False:
        if peicesMadeB > peicesMadeW:
            return True, 'b'
        elif peicesMadeB < peicesMadeW:
            return True, 'w'
        else:
            return True, 'draw'
    elif peicesMadeW != False:
        return True, 'w'
    elif peicesMadeB != False:
        return True, 'b'
    else:
        return False, ''

# a function I used for testing- allows me to play the game
def gamePlayHuman(startBoard,color,depth):
    while True:
        aimove = minmax(b, 4, 'w')
        # print('here')
        print(aimove)
        if aimove.goalposW == []:
            break
        print('your choices')
        a = moveGenR(aimove, 'b')
        count = 0
        for i in a:
            print(count)
            print(i)
            count += 1
        inp = int(input('index of move chosen\n'))
        b = a[inp]
        if gameEnd(b)[0]:
            break
# the ai plays itself- white goes first
def gamePlay(baimove,depth):
    while True:
        aimove = minmax(baimove, depth, 'w')
        print(aimove)
        inp = input('change\n')
        if (aimove.peicesnum - len(aimove.goalposW)) == len(aimove.positionsW):
            break
        else:
            baimove = minmax(aimove, 4, 'b')
            print(baimove)
            inp = input('change\n')
            if (baimove.peicesnum - len(baimove.goalposB)) == len(baimove.positionsB):
                break

string1 = ['-b--', 'w-b', 'wb', 'b--', '----']
print(oskaplayer(string1, 'b', 6))













