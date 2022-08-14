from Grid_ import Grid
import sys

def Maximize(grid: Grid, depth):
    res = (None, -1)
    if depth == 0 or grid.outOfMoves(p = 0):
        return (None, grid.Eval())
    
    for child in grid.getChildren(p = 0):
        (_, score) = Minimize(child[1], depth - 1)
        if res[1] < score:
            res = (child[0], score)

    return res


def Minimize(grid: Grid, depth):
    res = (None, sys.maxsize)
    if depth == 0 or grid.outOfMoves(p = 1):
        return (None, grid.Eval())
    
    for child in grid.getChildren(p = 1):
        (_, score) = Maximize(child[1], depth - 1)
        if res[1] > score:
            res = (child[0], score)

    return res