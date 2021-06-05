from Model import Model
from IntegerProgramming import IP
import numpy as np
from BFS_methods import northwest_corner, minium_cost, voguels

def main():
    A = np.array([
        [1,1],
        [9,5]
    ])
    b = np.array([
        [6],
        [45]
    ])
    c = np.array([8, 5])
    lp = Model(c=c, A_le=A, b_le=b, max=True)
    int_vars = np.array([True, True])
    ip = IP(lp, int_vars)
    #print(ip.solve("cutting plane").x)
    print(ip.solve("branch bound").x)

def test():
    s = np.array([1000, 1500, 750])
    d = np.array([2000, 500, 400, 10, 100, 240])
    c = np.array([
        [3, 20, 25, 75, 45, 0],
        [20, 15, 2, 50, 80, 0],
        [15, 2, 10, 40, 60, 0]
    ])
    e = np.array([
        [1000, 0, 0, 0, 0, 0],
        [1000, 0, 400, 0, 0, 100],
        [0, 500, 0, 10, 100, 140]
    ])
    print(voguels(s,d,c))

if __name__ == "__main__":
    test()