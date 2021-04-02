from scipy.optimize import linprog
from scipy.optimize import OptimizeResult

class Model:
    def __init__(self):
        """
        le: less equals
        eq: equals
        """
        self.A_le = None
        self.A_eq = None
        self.b_le = None
        self.b_eq = None
        self.c = None
        self.integer = None

    def iteration(self, result):
        print("hola")

    def solve(self):
        return linprog(c=self.c,
                A_ub=self.A_le,
                A_eq=self.A_eq,
                b_ub=self.b_le,
                b_eq=self.b_eq,
                callback=self.iteration,
                method='revised simplex')