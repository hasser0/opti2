import numpy as np

class IP:
    def __init__(self, relaxed_LP, int_vars):
        """
        :param integers: np.array of booleans
        :param relaxed_LP: Model LP problem
        """
        self.relaxed_LP = relaxed_LP
        self.int_vars = int_vars

    def integer_satisfied(self, LP):
        """
        a => b  === a&b or !a
        :param LP: an Linear Programming
        :return: boolean np.array integer restrictions satisfied in LP solution
        """
        return (self.int_vars & LP.is_integer) | np.logical_not(self.int_vars)

    def all_integer_satisfied(self, LP):
        """
        :param LP: linear programming
        :return: Are all integer restrictions satisfied
        """
        return np.all(self.integer_satisfied(LP))

    def branch(self, LP):
        int_sat = self.integer_satisfied(LP)
        solution = LP.solution
        index_branch = np.argwhere(int_sat == False)[0][0]
        value_branch = solution[index_branch]
        lower_rest = np.zeros(solution.shape[0])
        lower_rest[index_branch] = 1
        upper_rest = np.zeros(solution.shape[0])
        upper_rest[index_branch] = 1
        lower_LP = LP.add_restriction(lower_rest, "<=", np.floor(value_branch))
        upper_LP = LP.add_restriction(upper_rest, ">=", np.ceil(value_branch))
        return lower_LP, upper_LP

    def solve(self, method = "branch bound"):
        if method == "branch bound":
            return self.branch_bound()

    def branch_bound(self):
        """
        :return: Either an OptimizedResult or None
        """
        solution = None
        iteration = 1
        z_value = np.inf
        stack = []
        stack.append(self.relaxed_LP)
        while stack:
            cur_LP = stack.pop()
            cur_sol = cur_LP.solveLP()  #OptimizeResult
            cur_z = cur_sol.fun #z_value of current LP solution
            print(iteration)
            print(cur_sol)
            iteration+=1
            if cur_sol.status != 0:
                continue
            if cur_z >= z_value:
                continue
            if not self.all_integer_satisfied(cur_LP):
                lower_LP, upper_LP = self.branch(cur_LP)
                stack.append(lower_LP)
                stack.append(upper_LP)
                continue
            solution = cur_sol
            z_value = cur_z
        print("")
        return solution