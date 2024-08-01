from dataclasses import dataclass, field
from typing import List, Union, Dict, TypeVar, Tuple

from main.solver_utils.variable import Variable


@dataclass(frozen=True)
class LinExpr:
    name: str
    variables: List[Union[Variable, "LinExpr"]]
    coefs: List[float]
    const: float

    _net_var_coefs: Dict[Variable, float] = field(init=False)
    _net_const: float = field(init=False)

    @property
    def var_coefs(self) -> Dict[Variable, float]:
        return self._get_expr_variables()

    @property
    def expr_coefs(self) -> Dict["LinExpr", float]:
        return  self._get_expr_expressions()

    @property
    def net_variable_coefs(self) -> Dict[Variable, float]:
        return self._get_expr_net_variables()
    
    @property
    def net_constant(self) -> float:
        return self._get_expr_net_constant()
  

    @property
    def value(self) -> float:
        vars_dot_ceof: List[float] = [
            variable.value * coef for variable, coef in self.net_variable_coefs.items()
        ]
        return sum(vars_dot_ceof)


    def _get_expr_variables(
        self,
    ) ->  Dict[Variable, float]:
        
        var_coef_dict = {
            variable: coef for variable,coef in zip(self.variables,self.coefs) if isinstance(variable, Variable)
        }
        return var_coef_dict

    def _get_expr_expressions(
        self,
    ) -> Dict["LinExpr", float]:
        var_coef_dict = {
            variable: coef for variable,coef in zip(self.variables,self.coefs) if isinstance(variable, LinExpr)
        }
        return var_coef_dict

    def _get_expr_net_variables(
        self,
    ) -> Dict[Variable, float]:
        if not self._get_expr_variables:
           self._net_var_coefs, self._net_const = _traverse (self)
        return self._net_var_coefs
    
    def _get_expr_net_constant(self) -> float:
        if not self._net_const:
            self._net_var_coefs, self._net_const = _traverse (self)
        return self._net_const


def _traverse(expr: LinExpr, parent_coef: float = 1) -> Tuple[Dict[Variable, float], float]:
    result: Dict[Variable, float] = {}
    net_constant: float = 0.0
    def _update_result(var: Variable, coef: float):
        if var in result:
            result[var] +=coef
        else:
            result[var] = coef

    for var, coef in zip(expr.variables, expr.coefs):
        total_coef = coef * parent_coef
        if isinstance(var, Variable):
            _update_result(var, total_coef)
        elif isinstance(var, LinExpr):
            nested_result, nested_constant = _traverse(var, total_coef)
            for nested_var, nested_coef in nested_result.items():
                _update_result(nested_var, nested_coef)

            net_constant += nested_constant

    net_constant += expr.const * parent_coef
    return result, net_constant
    

    # should we add, and other overload methods
    # should we add modify methods
    # should we, or can we, implement a full blown implementation for LinExpr
    # should it be just for Type Testing?
    # does LinExpr really need to have the init method that way?

    # so I have to define all the overloader methods, in the interface
    # then I cannot just use the  pre-implemnted solvers/amls that already have this
    # and further the implementation might have a different way/conflict in implementation 
    # atributes, inits, methods than the contratct/
    # would I need an intermediate class that inherit from both contract, and implementaion
    # or somehow reconsiliate the two?

    # also are we kinda mutilating the use of the solvers/amls or their APIs
    # by putting our own layer? well that is kinda needed to make it solver independet
    # what would the MINIMUM Set of Requirements or Atributes that can we put on the 
    # Interface Without a Major risk of conflict in a specific implementatio.


# i guess the approach that I am taking does not allow to directly be using 
# the solver interface(gurobi) within the code, like having Isolver directly let gurobi API 
# to create LinXpr, etc

# Will mypy be okay, for further narrowing down an Attribute of the Base/Contract class


# TODO: I should add a saftey check that complains iff a variable included in the list of vars
# is not added to a model, i.e does not have model attached.
# also all variables need to be having the same model