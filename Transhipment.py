import numpy as np
from BFS_methods import northwest_corner, minium_cost, vogels

def get_min_loop(tableau, odd):
    min = np.infty
    min_row, min_col = None, None
    for row, col in odd:
        if min > tableau[row, col]:
            min = tableau[row, col]
            min_row, min_col = row, col
    return min, min_row, min_col


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
        if row_move:
            return nodes_in_column
        return nodes_in_row

def get_loop(BFS, erow, ecol):
    def inner(loop):
        if len(loop) > 3:
            can_be_closed = len(get_possible_next_nodes(loop, [(erow, ecol)])) == 1
            if can_be_closed:
                return loop
        not_visited = list(set(BFS) - set(loop))
        possible_next_nodes = get_possible_next_nodes(loop, not_visited)
        for next_node in possible_next_nodes:
            new_loop = inner(loop + [next_node])
            if new_loop:
                return new_loop
    return inner([(erow, ecol)])

def transhipment_simplex(cost, supply, demand):
    supply = supply.flatten()
    demand = demand.flatten()
    nrows, ncols = cost.shape
    if not supply.sum() == demand.sum():
        raise ValueError('Supply and demand must equals')
    tableau, BFS = northwest_corner(supply, demand)
    u = np.zeros(nrows)
    w = np.zeros(ncols)
    while True:
        A, Cij = calc_A_Cij(BFS, cost)
        uw = (np.linalg.inv(A) @ Cij).flatten()
        u[0] = 0
        u[1:] = uw[0:nrows - 1]
        w = uw[nrows - 1:]
        zij_cij = u.reshape(-1, 1) + w - cost
        entry_row, entry_col = np.unravel_index(zij_cij.argmax(), zij_cij.shape)
        if zij_cij[entry_row, entry_col] <= 0:
            return tableau
        loop = get_loop(BFS, entry_row, entry_col)
        even = loop[::2]
        odd = loop[1::2]
        theta, min_row, min_col = get_min_loop(tableau, odd)
        for row, col in even:
            tableau[row, col] += theta
        for row, col in odd:
            tableau[row, col] -= theta
        BFS.remove((min_row, min_col))
        BFS.append((entry_row, entry_col))



if __name__ == '__main__':
    cost = np.array([
        [8,6,10,9],
        [9,12,13,7],
        [14,9,16,5]
    ])
    supply = np.array([35,50,40])
    demand = np.array([45,20,30,30])
    print(transhipment_simplex(cost, supply, demand))


