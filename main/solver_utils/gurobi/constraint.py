
# from gurobipy import Model

# from main.solver_utils.constraint import ILinConstraint, ConstrSense


# from solver_utils.gurobi.expression import LinExpr


# class LinConstraint(ILinConstraint):

#     def __init__(
#         self,
#         model: Model,
#         name: str,
#         expr: LinExpr,
#         sense: ConstrSense,
#     ):
#         self.name = name
#         self.expr = expr
#         self.sense = sense








# # so one question I had was is it really needed to have model be part of the init method args
# # we could use that in add_constr method or else
# # do we need to add that method which would create temp constraint objects?
# # then I thought about same concept in Variable, we could potentialy differ the variable addition to model
# # to the add_var method.