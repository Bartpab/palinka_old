from ....model.automation import System
from ....model import ast

from .. import function_plan_builder
from . import step_function_builder

def build(system: System) -> ast.automation.SystemDeclaration:
    declarations: list[ast.automation.ExternalDeclaration] = [] 
    declarations += ast.automation.ExternalDeclaration(step_function_builder.build(system))

    for function_plan in system.get_function_plans():
        declarations.append(
            ast.automation.ExternalDeclaration(
                function_plan_builder.build(function_plan)
            )
        )
    
    return ast.automation.SystemDeclaration.create(
        ast.Identifier(system.get_name()),
        ast.TranslationUnit(declarations)
    )

