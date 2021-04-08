from Model import Model
from IntegerProgramming import IP
import numpy as np
import timeit

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

if __name__ == "__main__":
    main()