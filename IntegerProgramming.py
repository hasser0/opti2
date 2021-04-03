import numpy as np

class IP:
    def __init__(self, relaxed_LP, integers):
        """
        :param integers: np.array of booleans
        :param relaxed_LP: Model LP problem
        """
        self.relaxed_LP = relaxed_LP
        self.integers = integers

    def int_rest_satisfied(self):
        pass

    def branch_bound(self, relaxed_IP):
        """
        :param relaxed_IP: is a relaxed integer programming model type Model
        :return: Either an OptimizedResult or None
        """
        solution = None
        z_value = np.inf
        stack = []
        stack.append(relaxed_IP)
        while stack:
            cur_LP = stack.pop()
            cur_sol = cur_LP.solveLP()  #OptimizeResult
            cur_z = cur_sol.fun #z_value of current LP solution
            if cur_sol.status != 0:
                continue
            if cur_z >= z_value:
                continue
            if not self.int_rest_satisfied():
                #choose first variable no integer
                #create two restrictions rest1, rest2
                sub_LP1 = cur_LP.add_restriction(rest1)
                sub_LP2 = cur_LP.add_restriction(rest2)
                stack.append(sub_LP1)
                stack.append(sub_LP2)
                continue
            solution = cur_sol
        return solution