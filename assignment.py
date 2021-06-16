import numpy as np
from itertools import combinations

def crossed_rows_columns(cross):
    size = cross.shape[0]
    indexes = [i for i in range(size*2)]
    for num_lines in range(1, size+1):
        for combination in combinations(indexes, num_lines):
            rows_cols = np.zeros(size*2)
            rows_cols[list(combination)] = 1
            xrow, xcol = rows_cols[:size].astype(bool), rows_cols[size:].astype(bool)
            reduced_matrix = (~xrow.reshape(-1, 1)) & (~xcol)
            if np.count_nonzero(cross[reduced_matrix]) == 0:
                return xrow, xcol, num_lines
def hungarian_method(cost):
    size = cost.shape[0]
    min_row = cost.min(axis=1).reshape(size,1)
    cost = cost - min_row
    min_col = cost.min(axis=0)
    cost = cost - min_col
    ones = np.ones(size)
    while True:
        cross = (cost == 0).astype(int)
        x_rows, x_cols, crossed = crossed_rows_columns(cross)
        if crossed == size:
            cross = (cost == 0).astype(int)
            return cross
        nx_rows, nx_cols = np.logical_not(x_rows), np.logical_not(x_cols)
        reduced_matrix = nx_cols & nx_rows.reshape(-1, 1)
        cover_twice_matrix = x_cols & x_rows.reshape(-1, 1)
        k = cost[reduced_matrix].min()
        cost[reduced_matrix] -= k
        cost[cover_twice_matrix] += k
if __name__ == '__main__':
    #cost = np.array([
    #    [47, 50, 57, 57, 0],
    #    [48, 52, 52, 62, 0],
    #    [50, 55, 54, 59, 0],
    #    [52, 54, 55, 60, 0],
    #    [51, 51, 53, 58, 0]
    #])
    cost = np.array([
        [42, 46, 2, 9, 26],
        [15, 43, 26, 49, 19],
        [27, 6, 15, 44, 33],
        [7, 7, 7, 0, 34],
        [35, 27, 16, 41, 33]])
    print(hungarian_method(cost))