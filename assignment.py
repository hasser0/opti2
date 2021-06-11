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
        if r_max >= c_max:
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
    size = cost.shape[0]
    min_row = cost.min(axis=1).reshape(size,1)
    cost = cost - min_row
    min_col = cost.min(axis=0)
    cost = cost - min_col
    ones = np.ones(size)
    while True:
        cross = (cost == 0).astype(int)
        zeros_col = cross.sum(axis=0)
        zeros_row = cross.sum(axis=1)
        x_rows, x_cols, crossed = crossed_rows_columns(zeros_row, zeros_col, cross)
        if crossed == size:
            cross = (cost == 0).astype(int)
            return cross
        nx_rows, nx_cols = np.logical_not(x_rows), np.logical_not(x_cols)
        reduced_matrix = nx_cols & nx_rows.reshape(-1, 1)
        cover_twice_matrix = x_cols & x_rows.reshape(-1,1)
        k = cost[reduced_matrix].min()
        cost[reduced_matrix] -= 1
        cost[cover_twice_matrix] += 1

if __name__ == '__main__':
    cost = np.array([
        [47, 50, 57, 57, 0],
        [48, 52, 52, 62, 0],
        [50, 55, 54, 59, 0],
        [52, 54, 55, 60, 0],
        [51, 51, 53, 58, 0]
    ])
    print(hungarian_method(cost))