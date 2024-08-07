
# from typing import List, Union, Tuple, Dict
# from gurobipy import LinEXpr as grb_LinExpr

# from main.solver_utils.expression import ILinExpr
# from solver_utils.gurobi.variable import Variable



# class LinExpr(ILinExpr):
    
#     def __init__(
#         self,
#         name: str,
#         variables: List[Union[Variable, "LinExpr"]],
#         coefs: List[float],
#         const: float,
#     ):
#         self.name = name
#         self.variables = variables
#         self.coefs = coefs
#         self.const = const

#         self._var_coefs: Dict[Variable, float] = self._get_expr_variables()
#         self._expr_coefs: Dict["LinExpr", float] = self._get_expr_expressions()
#         self._net_variable_ceofs: Dict[Variable, float] = self._get_expr_net_variables()

#         self._grb_expr: grb_LinExpr = grb_LinExpr(const) + grb_LinExpr(list(self._net_variable_ceofs.values()), list(self._net_variable_ceofs.keys()))
        

#     def _get_expr_variables(
#         self,
#     ) ->  Dict[Variable, float]:
        
#         var_coef_dict = {
#             variable: coef for variable,coef in zip(self.variables,self.coefs) if isinstance(variable, Variable)
#         }
#         return var_coef_dict

#     def _get_expr_expressions(
#         self,
#     ) -> Dict["LinExpr", float]:
#         var_coef_dict = {
#             variable: coef for variable,coef in zip(self.variables,self.coefs) if isinstance(variable, LinExpr)
#         }
#         return var_coef_dict

#     def _get_expr_net_variables(
#         self,
#     ) -> Dict[Variable, float]:
#         return _traverse (self)

        


# # i guess the approach that I am taking does not allow to directly be using 
# # the solver interface(gurobi) within the code, like having Isolver directly let gurobi API 
# # to create LinXpr, etc

# # Will mypy be okay, for further narrowing down an Attribute of the Base/Contract class




# def _traverse(expr: LinExpr, parenet_coef: float = 1) -> Dict[Variable, float]:
#     result = {}
#     def _update_result(var: Variable, coef: float):
#         if var in result:
#             result[var] +=coef
#         else:
#             result[var] = coef

#     for var, coef in zip(expr.variables, expr.coefs):
#         total_coef = coef * parenet_coef
#         if isinstance(var, Variable):
#             _update_result(var, total_coef)
#         elif isinstance(var, LinExpr):
#             nested_result = _traverse(var, total_coef)
#             for nested_var, nested_coef in nested_result.items():
#                 _update_result(var, nested_coef)
    
#     return result