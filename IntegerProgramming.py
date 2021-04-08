import numpy as np
import copy
from Model import Model

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

    def cut(self, LP):
        """
        Regresa LP con una restricción adicional tipo cut
        :param LP:
        :return:
        """
        A = LP.A
        b = LP.b
        c = np.append(LP.c, np.zeros(A.shape[1] - LP.c.shape[0]))
        int_vars = np.append(self.int_vars, np.ones(A.shape[1] - LP.c.shape[0],dtype=bool))
        basis = LP.basis
        A_optime = np.linalg.inv(A[:,basis]) @ A
        b_optime = np.linalg.inv(A[:,basis]) @ b
        diff_b = b_optime - np.floor(b_optime)
        cutting_index = np.argmax(diff_b)
        A_cutting = A_optime[cutting_index]
        b_cutting = b_optime[cutting_index]
        cut_A = np.floor(A_cutting)-A_cutting
        cut_b = np.floor(b_cutting)-b_cutting
        cut_A = np.atleast_2d(cut_A)
        cut_b = np.atleast_2d(cut_b).T
        return Model(c=c, A_le=cut_A, b_le=cut_b, A_eq=A, b_eq=b), int_vars

    def branch(self, LP):
        """
        lower: branch from below
        upper: branch from above
        :param LP:
        :return:
        """
        int_rest_satisfied = self.int_rest_satisfied(LP)
        x_solution = LP.x_solution_values
        branching_index = np.argwhere(int_rest_satisfied == False)[0][0]
        x_branch_value = x_solution[branching_index]
        lower_rest = np.zeros(x_solution.shape[0])
        lower_rest[branching_index] = 1
        upper_rest = np.zeros(x_solution.shape[0])
        upper_rest[branching_index] = 1
        lower_LP = LP.add_restriction(lower_rest, "<=", np.floor(x_branch_value))
        upper_LP = LP.add_restriction(upper_rest, ">=", np.ceil(x_branch_value))
        return lower_LP, upper_LP

    def solve(self, method = "branch bound"):
        if method == "branch bound":
            return self.branch_bound()
        elif method == "cutting plane":
            return self.cutting_plane()

    def branch_bound(self):
        """
        :return: Either an OptimizedResult or None
        """
        SUCCESSFUL = 0
        better_solution = None
        better_z_value = np.inf
        LP_stack = []
        LP_stack.append(self.relaxed_LP)
        while LP_stack:
            current_LP = LP_stack.pop()
            current_sol = current_LP.solve()
            current_z = current_sol.fun
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
        return better_solution

    def cutting_plane(self):
        """
        Int restrictions satisfied | Status = 0 | Continuar algoritmo|
        T|T|    F
        T|F|    F
        F|T|    T
        F|F|    F
        :return:
        """
        SUCCESFULL = 0
        cutted_LP = copy.deepcopy(self.relaxed_LP)
        int_vars = copy.deepcopy(self.int_vars)
        current_solution = cutted_LP.solve()
        while not self.all_int_rest_satisfied(cutted_LP) and current_solution['status'] == SUCCESFULL:
            cutted_LP, self.int_vars = self.cut(cutted_LP)
            current_solution = cutted_LP.solve()
        self.int_vars = int_vars
        return current_solution