'''
rush hour
- Representing the board state
    - Node class: keep track of the board
    - Vehicle class: keep track of the position of the car

- Helper functions:
    - conv: converts input to match how the node class expects it
    - makeVehicleList: parses the input of the board into a list of vehicles(class organizes positions and orientation of the vehicle)
    - searchfornode: searches for the list for a node (both provided as input
    - generateNewStates: creates new nodes for each possible vehicle movement
    - bfsSearch: implementation of the a* algorithm

- rushour: converts input and passes into bfsSearch and then prints what has been returned


'''

import heapq
import copy


# represents a single vehicle on the board
class Vehicle:

    def __init__(self, letter, pos, orientation):
        #position of the 'head' of the vehicle
        self.posh = pos[0]
        # position of the 'tail' of the vehicle
        self.post = pos[1]
        self.orientation = orientation
        self.name = letter

    def __str__(self):
        return "Vehicle {name} with head {pos} and tail {pos1} orientation {o}".format(name=self.name, pos=self.posh, pos1 = self.post,o = self.orientation)


## stores the board, a vehicle list, f(n), g(n), and h(n)
class Node:

    def __init__(self, board, vehicleList, parent, g = 0):
        self.board = board
        self.vehicleList = vehicleList
        self.parent = parent

        self.g = g
        self.h = 0
        self. f = self.g + self.h

    def setH(self,h):
        self.h = h

    def updateF(self):
        self.f = self.g + self.h


    ## calculates tehe blocking heuristic
    def blockingHeur(self):
        xcar = [car for car in self.vehicleList if car.name == 'X']#should only be 1
        xcar = xcar[0]
        txcar = xcar.post[1]
        blockingheur = 1
        for i in range(txcar + 1, 6):
            if self.board[2][i] != '-':
                blockingheur += 1
        return blockingheur

    #ignore
    def myHeur2(self):
        xcar = [car for car in self.vehicleList if car.name == 'X']  # should only be 1
        xcar = xcar[0]
        txcar = xcar.post[1]
        myheur = 1
        for i in range(txcar + 1, 6):
            if self.board[2][i] != '-':
                myheur += 1
                vname = self.board[2][i]
                carblock = [car for car in self.vehicleList if car.name == vname]
                carblock = carblock[0]
                if (carblock.posh[0]-1)<0 or self.board[carblock.posh[0] - 1][i] != '-':
                    myheur += 1
                if (carblock.post[0]+1)>5 or self.board[carblock.post[0] + 1][i] != '-':
                    myheur += 1
        return myheur

    ## my heuristic counts the vehicles blocking the X car and then counts the vehicles blocking that car anf add how far the X car is from the goal state
    def myHeur3(self):
        xcar = [car for car in self.vehicleList if car.name == 'X']  # should only be 1
        xcar = xcar[0]
        txcar = xcar.post[1]
        myheur = 5 - txcar#distance from endstate
        for i in range(txcar + 1, 6):
            if self.board[2][i] != '-':
                myheur += 1
                vname = self.board[2][i]
                carblock = [car for car in self.vehicleList if car.name == vname]
                carblock = carblock[0]
                if (carblock.posh[0]-1)<0 or self.board[carblock.posh[0] - 1][i] != '-':
                    myheur += 1
                if (carblock.post[0]+1)>5 or self.board[carblock.post[0] + 1][i] != '-':
                    myheur += 1
        return myheur
    #ignore
    def myHeur1(self):
        xcar = [car for car in self.vehicleList if car.name == 'X']  # should only be 1
        xcar = xcar[0]
        txcar = xcar.post[1]
        myheur = 5 - txcar  # distance from endstate
        for i in range(txcar + 1, 6):
            if self.board[2][i] != '-':
                myheur += 1
        return myheur


    def __repr__(self):
        newStr = ""
        for i in self.board:
            for j in i:
                newStr = newStr + j + " "
            newStr = newStr + "\n"
        return newStr

    def __lt__(self, other):
        return self.f < other.f

    #def __eq__(self, other):
        #return self.board == other.board

# creates a node of the start board and then passes it into the best first search funtion and then manipulates the output to print correctly
def rushhour(heur, start):
    startB = conv(start)
    startNode = Node(startB, makeVehicles(startB),None,0)
    path, expStates = bfsSearch(heur, [startNode], [])
    if path == []:
        print ("No solution ")
        print("Total states Explored: ", expStates)
    else:
        toprint = ""
        for i in path:
            toprint = toprint + str(i) + "\n"
        print(toprint)
        print('Total Moves: ', (len(path)-1))#subtract because path includes the start state
        print("Total states Explored: ", expStates)

# my implementation of the a* algorithm
# not necessary to pass an explored list just and artifact of trying a recursive algorithm before doing this implementation
def bfsSearch(heur, unexplored, explored):
    exploredstatescounter = 0
    while unexplored != []:
        for state in unexplored:
            #print(heur)
            #pick which heuristic to calculate
            if heur == 0:
                state.setH(state.blockingHeur())
            else:
                state.setH(state.myHeur3())
            state.updateF()
        #sort the unexplored list and pick the one with least f(n)
        heapq.heapify(unexplored)
        currNode = heapq.heappop(unexplored)
        explored.append(currNode)
        if currNode.board[2][4] == 'X' and currNode.board[2][5] == 'X':
            # function that makes the path by exploring the parent recursively
            path = getPath(currNode)
            return (path + [currNode],len(explored))
        else:
            newStatesList = genNewStates(currNode)
            for newState in newStatesList:
                #check if the newstate has been seen already
                if searchfornodes(unexplored,newState):
                    continue
                elif searchfornodes(explored, newState):
                    continue
                else:
                    unexplored.append(newState)
        #explored.append(currNode)

    return ([], len(explored))

# takes a node and then returns a list of next possible states
def genNewStates(currNode):
    newStates = []
    for i in range(len(currNode.vehicleList)):
        if currNode.vehicleList[i].orientation == 'h':
            row = currNode.vehicleList[i].posh[0]
            head = currNode.vehicleList[i].posh[1]
            tail = currNode.vehicleList[i].post[1]
            # move left
            newStates = newStates + moveLeft(currNode,i,row, head, tail)
            # move right
            newStates = newStates + moveRight(currNode,i,row, head, tail)

        else:
            col = currNode.vehicleList[i].posh[1]
            head = currNode.vehicleList[i].posh[0]
            tail = currNode.vehicleList[i].post[0]
            # move up
            newStates = newStates + moveUp(currNode,i,col,head,tail)
            # move down
            newStates = newStates + moveDown(currNode,i,col,head,tail)
    return newStates


## how moves are made to generate new states:
## new node is made by copying the last node and changing the positions in vehicleList and Board accordingly.
## Also checks to make sure that the move is possible
def moveLeft(currNode,vindex, row, head, tail):
    vehicle = currNode.vehicleList[vindex]
    if head > 0 and currNode.board[row][head - 1] == '-':
        newboardState = [row[:] for row in currNode.board]
        # changing the board representation
        newboardState[row][head - 1] = vehicle.name
        newboardState[row][tail] = '-'
        # changing the vehicle representation
        newVehicleList = copy.deepcopy(currNode.vehicleList)
        #newVehicleList = []
        #[newVehicleList.append(i) for i in currNode.vehicleList]
        newVehicleList[vindex].posh = (row, head - 1)
        newVehicleList[vindex].post = (row, tail - 1)
        newg = currNode.g + 1
        return [Node(newboardState, newVehicleList, currNode, newg)]
    else:
        return []


def moveRight(currNode,vindex, row, head, tail):
    vehicle = currNode.vehicleList[vindex]

    if tail<5 and currNode.board[row][tail + 1] == '-':
        newboardState = [row[:] for row in currNode.board]
        # changing the board representation
        newboardState[row][tail + 1] = vehicle.name
        newboardState[row][head] = '-'
        # changing the vehicle representation
        newVehicleList = copy.deepcopy(currNode.vehicleList)
        newVehicleList[vindex].posh = (row, head + 1)
        newVehicleList[vindex].post = (row, tail + 1)
        newg = currNode.g + 1
        return [Node(newboardState, newVehicleList, currNode, newg)]
    else:
        return []


def moveUp(currNode, vindex, col, head, tail):

    vehicle = currNode.vehicleList[vindex]
    if head > 0 and currNode.board[head-1][col] == '-':
        newboardState = [row[:] for row in currNode.board]
        # changing the board representation
        newboardState[head -1][col] = vehicle.name
        newboardState[tail][col] = '-'
        # changing the vehicle representation
        newVehicleList = copy.deepcopy(currNode.vehicleList)
        newVehicleList[vindex].posh = (head-1, col)
        newVehicleList[vindex].post = (tail-1, col)
        newg = currNode.g + 1
        return [Node(newboardState, newVehicleList, currNode, newg)]
    else:
        return []


def moveDown(currNode, vindex, col, head, tail):

    vehicle = currNode.vehicleList[vindex]
    if tail<5 and currNode.board[tail + 1][col] == '-':
        newboardState = [row[:] for row in currNode.board]
        # changing the board representation
        newboardState[tail+1][col] = vehicle.name
        newboardState[head][col] = '-'
        # changing the vehicle representation
        newVehicleList = copy.deepcopy(currNode.vehicleList)
        newVehicleList[vindex].posh = (head + 1, col)
        newVehicleList[vindex].post = (tail + 1, col)
        newg = currNode.g + 1
        return [Node(newboardState, newVehicleList, currNode, newg)]
    else:
        return []

# gets path from current node to the start node
def getPath(node):
    path = []
    if node.parent == None:
        return []
    else:
        return getPath(node.parent) + [node.parent]
    
# takes in a list of nodes and a node and checks if the node is in the list of nodes
def searchfornodes(unexplored, newState):
    for i in unexplored:
        if i.board == newState.board:
            return True
    return False

# turn list of strings input in to a list of list of single letters
def conv(instate):
    res = []
    for i in instate:
        res1 = []
        for j in i:
            res1.append(j)
        res.append(res1)
    return res

# parses the board to attach indices and orientation(stored in vehicle class) for all vehicles.
# returns a list of vehicles
def makeVehicles(jinstate):
    vehicleList = []
    instate = [row[:] for row in jinstate]
    for row in range(len(instate)):
        #k = instate(row)
        for col in range(len(instate[row])):
            lettercur = instate[row][col]
            #print(instate[row + 2][col])
            if (lettercur != '-'):
                if (col+2) < 6 and instate[row][col + 2] == lettercur:
                    v = Vehicle(lettercur,[(row, col),(row,col+2)], 'h')
                    vehicleList.append(v)
                    instate[row][col:col+3] = ['-','-','-']
                    col += 3

                elif (col+1) < 6 and instate[row][col + 1] == lettercur:
                    v = Vehicle(lettercur,[(row, col),(row,col+1)], 'h')
                    vehicleList.append(v)
                    instate[row][col:col + 2] = ['-', '-']
                    col += 2


                elif (row+2) < 6 and instate[row + 2][col] == lettercur:
                    v = Vehicle(lettercur,[(row, col), (row + 2, col)], 'v')
                    vehicleList.append(v)
                    instate[row][col] = '-'
                    instate[row+1][col] = '-'
                    instate[row+2][col] = '-'

                elif((row+1) < 6 and instate[row + 1][col] == lettercur):
                    v = Vehicle(lettercur,[(row, col), (row + 1, col)], 'v')
                    vehicleList.append(v)
                    instate[row][col] = '-'
                    instate[row+1][col] = '-'
    return vehicleList


### Teting

hardpuzzle = ["MMMDEF", "ANNDEF", "A-XXEF", "PPC---", "-BC-QQ","-BRRSS"]
simplepuzzle = conv(["--B---","--B---","XXB---","--AA--","------","------"])
puzzle = conv(["------", "---B--", "XX-B--","---B--","------","--AA--"])



puzzle1 = ["--B---","--B---","XXB---","----C-","--EEC-","----C-"]
puzzle2 = ["-ABBCC","-ADDDE","-AXX-E","--F---","--FGGG","HHIII-"]
puzzle3 = ["ABBCC-", "ADDEFF", "XXGEHI", "J-GKHI", "J--K--", "JLLK--"]
puzzle4 = ["-ABBCD", "-AEFCD", "XXEF--", "--GH--", "--GHII", "------"]

##Ep 11
beginnerCard = ["OOOP--", "--AP--", "XXAP--", "Q-----", "QGGCCD", "Q----D"]
intermediatecard = ["--OPPP", "--O--A", "XXO--A", "-CC--Q", "-----Q", "--RRRQ"]
advancedcard = ["-ABBO-",  "-ACDO-", "XXCDO-", "PJFGG-", "PJFH--", "PIIH--"]
expertcard = ["OOO--P", "-----P", "--AXXP", "--ABCC", "D-EBFF", "D-EQQQ"]

puzzlenode = Node(board=hardpuzzle, vehicleList=makeVehicles(conv(hardpuzzle)),parent=None, g=1)
#print(puzzlenode)
#print(puzzlenode.myHeur())

#print(*c)
#print(*puzzle2)

#rushhour(3,hardpuzzle)
'''for i in range (4):
    print("heuristic ", i)
    rushhour(i,expertcard)
    print("\n")'''


rushhour(1,hardpuzzle)





