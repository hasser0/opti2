from Model import Model
import numpy as np
if __name__ == '__main__':
    A_le = np.array([[3, 4],
                     [5, 2]])
    b_le = np.array([[10],
                     [12]])
    c = np.array([-4, -3])
    m = Model()
    m.A_le = A_le
    m.b_le = b_le
    m.c = c
    print(m.solve())

