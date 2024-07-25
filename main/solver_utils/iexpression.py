from abc import ABC, abstractmethod
from typing import List, Union

from solver_utils.ivariable import IVariable

class ILinExpr(ABC):
    name: str
    variables: List[Union[IVariable, "ILinExpr"]]
    coefs: List[float]
    const: float

    # @abstractmethod
    # def __init__(
    #     self,
    #     name: str,
    #     variables: List[Union[IVariable, "ILinExpr"]],
    #     coefs: List[float],
    #     const: float,
    # ):
    #     raise NotImplementedError
    

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