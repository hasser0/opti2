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
