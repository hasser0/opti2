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
        # Calculate the two smallest values
        min1,min2 = np.sort(vector)[[0,1]]
        return min2-min1
    demand = demand.flatten()
    supply = supply.flatten()
    if np.sum(supply) != np.sum(demand):
        return
    tableau = np.zeros((supply.size, demand.size))
    supply_penalty = np.array([calc_penalty(row) for row in cost])
    demand_penalty = np.array([calc_penalty(col) for col in cost.T])
    while not (supply == 0).all() and not (demand == 0).all():
        entry_row = np.argmin(supply_penalty)
        entry_col = np.argmax(demand_penalty)
        entry_value = min(supply[entry_row], demand[entry_col])
        tableau[entry_row, entry_col] = entry_value
        supply[entry_row] -= entry_value
        demand[entry_col] -= entry_value
        supply_penalty[entry_row] = calc_penalty(cost[entry_row])
        demand_penalty[entry_col] = calc_penalty(cost.T[entry_col])
        if supply[entry_row] == 0:
            supply_penalty[entry_row] = np.iinfo(np.int16).max
        if demand[entry_col] == 0:
            demand_penalty[entry_col] = -1
    return tableau