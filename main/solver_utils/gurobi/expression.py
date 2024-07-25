
from gurobipy import LinXpr as grb_LinXpr

from solver_utils.iexpression import ILinExpr




class LinXpr(ILinExpr, grb_LinXpr):
    
    def __init__(
        self,

    ):