# https://www.codewars.com/kata/55171d87236c880cea0004c6

from collections import defaultdict
import numpy as np

def np_has_duplicates(a):
    u, c = np.unique(a, return_counts=True)
    dup = u[c>1]
    return np.any(dup != 0)


def has_duplicates(pz):
    for i in range(len(pz)):
        if np_has_duplicates(pz[i]):
            return True
    
    for i in range(len(pz[0])):
        if np_has_duplicates(pz[:,i]):
            return True
    
    for i in [0, 3, 6]:
        if np_has_duplicates(pz[i:i+3, i:i+3]):
            return True

    return False


def _solve(cols, out):
    if len(cols) == 0:
        return True

    col_id = min(cols.items(), key=lambda x:len(x[1]))[0]

    row_ids = cols[col_id]
    if len(row_ids) == 0:
        return False
    
    flag = False
    for row_id in row_ids:
        r_col_ids = {
            k for k,v in cols.items()
            if row_id in v}

        r_row_ids = {
            v for r_col_id in r_col_ids 
            for v in cols[r_col_id]}

        cols_next = {}
        for k,v in cols.items():
            if k in r_col_ids: 
                continue
            cols_next[k] = v - r_row_ids

        if _solve(cols_next, out):
            out.append(row_id)
            flag = True

    return flag


def gen_candidates(i, k, pz):
    horizontal = pz[i, :]
    vertical = pz[:, k] 
    ii, kk = i//3, k//3
    box = pz[ii*3:(ii+1)*3, kk*3:(kk+1)*3].flat
    nums = set(range(1,10))
    nums -= set(horizontal)
    nums -= set(vertical)
    nums -= set(box)
    return nums


def gen_puzzle_candidates(pz):
    pzc = {}
    for i,k in zip(*np.where(pz==0)):    
        ns = gen_candidates(i,k,pz)
        pzc[(i,k)] = ns
    return pzc


def gen_groups(pzc):
    groups = defaultdict(set)
    for i,k in pzc.keys():
        for v in pzc[(i,k)]:
            assert v != 0
            groups[('row_col', i, k)].add((i,k,v))
            
            groups[('row', i, v)].add((i,k,v))
            groups[('col', k, v)].add((i,k,v))

            ii, kk = (i//3)*3, (k//3)*3
            groups[('box', ii, kk, v)].add((i,k,v))
    return dict(groups)


def must_valid(pz):
    if pz.shape != (9,9): raise ValueError()
    if np.any(pz < 0): raise ValueError()
    if np.any(9 < pz): raise ValueError()
    if (pz != 0).sum() < 17: raise ValueError()
    if has_duplicates(pz): raise ValueError()


def solve(puzzle):
    pz = np.array(puzzle)
    must_valid(pz)
    pzc = gen_puzzle_candidates(pz)
    groups = gen_groups(pzc)
    out = []
    _solve(groups, out)
    for i,k,v in out: pz[i,k] = v
    return pz.tolist()
