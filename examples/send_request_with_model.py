
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from optclient.solver_utils.ortools.client import Client
from optclient.solver_utils.ortools.solver import Solver

from optclient.solver_utils.variable import Variable, VarType
from optclient.solver_utils.constraint import LinConstraint, ConstrSense
from optclient.solver_utils.expression import LinExpr
from optclient.solver_utils.isolver import OptSense


def create_sample_problem():
    solver = Solver(Client(target="localhost:50051"))

    # Define variables
    x1 = Variable(name="x1", vtype=VarType.real, lower_bound=0.0)
    x2 = Variable(name="x2", vtype=VarType.real, lower_bound=0.0)
    x3 = Variable(name="x3", vtype=VarType.real, lower_bound=0.0)

    solver.add_variable(x1)
    solver.add_variable(x2)
    solver.add_variable(x3)

    # Define constraints
    xp1 = LinExpr([x1, x2, x3], [1.0, 1.0, 1.0], name="c1")
    xp2 = LinExpr([x1, x2, x3], [10.0, 4.0, 5.0], name="c2")
    xp3 = LinExpr([x1, x2, x3], [2.0, 2.0, 6.0], name="c3")

    c1 = LinConstraint(expr=xp1, rhs=100.0, name="c1", sense=ConstrSense.leq)
    c2 = LinConstraint(expr=xp2, rhs=600.0, name="c2", sense=ConstrSense.leq)
    c3 = LinConstraint(expr=xp3, rhs=300.0, name="c3", sense=ConstrSense.leq)

    solver.add_linear_constraint(c1)
    solver.add_linear_constraint(c2)
    solver.add_linear_constraint(c3)

    objective_expr = LinExpr([x1, x2, x3], [10.0, 6.0, 4.0], name="objective")
    solver.add_objective(objective_expr, name="objective")

    solver.solve_model(sense=OptSense.maximize, options={})

    x_1 = solver.get_variable_value(x1)
    x_2 = solver.get_variable_value(x2)
    x_3 = solver.get_variable_value(x3)

    o1 = solver.get_objective_value()

    print(f"Optimal values: x1={x_1}, x2={x_2}, x3={x_3}")
    print(o1)
    print(xp3.value)
    print(xp2.value)


    
if __name__ == "__main__":
    create_sample_problem()
    # send_and_solve_problem(create_sample_problem())