import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog

class GraphLinearProgram:
    def __init__(self, df):
        # Determine if we are minimizing or maximizing
        optimize = df.iloc[0, -1]
        self.minimize = (optimize == "min")

        # Objective function coefficients
        self.c = np.array(df.iloc[0, :-2], dtype=float)
        # Constraint coefficients
        self.A = np.array(df.iloc[1:-1, :-2], dtype=float)
        # Constraint bounds
        self.b = np.array(df.iloc[1:-1, -1], dtype=float)
        # Constraint signs
        self.sign_constraints = np.array(df.iloc[1:-1, -2])
        # Variable signs
        self.sign_vars = np.array(df.iloc[-1, :-2])

        # Number of variables and constraints
        self.num_variables = self.c.shape[0]
        self.num_constraints = self.b.shape[0]

    
    def is_valid(self):
        return self.num_variables == 2
    
    def find_intersection(self, A1, b1, A2, b2):
        A = np.array([A1, A2])
        b = np.array([b1, b2])
        
        if np.linalg.det(A) == 0:
            return None
        
        x, y = np.linalg.solve(A, b)
        
        return [x, y]
    
    def is_feasible(self, point):
        # Check if the point lies within the feasible region
        for i in range(self.num_constraints):
            if self.sign_constraints[i] == "<=" and not np.isclose(self.A[i] @ point, self.b[i], atol=1e-9) and not ((self.A[i] @ point) <= self.b[i]):
                return False
            elif self.sign_constraints[i] == ">=" and not np.isclose(self.A[i] @ point, self.b[i], atol=1e-9) and not ((self.A[i] @ point) >= self.b[i]):
                return False
            elif self.sign_constraints[i] == "=" and not np.isclose((self.A[i] @ point), self.b[i], atol=1e-9):
                return False

        if self.sign_vars[0] == "<=" and not (point[0] <= 0):
            return False
        elif self.sign_vars[0] == ">=" and not (point[0] >= 0):
            return False
        if self.sign_vars[1] == "<=" and not (point[1] <= 0):
            return False
        elif self.sign_vars[1] == ">=" and not (point[1] >= 0):
            return False

        return True

    def feasible_points(self):
        A_list = self.A.copy()
        b_list = self.b.copy()

        if self.sign_vars[0] == "<=":
            A_list = np.vstack([A_list, [1, 0]]) 
            b_list = np.hstack([b_list, 0])  
        elif self.sign_vars[0] == ">=":
            A_list = np.vstack([A_list, [1, 0]]) 
            b_list = np.hstack([b_list, 0]) 

        if self.sign_vars[1] == "<=":
            A_list = np.vstack([A_list, [0, 1]]) 
            b_list = np.hstack([b_list, 0]) 
        elif self.sign_vars[1] == ">=":
            A_list = np.vstack([A_list, [0, 1]]) 
            b_list = np.hstack([b_list, 0]) 

        self.feasible_points = []
        for i in range(len(A_list) - 1):
            for j in range(i + 1, len(A_list)):
                intersection_point = self.find_intersection(A_list[i], b_list[i], A_list[j], b_list[j])
                if intersection_point is not None and self.is_feasible(intersection_point):
                    self.feasible_points.append(intersection_point)

    def make_grid(self):

        # Draw axes
        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)
        size = 10
        if len(self.feasible_points) != 0:
            self.x_max = np.max(np.array([point[0] for point in self.feasible_points])).astype(int) + size
            self.y_max = np.max(np.array([point[1] for point in self.feasible_points])).astype(int) + size
            self.x_min = np.min(np.array([point[0] for point in self.feasible_points])).astype(int) - size
            self.y_min = np.min(np.array([point[1] for point in self.feasible_points])).astype(int) - size
        else:
            self.x_max = size
            self.y_max = size
            self.x_min = -size
            self.y_min = -size

        plt.xticks(np.arange(self.x_min,self.x_max, 2))  
        plt.yticks(np.arange(self.y_min,self.y_max, 2)) 
        plt.ylim((self.x_min, self.x_max))
        plt.ylim((self.y_min,self.y_max))
        # plt.xlabel('x1')
        # plt.ylabel('x2')
        plt.grid(True)
    
    def draw_constraints(self):
        x = np.linspace(self.x_min, self.x_max, 800)
        d = np.linspace(self.x_min, self.x_max, 800)
        x_mesh, y_mesh = np.meshgrid(d, d)
        constraints = []
        for i in range(self.num_constraints):
            y = (self.b[i] - self.A[i, 0] * x) / self.A[i, 1]
            plt.plot(x, y, label=f'{self.A[i, 0]}x1 + {self.A[i, 1]}x2 {self.sign_constraints[i]} {self.b[i]}', zorder = 1)
            if self.sign_constraints[i] == "<=":
                constraints.append((self.A[i, 0] * x_mesh + self.A[i, 1] * y_mesh) <= self.b[i])
            elif self.sign_constraints[i] == ">=":
                constraints.append((self.A[i, 0] * x_mesh + self.A[i, 1] * y_mesh) >= self.b[i])
            elif self.sign_constraints[i] == "=":
                constraints.append((self.A[i, 0] * x_mesh + self.A[i, 1] * y_mesh) == self.b[i])

        if self.sign_vars[0] == "<=":
            constraints.append(x_mesh <= 0)
        elif self.sign_vars[0] == ">=":
            constraints.append(x_mesh >= 0)

        if self.sign_vars[1] == "<=":
            constraints.append(y_mesh <= 0)
        elif self.sign_vars[1] == ">=":
            constraints.append(y_mesh >= 0)

        feasible_region = np.logical_and.reduce(constraints)
        plt.imshow(feasible_region.astype(int), 
                   extent=(x.min(), x.max(), d.min(), d.max()), 
                   origin="lower", cmap="Greys", alpha=0.3, zorder = 0)
        
        for point in self.feasible_points:
            plt.scatter(point[0], point[1], color='black', marker='o', s=24, zorder = 3)


    def optimize(self):
        # Prepare bounds for variables (x1, x2)

        bounds = []
        for var_sign in self.sign_vars:
            if var_sign == "<=":
                bounds.append((None, 0))
            elif var_sign == ">=":
                bounds.append((0, None))
            else:
                bounds.append((None, None))
        
        # Adjust for constraint types
        A_ub = []
        b_ub = []
        A_eq = []
        b_eq = []
        
        for i in range(self.num_constraints):
            if self.sign_constraints[i] == "<=":
                A_ub.append(self.A[i])
                b_ub.append(self.b[i])
            elif self.sign_constraints[i] == ">=":
                A_ub.append(-self.A[i])
                b_ub.append(-self.b[i])
            elif self.sign_constraints[i] == "=":
                A_eq.append(self.A[i])
                b_eq.append(self.b[i])

        # Convert to numpy arrays
        A_ub = np.array(A_ub) if A_ub else None
        b_ub = np.array(b_ub) if b_ub else None
        A_eq = np.array(A_eq) if A_eq else None
        b_eq = np.array(b_eq) if b_eq else None

        # Solve the linear program
        c = self.c
        if not self.minimize:
            c = -c

        res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

        return res
    
    def slide_target_function(self, optimal_point):
        x = np.linspace(self.x_min, self.x_max, 400)
        # lcm_value = np.lcm.reduce(self.c.astype(int))  # Convert coefficients to integers

        # y_lcm = (lcm_value - self.c[0]*x) / self.c[1] 
        # plt.plot(x, y_lcm, label=f'z = {self.c[0]}x1 + {self.c[1]}x2 = {lcm_value}', linestyle="--", zorder = 2)

        y_origin = (-self.c[0]*x) / self.c[1] 
        plt.plot(x, y_origin, label=f'z = {self.c[0]}x1 + {self.c[1]}x2 = 0', linestyle="--", zorder = 2, linewidth = 1.5)

        slope = -self.c[0] / self.c[1]
        x_opt, y_opt = optimal_point
        y_optimal = slope * x + (y_opt - slope * x_opt)
        plt.plot(x, y_optimal, label=f'z = {self.c[0]}x1 + {self.c[1]}x2 = {self.c[0]*x_opt + self.c[1]*y_opt}', linestyle='--', zorder=2, linewidth = 1.5)
    
    def show_result(self, res):
        check = None
        if res.success:
            if not self.minimize:
                optimal_value = np.abs(res.fun)
            else:
                optimal_value = res.fun
            optimal_point = res.x

            # Check for infinite solutions by evaluating other feasible points
            feasible_points = [point for point in self.feasible_points if not np.allclose(point, optimal_point, atol=1e-9)]
            solutions = [optimal_point]
            is_inf = False
            for point in feasible_points:
                if(self.c[0]*point[0] + self.c[1]*point[1] == optimal_value):
                    solutions.append(point)
                    is_inf = True
                    break
            if is_inf:
                check = 2
                plt.plot([solutions[0][0],solutions[1][0]],[solutions[0][1],solutions[1][1]], '--', label='Optimal Line', lw = 2.0, color = 'blue', zorder=4)
                for point in solutions:
                    plt.scatter(point[0], point[1], color='blue', marker='o', s=24, zorder=4)
            else:
                check = 1
                self.slide_target_function(optimal_point)
                plt.scatter(optimal_point[0], optimal_point[1], color='blue', marker='*', s=100, label='Optimal Point', zorder=4)

            self.solutions = [np.round(solution,2) for solution in solutions]
            self.optimal_value = round(optimal_value,2)


                
        else:
            if res.status == 2:
                check = 0 # Vô nghiệm
                self.optimal_value = np.inf if self.minimize else -np.inf
            elif res.status == 3:
                check = 3 # Unbounded
                self.optimal_value = -np.inf if self.minimize else np.inf


        self.status = check

    def plot_graph(self):
        fig, ax = plt.subplots(figsize=(7, 6))
        if not self.is_valid():
            ax.set_title("CAN'T USE GRAPHICAL METHOD FOR MORE THAN 2 VARIABLES", fontweight='bold', fontsize=13, color = 'red')
            ax.axis('off')  # Hide axes
            return fig
        
        self.feasible_points()
        self.make_grid()
        self.draw_constraints()
        
        # Get optimal solution
        res = self.optimize()
        self.show_result(res)

        ax.legend()
        ax.set_title('Graphical Linear Programming Solver', fontweight='bold', fontsize=14)
        ax.margins(x=0)
        return fig
