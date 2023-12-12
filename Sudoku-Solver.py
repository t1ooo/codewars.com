# https://www.codewars.com/kata/5296bc77afba8baa690002d7

# %%
import numpy as np

def sudoku_v1(puzzle):
    def horizontal(i, pz): return pz[i,:]
    def vertical(k, pz): return pz[:,k]
    def square(i, k, pz):
        i, k = int(i/3), int(k/3)
        return pz[i*3:(i+1)*3, k*3:(k+1)*3]

    def f(i, k, pz):
        if not (i < len(pz)):    return pz, 0 not in pz
        if not (k < len(pz[i])): return f(i+1, 0, pz)
        if pz[i,k] != 0:         return f(i, k+1, pz)

        for v in range(1,10):
            if v in horizontal(i,pz): continue
            if v in vertical(k, pz):  continue
            if v in square(i, k, pz): continue
            pz[i,k] = v
            solution, solved = f(i, k+1, pz.copy())
            if solved: return solution, solved
        
        return pz, False

    return f(0, 0, np.array(puzzle))[0].tolist()


def sudoku(puzzle):
    def horizontal(i, pz): return pz[i, :]
    def vertical(k, pz): return pz[:, k]
    def square(i, k, pz):
        i, k = i//3, k//3
        return pz[i*3:(i+1)*3, k*3:(k+1)*3]

    def f(i, k, pz):
        if not (i < len(pz)):    return True
        if not (k < len(pz[i])): return f(i+1, 0, pz)
        if pz[i, k] != 0:        return f(i, k+1, pz)

        for v in range(1,10):
            if v in horizontal(i, pz): continue
            if v in vertical(k, pz):   continue
            if v in square(i, k, pz):  continue
            pz[i,k] = v
            if f(i, k+1, pz): return True
            pz[i,k] = 0
        
        return False

    pz = np.array(puzzle)
    f(0, 0, pz)
    return pz.tolist()


def assert_equals(actual, expected, msg=''):
    def fmt_lst(lst):
        return '\n'+'\n'.join(str(v) for v in lst)
    assert actual == expected,\
        f'{msg}\nactual:   {fmt_lst(actual)}\nexpected: {fmt_lst(expected)}'


puzzle = [[5,3,0,0,7,0,0,0,0],
          [6,0,0,1,9,5,0,0,0],
          [0,9,8,0,0,0,0,6,0],
          [8,0,0,0,6,0,0,0,3],
          [4,0,0,8,0,3,0,0,1],
          [7,0,0,0,2,0,0,0,6],
          [0,6,0,0,0,0,2,8,0],
          [0,0,0,4,1,9,0,0,5],
          [0,0,0,0,8,0,0,7,9]]

solution = [[5,3,4,6,7,8,9,1,2],
            [6,7,2,1,9,5,3,4,8],
            [1,9,8,3,4,2,5,6,7],
            [8,5,9,7,6,1,4,2,3],
            [4,2,6,8,5,3,7,9,1],
            [7,1,3,9,2,4,8,5,6],
            [9,6,1,5,3,7,2,8,4],
            [2,8,7,4,1,9,6,3,5],
            [3,4,5,2,8,6,1,7,9]]

assert_equals(sudoku(puzzle), 
              solution,
              "Incorrect solution for the following puzzle: " + str(puzzle));
