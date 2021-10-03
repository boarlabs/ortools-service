# from ..context import operations_research

from os import name
from operations_research.linear_solver_pb2 import(
    MPModelProto,
    MPVariableProto,
    MPConstraintProto
)

from operations_research.linear_extension_pb2 import(
    ExpressionMPModel,
    ReferenceMPVariable,
    MPExpression,
    ReferenceMPModel,
    ReferenceMPConstraint,
)


class Load:
    def __init__(
        self,
        interval_set,
        params: dict,
        ):
        super().__init__()

        self.mipmodel = MPModelProto()


        ## Setup
        self.id = params["name"]
        self.objective_terms = {}

        self.mipmodel.name = self.id
        self.load_ramp = 100

        self.load =  params["load"]

        self.net_export = [
            MPVariableProto(
                lower_bound = -self.load[idx],
                upper_bound = -self.load[idx],
                name = "net_export["+ str(idx)+"]"
            ) for idx in interval_set
        ]

        ## I need this to test the constraint creation on the server
        self.load_ramp = [
            MPConstraintProto(
                name= f"load_ramp[{str(idx)}]",
                coefficient = [1, -1],
                var_index = [idx+1, idx],
                lower_bound = self.load_ramp,
                
            ) for idx in range(len(interval_set)-1)
        ]

        # [self.mipmodel.variable.add(var) for var in self.net_export]
        self.mipmodel.variable.extend(self.net_export)
        # self.mipmodel.constraint.extend(self.load_ramp)
        return


class Generator:
    def __init__(
        self,
        interval_set,
        params: dict,
        ):
        super().__init__()

        self.mipmodel = ExpressionMPModel()

        self.id = params["name"]
        self.objective_terms = {}

        self.mipmodel.name = self.id

        ## Parameters
        self.maxMW = params["maxMW"]
        self.minMW = params["minMW"]
        self.max_ramp = params["max_ramp"]
        self.marginal_cost = params["marginal_cost"]
        self.initial_commit = params["initial_commit"]

        ## Variables
        self.output = [
            MPVariableProto(
                lower_bound = 0,
                upper_bound = self.maxMW,
                name = "output["+ str(idx)+"]",
            ) for idx in interval_set
        ] 
        # [self.mipmodel.variable.add(var) for var in self.output]
        # for var in self.output: 
        self.mipmodel.variable.extend(self.output)


        self.commit = [
            MPVariableProto(
                lower_bound = 0,
                upper_bound = 1,
                is_integer = True,
                name = f"commit[{idx}]",
            ) for idx in interval_set
        ] 

        # for var in self.commit: 
        self.mipmodel.variable.extend(self.commit)


        ## Expressions - this is where we define a common interface for model resource elements
        # Note in Optopy we have to have a generic and dynamic common interface for market products, different time indices, etc.
        # Will just use net_export as an interface for now
        # def _net_export(b,idx):
        #     return b.output[idx]
        # self.block.net_export = aml.Expression(interval_set, rule=_net_export)


        self.net_export = [ 
            MPExpression(
                name = f"net_export[{idx}]",
                variables = [
                    ReferenceMPVariable(
                        var_name = f"output[{idx}]",
                    )
                ],    
                variable_coefficients = [1],
            ) for idx in interval_set
        ]

        # for item in self.ne_export: 
        self.mipmodel.expressions.extend(self.net_export)


        ## Constraints
        # Note constraints should work with regular pyomo expression syntax
        # Should be able to reduce the amount of boilerplate here
        # def _output_commit_upper_bound(b,idx):
        #     return b.output[idx] - b.commit[idx] * b.maxMW <= 0
        # self.con_output_commit_upper_bound = aml.Constraint(interval_set, rule=_output_commit_upper_bound)


        self.con_output_commit_upper_bound = [
            MPConstraintProto(
                var_index= [idx, len(interval_set)+idx],
                coefficient = [1, -1*self.maxMW],
                upper_bound = 0,
                name = f"con_output_commit_upper_bound[{idx}]"
            ) for idx in range(len(interval_set))
        ]

        # for item in  self.con_output_commit_upper_bound: 
        self.mipmodel.constraint.extend(self.con_output_commit_upper_bound)
        # def _output_commit_lower_bound(b,idx):
        #     return b.commit[idx] * b.minMW - b.output[idx] <= 0
        # self.block.con_output_commit_lower_bound = aml.Constraint(interval_set, rule=_output_commit_lower_bound)
        # todo Add constraints/costs for ramping, min up, min down, startup/shutdown costs, etc.

        self.con_output_commit_lower_bound = [
            MPConstraintProto(
                var_index= [idx, len(interval_set)+idx],
                coefficient = [-1, 1*self.minMW],
                upper_bound = 0,
                name = f"con_output_commit_lower_bound[{idx}]"
            ) for idx in range(len(interval_set))
        ]


        self.mipmodel.constraint.extend(self.con_output_commit_lower_bound)
        

        ## Objective Terms
        # Unclear whether this expression object needs to be added to block/model - may be enough just to have it in the objective

        # def _interval_cost(b,idx):
        #     return b.marginal_cost * b.output[idx]
        # self.block.interval_cost = aml.Expression(interval_set, rule=_interval_cost)

        # def _total_cost(b):
        #     return sum(b.interval_cost[idx] for idx in interval_set)
        # self.block.total_cost = aml.Expression(rule=_total_cost)



        self.interval_cost = [
            MPExpression(
                name = f"interval_cost[{idx}]",
                variables = [
                    ReferenceMPVariable(
                        var_name = f"output[{idx}]",
                    )
                ],    
                variable_coefficients = [self.marginal_cost],
            ) for idx in interval_set
        ]
        
        self.mipmodel.expressions.extend(self.interval_cost)

        self.total_cost =  MPExpression(
            name = f"total_cost",
            variables = [
                ReferenceMPVariable(
                    var_name = f"interval_cost[{idx}]",
                ) for idx in interval_set
            ],    
            variable_coefficients = [1]*len(interval_set),
            objective_coefficient = 1
        )         
        
        
        self.mipmodel.expressions.extend([self.total_cost])


        self.objective_terms["marginal_cost"] = self.total_cost
        

class Collection:
    def __init__(
        self,
        interval_set,
        params: dict,
    ):
        super().__init__()

        self.mipmodel = ReferenceMPModel()
        self.mipmodel.model_dependencies.extend(['parent'])

        ## Setup
        self.id = params["name"]
        self.objective_terms = {}
        self.mipmodel.name = self.id
        self.interval_set = interval_set

        self.component_element_ids = params["component_element_names"] # resources or other collections

        ## Parameters
        self.import_limit = params["import_limit"] # assume positive
        self.export_limit = params["export_limit"]

        
        self.net_export = [
            MPVariableProto(
                lower_bound = -self.import_limit,
                upper_bound = self.export_limit,
                name = f"net_export[{idx}]"
            ) for idx in interval_set
        ]


        # for item in self.net_export: self.mipmodel.variables.add(item)
        self.mipmodel.variables.extend(self.net_export)

        ### Can we have some reference vars that are added to model but not used in any constraints?
        ## if it can happen, then should we check to remove before passing?

        self.collection_components_net_exports = list()

        for idx in interval_set:

            self.collection_components_net_exports.append(
                [
                    ReferenceMPVariable(
                        var_name = f"net_export[{idx}]",
                        model_name = f"parent.{component_element}",
                        )  for component_element in self.component_element_ids 
                ]
            ) 
                
        
        # toDo for the wild character should I go for ..* or container.conetnts, parent.children... 
        # note that when defining a model with wild-chars, then we would be facing multiple(Or maybe none)
        # with such description.


        # toDO: I could assign a name to the reference variables and then assign the expressions based on name

        # for item in self.collection_components_net_exports: self.mipmodel.reference_variables.add(item)
        for idx in range(len(interval_set)):
            self.mipmodel.reference_variables.extend(self.collection_components_net_exports[idx])

        self.sum_of_component_net_exports= [ 
            MPExpression(
                name = f"sum_of_component_net_exports[{idx+1}]",
                variables = self.collection_components_net_exports[idx],    
                variable_coefficients = [1]*len(self.collection_components_net_exports[idx]),
            ) for idx in range(len(interval_set))

        ]

        # for item in self.sum_of_component_net_exports: self.mipmodel.expressions.add(item)
        self.mipmodel.expressions.extend(self.sum_of_component_net_exports)


        # toDo here we are creating an expression based on some variables that each of them could actually be multiple 
        # ones, based on the wild-char defenition we included in the past segment. So in that case, the coeff defined 
        # for such vars, should be extended for all of them.

        # def update_coupling_constraints(self):
            
        #     def _coupling_net_export(b,idx):
        #         sum_of_component_element_net_exports_idx = sum(getattr(b.parent_block(),component_element_id).net_export[idx] for component_element_id in self.component_element_ids)
        #         return b.net_export[idx] - sum_of_component_element_net_exports_idx == 0

        self.con_coupling_net_export = [
            ReferenceMPConstraint(
                lower_bound = 0,
                upper_bound = 0,
                name = f"con_coupling_net_export[{idx+1}]",
                variable_references = [
                    ReferenceMPVariable(
                        var_name = f"net_export[{idx+1}]",
                    ),
                    ReferenceMPVariable(
                        var_name = f"sum_of_component_net_exports[{idx+1}]"
                    ),
                ],
                variable_coefficients = [1, -1], 

                # expression_coefficients = [-1],
                # expressions = [self.sum_of_component_net_exports[idx]],
                # variables = [self.net_export[idx]],
                # var_coefficients = [1],
            ) for idx in range(len(interval_set))
        ]

        self.mipmodel.reference_constraints.extend(self.con_coupling_net_export)
