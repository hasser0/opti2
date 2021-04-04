import numpy as np

class IP:
    def __init__(self, relaxed_LP, int_vars):
        """
        :param integers: np.array of booleans
        :param relaxed_LP: Model LP problem
        """
        self.relaxed_LP = relaxed_LP
        self.int_vars = int_vars

    def int_rest_satisfied(self, LP):
        """
        a => b  === a&b or !a
        :param LP: an Linear Programming
        :return: boolean np.array integer restrictions satisfied in LP solution
        """
        return (self.int_vars & LP.are_int_vars) | np.logical_not(self.int_vars)

    def all_int_rest_satisfied(self, LP):
        """
        :param LP: linear programming
        :return: Are all integer restrictions satisfied
        """
        return np.all(self.int_rest_satisfied(LP))

    def branch(self, LP):
        """
        lower: branch from below
        upper: branch from above
        :param LP:
        :return:
        """
        int_rest_satisfied = self.int_rest_satisfied(LP)
        x_solution = LP.x_solution_values
        index_branch = np.argwhere(int_rest_satisfied == False)[0][0]
        x_branch_value = x_solution[index_branch]
        lower_rest = np.zeros(x_solution.shape[0])
        lower_rest[index_branch] = 1
        upper_rest = np.zeros(x_solution.shape[0])
        upper_rest[index_branch] = 1
        lower_LP = LP.add_restriction(lower_rest, "<=", np.floor(x_branch_value))
        upper_LP = LP.add_restriction(upper_rest, ">=", np.ceil(x_branch_value))
        return lower_LP, upper_LP

    def solve(self, method = "branch bound"):
        if method == "branch bound":
            return self.branch_bound()

    def branch_bound(self):
        """
        :return: Either an OptimizedResult or None
        """
        SUCCESSFUL = 0
        better_solution = None
        iteration = 1
        better_z_value = np.inf
        LP_stack = []
        LP_stack.append(self.relaxed_LP)
        while LP_stack:
            current_LP = LP_stack.pop()
            current_sol = current_LP.solve()
            current_z = current_sol.fun
            print(iteration)
            print(current_sol)
            iteration += 1
            if not current_sol.status == SUCCESSFUL:
                continue
            if current_z >= better_z_value:
                continue
            if not self.all_int_rest_satisfied(current_LP):
                lower_LP, upper_LP = self.branch(current_LP)
                LP_stack.append(lower_LP)
                LP_stack.append(upper_LP)
                continue
            better_solution = current_sol
            better_z_value = current_z
        print("")
        return better_solution