import numpy as np
from BFS_methods import northwest_corner, minium_cost, vogels
def calc_A_Cij(BFS, cost):
    nrows, ncols = cost.shape
    size = nrows + ncols
    A = np.array([[1 if uw==i or uw == nrows + j else 0 for uw in range(size)] for i, j in BFS])
    A = A[:,1:]
    C = np.array([cost[i,j] for i,j in BFS]).reshape(-1,1)
    return A, C

def get_possible_next_nodes(loop, not_visited):
    last_node = loop[-1]
    nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
    nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]
    if len(loop) < 2:
        return nodes_in_row + nodes_in_column
    else:
        prev_node = loop[-2]
        row_move = prev_node[0] == last_node[0]
        if row_move: return nodes_in_column
        return nodes_in_row
def create_tree(BFS, erow, ecol):
    def row_BFS(erow, height):
        row = []
        for irow, icol in BFS:
            if irow == erow:
                row.append((irow, icol, height))
        return row
    def col_BFS(ecol, height):
        col = []
        for irow, icol in BFS:
            if icol == ecol:
                col.append((irow, icol, height))
        return col
    height = 0
    childs = row_BFS(erow, height + 1)
    stack = childs
    tree = [(erow, ecol, height, childs)]
    while stack:
        irow, icol, height = stack.pop(0)
        childs = row_BFS(irow, height + 1)
        if height%2 == 1:
            childs = col_BFS(icol, height + 1)
        tree.append((irow, icol, height, childs))
        if (erow, ecol, 0) in childs:
            break


def transhipment_simplex(cost, supply, demand):
    supply = supply.flatten()
    demand = demand.flatten()
    nrows, ncols = cost.shape
    if not supply.sum() == demand.sum():
        raise ValueError('Supply and demand must equals')
    tableau, BFS = northwest_corner(supply, demand)
    u = np.zeros(nrows)
    w = np.zeros(ncols)
    A, Cij = calc_A_Cij(BFS, cost)
    uw = (np.linalg.inv(A) @ Cij).flatten()
    u[0] = 0
    u[1:] = uw[0:nrows-1]
    w = uw[nrows-1:]
    zij_cij = u.reshape(-1,1) + w - cost
    entry_row, entry_col = np.unravel_index(zij_cij.argmax(), zij_cij.shape)
    if zij_cij[entry_row, entry_col] <= 0:
        return tableau
    loop =


if __name__ == '__main__':
    cost = np.array([
        [8,6,10,9],
        [9,12,13,7],
        [14,9,16,5]
    ])
    supply = np.array([35,50,40])
    demand = np.array([45,20,30,30])
    transhipment_simplex(cost, supply, demand)


