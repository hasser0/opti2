from Model import Model
from IntegerProgramming import IP
import numpy as np

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



from BFS_methods import northwest_corner, minium_cost, voguels

def test():
    s=np.array([10, 15])
    d=np.array([15, 5, 5])
    c=np.array([
        [6, 7, 8],
        [15, 80, 78]
    ])
    np.array([
        [0, 5, 5],
        [15, 0, 0]
    ])
    print(voguels(s,d,c))

if __name__ == "__main__":
    test()