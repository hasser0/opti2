from scipy.optimize import linprog
import numpy as np

class Model:
    def __init__(self, c, A_le=None, A_eq=None, b_le=None, b_eq=None):
        """
        le: less equals
        eq: equals
        """
        self.A_le = A_le
        self.A_eq = A_eq
        self.b_le = b_le
        self.b_eq = b_eq
        self.c = c
        self.result = None

    def iteration(self, result):
        pass

    @property
    def is_integer(self):
        """
        :return: Whether solution to LP has integer values or not
        """
        x = self.solution
        x = np.round(x, decimals=6)
        return (x-x.astype(int)) == 0

    def add_restriction(self, restriction, sign, b):
        c = self.c
        if sign == '<=':
            A_le = np.append(self.A_le, [restriction], axis=0)
            b_le = np.append(self.b_le, [[b]], axis=0)
            A_eq = self.A_eq
            b_eq = self.b_eq
        elif sign == '=':
            A_eq = np.append(self.A_eq, [restriction], axis=0)
            b_eq = np.append(self.b_eq, [[b]], axis=0)
            A_le = self.A_le
            b_le = self.b_le
        elif sign == '>=':
            return self.add_restriction(restriction=restriction*-1, sign='<=' ,b=b*-1)
        return Model(A_le=A_le, A_eq=A_eq, b_le=b_le, b_eq=b_eq,c=c)

    def solveLP(self):
        if self.result is None:
            self.result = linprog(c=self.c,
                                    A_ub=self.A_le,
                                    A_eq=self.A_eq,
                                    b_ub=self.b_le,
                                    b_eq=self.b_eq,
                                    callback=self.iteration,
                                    method='revised simplex')
        return self.result

    @property
    def solution(self):
        return self.solveLP().x

