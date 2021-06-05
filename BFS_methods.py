import numpy as np
def northwest_corner(supply, demand):
    demand = demand.flatten()
    supply = supply.flatten()
    if np.sum(supply) != np.sum(demand):
        return
    i, j = 0 , 0
    m = supply.size
    n = demand.size
    tableau = np.zeros((m,n))
    while i < m and j < n:
        tableau[i, j] = np.min([supply[i], demand[j]])
        supply[i] -= tableau[i, j]
        demand[j] -= tableau[i, j]
        if demand[j] == 0:
            j += 1
            continue
        i += 1
    return tableau

def minium_cost(supply, demand, cost):
    demand = demand.flatten()
    supply = supply.flatten()
    if np.sum(supply) != np.sum(demand):
        return
    tableau = np.zeros((supply.size, demand.size))
    while not (supply == 0).all() and not (demand == 0).all():
        entry_row, entry_col = np.unravel_index(cost.argmin(), cost.shape)
        cost[entry_row, entry_col] = np.iinfo(np.int16).max
        entry_value = min(supply[entry_row], demand[entry_col])
        tableau[entry_row, entry_col] = entry_value
        supply[entry_row] -= entry_value
        demand[entry_col] -= entry_value
    return tableau

def voguels(supply, demand, cost):
    def calc_penalty(vector):
        sorted = np.sort(vector)
        sorted = sorted[sorted > 0]
        if sorted.size <= 1:
            return 0
        min1, min2 = sorted[[0, 1]]
        return min2-min1

    demand = demand.flatten()
    supply = supply.flatten()
    if np.sum(supply) != np.sum(demand):
        return
    tableau = np.zeros((supply.size, demand.size))
    supply_penalty = np.array([calc_penalty(row) for row in cost])
    demand_penalty = np.array([calc_penalty(col) for col in cost.T])
    while not (supply == 0).all() and not (demand == 0).all():
        entry_row = np.argmax(supply_penalty)
        entry_col = np.argmax(demand_penalty)
        if supply_penalty[entry_row] > demand_penalty[entry_col]:
            row = cost[entry_row, :]
            valid_index = np.where((row >= 0) & (demand_penalty > 0))[0]
            entry_col = valid_index[row[valid_index].argmin()]
        else:
            col = cost[:, entry_col]
            valid_index = np.where((col >= 0) & (supply_penalty >= 0))[0]
            entry_row = valid_index[col[valid_index].argmin()]
        entry_value = min(supply[entry_row], demand[entry_col])
        tableau[entry_row, entry_col] = entry_value
        supply[entry_row] -= entry_value
        demand[entry_col] -= entry_value
        cost[entry_row, entry_col] = -1
        if supply[entry_row] == 0:
            supply_penalty[entry_row] = -1
            for index, col in enumerate(cost.T):
                if demand_penalty[index] == -1:
                    continue
                demand_penalty[index] = calc_penalty(col[supply_penalty != -1])
        if demand[entry_col] == 0:
            demand_penalty[entry_col] = -1
            for index, row in enumerate(cost):
                if supply_penalty[index] == -1:
                    continue
                supply_penalty[index] = calc_penalty(row[demand_penalty != -1])
    return tableau
