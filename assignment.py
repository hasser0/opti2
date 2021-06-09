import numpy as np

def crossed_rows_columns(zeros_row,zeros_col,cross):
    size = zeros_row.shape[0]
    crossed = 0
    x_rows = np.zeros(size,dtype=bool)
    x_cols = np.zeros(size,dtype=bool)
    zeros = np.zeros(size)
    while not((zeros_row==zeros).all() and (zeros_col==zeros).all()):
        r_max_index = zeros_row.argmax()
        r_max = zeros_row[r_max_index]
        c_max_index = zeros_col.argmax()
        c_max = zeros_col[c_max_index]
        if r_max > c_max:
            cross[r_max_index,:] = 0
            x_rows[r_max_index] = True
        else:
            cross[:,c_max_index] = 0
            x_cols[c_max_index] = True
        zeros_col = cross.sum(axis=0)
        zeros_row = cross.sum(axis=1)
        crossed += 1
    return x_rows, x_cols, crossed

def hungarian_method(cost):
    min_row = cost.min(axis=1).reshape(4,1)
    cost = cost - min_row
    min_col = cost.min(axis=0)
    cost = cost - min_col
    cross = (cost == 0).astype(int)
    size = cross.shape[0]
    zeros_col = cross.sum(axis=0)
    zeros_row = cross.sum(axis=1)
    ones = np.ones(size)
    while True:
        cross = (cost == 0).astype(int)
        x_rows, x_cols, crossed = crossed_rows_columns(zeros_row, zeros_col, cross)
        cross = (cost == 0).astype(int)
        if crossed == size:
            return cross
        nx_rows, nx_cols = np.logical_not(x_rows), np.logical_not(x_cols)
        k = cost[nx_rows & nx_cols.reshape(-1, 1)].min()
        cost[nx_rows & nx_cols.reshape(-1, 1)] -= 1
        cost[x_rows & x_cols.reshape(-1, 1)] += 1

if __name__ == '__main__':
    cost = np.array([14, 5, 8, 7, 2, 12, 6, 5,
                     7, 8, 3, 9, 2, 4, 6, 10]).reshape(4, 4)
    print(hungarian_method(cost))