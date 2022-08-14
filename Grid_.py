from copy import deepcopy
from typing import List, Tuple

class Grid:
    def __init__(self, matrix):
        self.size = len(matrix)
        self.matrix = matrix

    def checkMoveUp(self):
        for j in range(self.size):
            ver = -1
            for i in range(self.size - 1, -1, -1):
                if self.matrix[i][j] > 0:
                    ver = i
                    break
            if ver > -1:
                for i in range(ver, -1, -1):
                    if self.matrix[i][j] == 0:
                        return True
                    elif i != 0 and self.matrix[i - 1][j] == self.matrix[i][j]:
                        return True
        return False

    def checkMoveDown(self):
        for j in range(self.size):
            ver = -1
            for i in range(self.size):
                if self.matrix[i][j] > 0:
                    ver = i
                    break
            if ver > -1:
                for i in range(ver, self.size):
                    if self.matrix[i][j] == 0:
                        return True
                    elif i != self.size - 1 and self.matrix[i][j] == self.matrix[i + 1][j]:
                        return True
        
        return False
    
    def checkMoveLeft(self):
        for i in range(self.size):
            ver = -1
            for j in range(self.size - 1, -1, -1):
                if self.matrix[i][j] > 0:
                    ver = j
                    break
            if ver > -1:
                for j in range(ver, -1, -1):
                    if self.matrix[i][j] == 0:
                        return True
                    elif j != 0 and self.matrix[i][j] == self.matrix[i][j - 1]:
                        return True
            
        return False
    
    def checkMoveRight(self):
        for i in range(self.size):
            ver = -1
            for j in range(self.size):
                if self.matrix[i][j] > 0:
                    ver = j
                    break
            if ver > -1:
                for j in range(ver, self.size):
                    if self.matrix[i][j] == 0:
                        return True
                    elif j != self.size - 1 and self.matrix[i][j] == self.matrix[i][j + 1]:
                        return True
        
        return False

    def moveUp(self):
        temp = deepcopy(self)
        for j in range(temp.size):
            ite = 0
            last_val = 0
            for i in range(temp.size):
                if temp.matrix[i][j] == 0:
                    continue
                if last_val == 0:
                    last_val = temp.matrix[i][j]
                    temp.matrix[ite][j] = last_val
                elif last_val == temp.matrix[i][j]:
                    temp.matrix[ite][j] = last_val * 2
                    last_val = 0
                    ite += 1
                else:
                    ite += 1
                    temp.matrix[ite][j] = temp.matrix[i][j]
                    last_val = temp.matrix[i][j]
        
        if last_val == 0:
            ite -= 1
        
        return temp
            
    def moveDown(self):
        temp = deepcopy(self)
        for j in range(temp.size):
            ite = temp.size - 1
            last_val = 0
            for i in range(temp.size - 1, -1, -1):
                if temp.matrix[i][j] == 0:
                    continue
                if last_val == 0:
                    last_val = temp.matrix[i][j]
                    temp.matrix[ite][j] = last_val
                elif last_val == temp.matrix[i][j]:
                    temp.matrix[ite][j] = 2 * last_val
                    last_val = 0
                    ite -= 1
                else:
                    last_val = temp.matrix[i][j]
                    ite -= 1
                    temp.matrix[ite][j] = temp.matrix[i][j]
        
            if last_val == 0:
                ite += 1
        
            for i in range(ite - 1, -1, -1):
                temp.matrix[i][j] = 0
        
        return temp

    def moveLeft(self):
        temp = deepcopy(self)
        for i in range(temp.size):
            ite = 0
            last_val = 0
            for j in range(temp.size):
                if temp.matrix[i][j] == 0:
                    continue
                if last_val == 0:
                    last_val = temp.matrix[i][j]
                    temp.matrix[i][ite] = last_val
                elif last_val == temp.matrix[i][j]:
                    temp.matrix[i][ite] = 2 * last_val
                    last_val = 0
                    ite += 1
                else:
                    ite += 1
                    temp.matrix[i][ite] = temp.matrix[i][j]
                    last_val = temp.matrix[i][j]
            if last_val == 0:
                ite -= 1
            for j in range(ite + 1, temp.size):
                temp.matrix[i][j] = 0

        return temp
    
    def moveRight(self):
        temp = deepcopy(self)
        for i in range(temp.size):
            last_val = 0
            ite = temp.size - 1
            for j in range(self.size - 1, -1, -1):
                if temp.matrix[i][j] == 0:
                    continue
                if last_val == 0:
                    last_val = temp.matrix[i][j]
                    temp.matrix[i][ite] = last_val
                elif last_val == temp.matrix[i][j]:
                    temp.matrix[i][ite] = 2 * last_val
                    ite -= 1
                    last_val = 0
                else:
                    ite -= 1
                    temp.matrix[i][ite] = temp.matrix[i][j]
                    last_val = temp.matrix[i][j]

            if last_val == 0:
                ite += 1
            
            for j in range(ite - 1, -1, -1):
                temp.matrix[i][j] = 0
        
        return temp

    def outOfMoves(self, p):
        if(p == 0): #Max
            if self.checkMoveLeft():
                return False
            if self.checkMoveUp():
                return False
            if self.checkMoveRight():
                return False
            if self.checkMoveDown():
                return False
            return True
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] == 0:
                        return False
            return True
        
    def getChildren(self, p):
        res = []
        if p == 0: #Max
            if self.checkMoveLeft():
                temp = self.moveLeft()
                res.append((0, temp))
            if self.checkMoveUp():
                temp = self.moveUp()
                res.append((1, temp))
            if self.checkMoveRight():
                temp = self.moveRight()
                res.append((2, temp))
            if self.checkMoveDown():
                temp = self.moveDown()
                res.append((3, temp))
        else:
            for i in range(self.size):
                for j in range(self.size):
                    if self.matrix[i][j] == 0:
                        t1 = deepcopy(self)
                        t1.matrix[i][j] = 2
                        res.append((0.9, t1))
                        
                        t1.matrix[i][j] = 4
                        res.append((0.1, t1))
        return res

    def Eval(self):
        w_all = []
        w = []
        cur = self.size
    #UL
        for i in range(self.size):
            ij = []
            #ij.append(cur * 3)
            for j in range(cur, cur-self.size, -1):
                ij.append(j)
            cur -= 1
            w.append(ij)
        w[0][0] *= self.size
        w_all.append(w)
        w = []
    #UR
        cur = self.size
        for i in range(self.size):
            ij = []
            for j in range(cur - self.size + 1, cur + 1):
                ij.append(j)
            #ij.append(cur * 3)
            cur -= 1
            w.append(ij)
        w[0][self.size - 1] *= self.size
        w_all.append(w)
    #DL
        cur = 1
        w = []
        for i in range(self.size):
            ij = []
            for j in range(cur, cur - self.size, -1):
                ij.append(j)
            cur += 1
            w.append(ij)
        w[self.size - 1][0] *= self.size
        w_all.append(w)
    #DR
        cur = 1
        w = []
        for i in range(self.size):
            ij = []
            for j in range(cur - self.size + 1, cur + 1):
                ij.append(j)
            cur += 1
            w.append(ij)
        w[self.size - 1][self.size - 1] *= self.size
        w_all.append(w)

        values = [0, 0, 0, 0]
        for c in range(4):
            for i in range(self.size):
                for j in range(self.size):
                    values[c] += self.matrix[i][j] * w_all[c][i][j]
        
        res = values[0]
        for i in range(4):
            res = max(res, values[i])
        
        return res

    def Eval_2(self):
        score = 0
        cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                score += self.matrix[i][j]
                if self.matrix[i][j] == 0:
                    cnt += 1
        
        return score / (self.size * self.size - cnt)

    def Eval_3(self):
        return self.Eval() + self.Eval_2()

    def Eval_4(self):
        r = []
        rul = [[2 ** 15, 2 ** 14, 2 ** 13, 2 ** 12],
            [2 ** 8, 2 ** 9, 2 ** 10, 2 ** 11],
            [2 ** 7, 2 ** 6, 2 ** 5, 2 ** 4],
            [2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3]]
        r.append(rul)
        rur = [[2 ** 12, 2 ** 13, 2 ** 14, 2 ** 15],
            [2 ** 11, 2 ** 10, 2 ** 9, 2 ** 8],
            [2 ** 4, 2 ** 5, 2 ** 6, 2 ** 7],
            [2 ** 3, 2 ** 2, 2 ** 1, 2 ** 0]]
        r.append(rur)
        rdl = [[2 ** 0, 2 ** 1, 2 ** 2, 2 ** 3],
            [2 ** 7, 2 ** 6, 2 ** 5, 2 ** 4],
            [2 ** 8, 2 ** 9, 2 ** 10, 2 ** 11],
            [2 ** 15, 2 ** 14, 2 ** 13, 2 ** 12]]
        r.append(rdl)
        rdr = [[2 ** 3, 2 ** 2, 2 ** 1, 2 ** 0],
            [2 ** 4, 2 ** 5, 2 ** 6, 2 ** 7],
            [2 ** 11, 2 ** 10, 2 ** 9, 2 ** 8],
            [2 ** 12, 2 ** 13, 2 ** 14, 2 ** 15]]
        r.append(rdr)
        val = [0, 0, 0, 0]
        for ind in range(4):
            for i in range(self.size):
                for j in range(self.size):
                    val[ind] += self.matrix[i][j] * r[ind][i][j]
        res = val[0]
        for i in range(4):
            res =  max(res, val[0])
        return res
