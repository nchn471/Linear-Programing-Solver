import numpy as np
import pandas as pd

class SimplexLinearProgram:
    def __init__(self, df):
        # Tìm max hay min
        optimize = df.iloc[0, -1]
        self.minimize = (optimize == "min")

        # Hàm mục tiêu
        self.c = np.array(df.iloc[0, :-2], dtype=float)
        # Hệ số ràng buộc
        self.A = np.array(df.iloc[1:-1, :-2], dtype=float)
        # Giới hạn ràng buộc
        self.b = np.array(df.iloc[1:-1, -1], dtype=float)
        # Dấu ràng buộc dt/bdt <= >= =
        self.sign_constraints = np.array(df.iloc[1:-1, -2])
        # Dấu ràng buộc biến
        self.sign_vars = np.array(df.iloc[-1, :-2])

        # Số biến, số ràng buộc
        self.num_variables = self.c.shape[0]
        self.num_constraints = self.b.shape[0]
        # Số biến cần tạo mới
        self.num_new_variable = 0

    def to_normal_form(self):
        # Chuyển hàm mục tiêu thành dạng tối thiểu hóa
        if not self.minimize:
            self.c = -self.c

        # Xử lý dấu của các biến
        for i in range(self.num_variables - self.num_new_variable):
            if self.sign_vars[i] == "<=":  # xi <= 0
                self.c[i] = -self.c[i]
                self.A[:, i] = -self.A[:, i]
                self.sign_vars[i] = ">="
            elif self.sign_vars[i] == "free":  # xi tự do
                self.num_variables += 1
                self.num_new_variable += 1
                self.c = np.append(self.c, -self.c[i])
                new_col = -np.array([self.A[:, i]]).T
                self.A = np.hstack((self.A, new_col))
                self.sign_vars[i] = ">="
                self.sign_vars = np.append(self.sign_vars, ">=")

        # Xử lý dấu của các ràng buộc
        for i in range(self.num_constraints):
            if self.sign_constraints[i] == ">=":  # >=
                self.A[i, :] = -self.A[i, :]
                self.b[i] = -self.b[i]
                self.sign_constraints[i] = "<="
            elif self.sign_constraints[i] == "=":  # =
                self.num_constraints += 1
                self.sign_constraints[i] = "<="
                new_row = -np.array([self.A[i, :]])
                self.A = np.vstack((self.A, new_row))
                self.b = np.append(self.b, -self.b[i])
                self.sign_constraints = np.append(self.sign_constraints, "<=")

    def to_table_form(self):
        # Tạo bảng
        self.to_normal_form()
        tableau = np.vstack((np.hstack((self.c, np.zeros(self.num_constraints + 1))),
                             np.hstack((self.A, np.eye(self.num_constraints), self.b.reshape(-1, 1)))))
        self.sign_vars = np.append(self.sign_vars, [">="] * self.num_constraints)
        return tableau

    def get_method(self):
        if np.any(self.b < 0):
            return 2  # 2 pha (two-phase method)
        elif np.any(self.b == 0):
            return 1  # Xoay Bland (Bland's rule)
        else:
            return 0  # Xoay đơn hình (Dantzig's rule)

    def choose_pivot(self, tableau, method):
        pivot_col, pivot_row = None, None
        if method == 'dantzig':
            # Chọn cột pivot theo phương pháp Dantzig
            pivot_col = np.argmin(tableau[0, :-1])
            if tableau[0, pivot_col] >= 0:
                return 1, pivot_row, pivot_col
            
        elif method == 'bland':
            # Chọn cột pivot theo phương pháp Bland
            for j in range(self.num_variables):
                if tableau[0, j] < 0:
                    pivot_col = j
                    break
            if pivot_col is None:
                return 1, pivot_row, pivot_col

        min_ratio = np.inf
        for i in range(1, self.num_constraints + 1):
            if tableau[i, pivot_col] > 0:
                ratio = tableau[i, -1] / tableau[i, pivot_col]
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row = i

        if pivot_row is None:
            return 0, pivot_row, pivot_col
        
        return -1, pivot_row, pivot_col

    def rotate(self, tableau, pivot_row, pivot_col):
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element
        for i in range(tableau.shape[0]):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]
        return tableau

    def simplex_method(self, tableau, method='dantzig'):
        iterations = []
        pivot_indices = []
        nit = 0

        while True:
            iterations.append(tableau.copy())
            if nit > 10 and np.array_equal(tableau, iterations[-2]):  
                check = 2
                break

            check, pivot_row, pivot_col = self.choose_pivot(tableau, method)
            if check != -1:
                break

            pivot_indices.append([pivot_row, pivot_col])
            tableau = self.rotate(tableau, pivot_row, pivot_col)
            nit += 1

        return check, iterations, pivot_indices

    
    def update_objective_function(self, tableau):
        # Lặp qua tất cả các cột trừ cột cuối cùng (hệ số tự do)
        for j in range(tableau.shape[1] - 1):
            # Kiểm tra nếu hệ số của biến trong hàm mục tiêu khác không
            if tableau[0, j] != 0:
                # Tìm hàng có biến cơ bản trong cột j
                pivot_row = None
                for i in range(1, tableau.shape[0]):
                    if tableau[i, j] == 1 and all(tableau[k, j] == 0 for k in range(1, tableau.shape[0]) if k != i):
                        pivot_row = i
                        break

                # Nếu tìm thấy hàng pivot, cập nhật hàm mục tiêu
                if pivot_row is not None:
                    coef = tableau[0, j]
                    for k in range(tableau.shape[1]):
                        tableau[0, k] -= coef * tableau[pivot_row, k]

        # Đặt hệ số các biến cơ bản vừa được thay thế về 0
        for j in range(tableau.shape[1] - 1):
            pivot_row = None
            for i in range(1, tableau.shape[0]):
                if tableau[i, j] == 1 and all(tableau[k, j] == 0 for k in range(1, tableau.shape[0]) if k != i):
                    pivot_row = i
                    break
            if pivot_row is not None:
                tableau[0, j] = 0
    


    def two_phase_method(self, tableau):
        tableau_p1 = np.zeros((tableau.shape[0], tableau.shape[1]+1))
        tableau_p1[0, -2] = 1
        tableau_p1[1:, -2] = -np.ones((tableau.shape[0]-1,1)).ravel()
        tableau_p1[1:,:tableau.shape[1]-1] = tableau[1:, :tableau.shape[1]-1]
        tableau_p1[1:, -1] = tableau[1:, -1]

        pivot_row = None
        pivot_col = tableau_p1.shape[1] - 2
        minBi = 0
        for i in range(tableau_p1.shape[0]):
            if tableau_p1[i,-1] < minBi:
                minBi = tableau_p1[i,-1]
                pivot_row = i
        tableau_p1 = self.rotate(tableau_p1, pivot_row, pivot_col)

        _, iterations_p1, pivot_indices_p1 = self.simplex_method(tableau_p1, 'dantzig')

        if np.any(tableau_p1[0, :-2] != 0):
            return 2, iterations_p1, pivot_indices_p1, None, None

        tableau[1:, :tableau.shape[1]-1] = tableau_p1[1:, :tableau.shape[1]-1]
        tableau[1:, -1] = tableau_p1[1:, -1]

        self.update_objective_function(tableau)

        check, iterations_p2, pivot_indices_p2 = self.simplex_method(tableau, 'dantzig')

        return check, iterations_p1, pivot_indices_p1, iterations_p2, pivot_indices_p2
    
    def extract_solution(self, tableau):
        solution = np.zeros(self.num_variables)
        for j in range(self.num_variables):
            pivot_row = None
            for i in range(1, tableau.shape[0]):
                if tableau[i, j] == 1 and all(tableau[k, j] == 0 for k in range(1, tableau.shape[0]) if k != i):
                    pivot_row = i
                    break
            if pivot_row is not None:
                solution[j] = tableau[pivot_row, -1]
        return solution
    
    def get_optimal(self,tableau, check):
        self.optimal_point = None
        if check == 0:
            self.optimal_value = -np.inf if self.minimize else np.inf

        elif check == 2:
            self.optimal_value = -np.inf if self.minimize else np.inf
        else:
            optimal_value = np.round(tableau[0,-1],2)
            self.optimal_value = -optimal_value if self.minimize else optimal_value

            self.optimal_point = self.extract_solution(tableau)
            if len(self.optimal_point) > 2:
                self.optimal_point = None
        
    
    def run_simplex(self,tableau,method):
        if method == 0:
            self.check, self.iterations, self.pivot_indices = self.simplex_method(tableau, method='dantzig')
        elif method == 1:
            self.check, self.iterations, self.pivot_indices = self.simplex_method(tableau, method='bland')

    def run_twophase(self,tableau,method):
        self.check, self.iterations_p1, self.pivot_indices_p1, self.iterations_p2, self.pivot_indices_p2 =  self.two_phase_method(tableau)

    
    def run_program(self):
        tableau = self.to_table_form()
        self.method = self.get_method()

        if self.method !=2:
            self.run_simplex(tableau,self.method)
        else:
            self.run_twophase(tableau,self.method)
        
        self.get_optimal(tableau, self.check)
