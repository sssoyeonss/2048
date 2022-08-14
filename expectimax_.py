from Grid_ import Grid
import sys

def Maximize_(grid: Grid, depth):
    if depth == 0 or grid.outOfMoves(p = 0):
        return (None, grid.Eval())
    
    res = (None, -1)
    for child in grid.getChildren(p = 0):
        score = Minimize_(child[1], depth - 1)
        if score > res[1]:
            res = (child[0], score)

    return res

def Minimize_(grid: Grid, depth):
    empty = grid.getChildren(p = 1)
    prob = 1 / (len(empty) / 2)
    res = 0
    for child in empty:
        res += child[0] * prob * (Maximize_(child[1], depth - 1)[1])

    return res