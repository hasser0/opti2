from scipy.optimize import linprog
import numpy as np

class Model:
    def __init__(self, c, A_le=None, A_eq=None, b_le=None, b_eq=None, max = False):
        """
        le: less equals
        eq: equals
        """
        self.A_le = A_le
        self.A_eq = A_eq
        self.b_le = b_le
        self.b_eq = b_eq
        self.c = c
        if max == True:
            self.c = c * -1
        self.optimize_result = None

    def iteration(self, optimize_result):
        pass

    @property
    def are_int_vars(self):
        """
        :return: Whether solution to LP has integer values or not
        """
        x_sol_values = self.x_solution_values
        x_sol_values = np.round(x_sol_values, decimals=6)
        return (x_sol_values-x_sol_values.astype(int)) == 0

    def add_restriction(self, A_new_restriction, sign, b_new_restriction):
        """
        Add model with new restriction
        :param A_new_restriction:
        :param sign:
        :param b_new_restriction:
        :return:
        """
        c = self.c
        A_le = self.A_le
        b_le = self.b_le
        A_eq = self.A_eq
        b_eq = self.b_eq
        if A_le is None and sign == '<=':
            A_le = np.array([])
            b_le = np.array([])
        elif A_eq is None and sign == '=':
            A_eq = np.array([])
            b_eq = np.array([])
        if sign == '<=':
            A_le = np.append(A_le, [A_new_restriction], axis=0)
            b_le = np.append(b_le, [[b_new_restriction]], axis=0)
        elif sign == '=':
            A_eq = np.append(A_eq, [A_new_restriction], axis=0)
            b_eq = np.append(b_eq, [[b_new_restriction]], axis=0)
        elif sign == '>=':
            return self.add_restriction(A_new_restriction=A_new_restriction * -1,
                                        sign='<=', b_new_restriction=b_new_restriction * -1)
        return Model(A_le=A_le, A_eq=A_eq, b_le=b_le, b_eq=b_eq, c=c)

    def solve(self):
        if self.optimize_result is None:
            self.optimize_result = linprog(c=self.c,
                                           A_ub=self.A_le,
                                           A_eq=self.A_eq,
                                           b_ub=self.b_le,
                                           b_eq=self.b_eq,
                                           callback=self.iteration,
                                           method='revised simplex')
        return self.optimize_result

    @property
    def x_solution_values(self):
        return self.solve().x

    @property
    def A(self):
        return self.solve()['A_aumented']

    @property
    def b(self):
        return np.atleast_2d(self.solve()['b_aumented']).T

    @property
    def basis(self):
        return self.solve()['basis']