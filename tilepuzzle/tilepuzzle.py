## ECS 170- Assignment 1
## tile puzzle

def tilepuzzle(start, goal):
    return reverse(statesearch([start], goal, []))

#code adapted from pegpuzzle code
def statesearch(unexplored,goal,path):
    if len(path) == 35:#depth limit
        return []
    if unexplored == []:
        return []
    elif goal == head(unexplored):
        return cons(goal, path)
    elif head(unexplored) in path:# stop cycles
        return statesearch(tail(unexplored),
                           goal,
                           path)
    else:
        result = statesearch(generateNewStates(head(unexplored)),
                             goal,
                             cons(head(unexplored), path))
        if result != []:
            return result
        else:

            return statesearch(tail(unexplored),
                               goal,
                               path)


def generateNewStates(currState):
    #result = []
    i,j = find0(currState)
    return moveup(currState,i,j) + moveright(currState,i,j) + movedown(currState,i,j) + moveleft(currState,i,j)


def moveup(currState,i,j):
    if i > 0:#check if possible to move up more
        newState = [row[:] for row in currState]
        newi = i - 1
        switch = newState[newi][j]
        newState[newi][j] = 0
        newState[i][j] = switch
        return [newState]
    else:
        return []


def movedown(currState,i,j):
    if i < (len(currState)-1):
        newState = [row[:] for row in currState]
        newi = i + 1
        switch = newState[newi][j]
        newState[newi][j] = 0
        newState[i][j] = switch
        return [newState]
    else:
        return []


def moveleft(currState,i,j):
    if j > 0:
        newState = [row[:] for row in currState]
        newj = j - 1
        switch = newState[i][newj]
        newState[i][newj] = 0
        newState[i][j] = switch
        return [newState]
    else:
        return []


def moveright(currState,i,j):
    if j < (len(currState[0])-1):
        newState = [row[:] for row in currState]
        newj = j + 1
        switch = newState[i][newj]
        newState[i][newj] = 0
        newState[i][j] = switch
        return [newState]
    else:
        return []
# finds the 0
def find0(currState):
    for i in range(len(currState)):
        for j in range(len(currState[i])):
            #print(currState[i][j])
            if currState[i][j] == 0:### stops at first 0- will need to change if possible to have more 0s
                return (i,j)



# gives the first thing in the list
def head(lst):
    return lst[0]
# appends to the begining of the list
def cons(item, lst):
    return [item] + lst
# pops the first item of the list and returns the rest of the list
def tail(lst):
    return lst[1:]
def reverse(st):
    return st[::-1]

start = [[1,2,3],[4, 5,0],[6,7,8]]
goal = [[0,2,3],[1,4,5],[6,7,8]]
answ = tilepuzzle(start, goal)
print(answ)

print(tilepuzzle([[2,8,3],[1,0,4],[7,6,5]],[[1,2,3],[8,0,4],[7,6,5]]))
print(tilepuzzle([[2,8,3],[0,1,4],[7,6,5]], [[8,3,0],[2,1,4],[7,6,5]]))
