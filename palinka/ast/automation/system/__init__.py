from more_itertools import unique_everseen

import palinka.ast.utils as astu

from palinka.utils import rec_find_all
from ....model.automation import System
from ....model import ast

from .. import function_plan
from . import step_function
from . import cpy_send
from . import cpy_recv


def build(system: System) -> ast.automation.SystemDeclaration:
    return ast.automation.SystemDeclaration.create(
        ast.Identifier(system.get_name()),
        build_header(system),
        build_source(system)
    )


def build_header(system: System) -> ast.automation.TranslationUnit:
    declarations = []

    # Declare the step function
    declarations += [ast.Declaration.create(
        [ast.Void().as_type_specifier().as_declaration_specifier()],
        ast.InitDeclarator.create(
            ast.Declarator.create(
                None, 
                ast.DirectDeclarator.call(
                    ast.DirectDeclarator.identifier(
                        ast.Identifier(f"sys_{system.get_id()}_step")
                    ), 
                    astu.param_list(
                        astu.param_decl(
                            [astu.struct_specifier("Plant_t").as_type_specifier().as_declaration_specifier()],
                            astu.id_declarator("plant", as_ptr=True)
                        )
                    )
                )
            )
        )
    )]

    preprocessors = [
        ast.Preprocessor(
            ast.Include(
                ast.Identifier(
                    f"src/model/plant.h"
                ), internal=True
            )
        )
    ]

    return ast.automation.TranslationUnit(declarations, preprocessors)

def build_source(system: System) -> ast.automation.TranslationUnit:
    declarations: list[ast.automation.ExternalDeclaration] = [] 
    declarations += ast.automation.ExternalDeclaration(step_function.build_source(system))

    for fp in system.get_function_plans():
        declarations.append(
            ast.automation.ExternalDeclaration(
                function_plan.build_source(fp)
            )
        )

    declarations += cpy_recv.build_source(system)
    declarations += cpy_send.build_source(system)

    preprocessors = [
        ast.Preprocessor(
            ast.Include(
                ast.Identifier(
                    f"src/model/system.h"
                ), internal=True
            )
        ),
        ast.Preprocessor(
            ast.Include(
                ast.Identifier(
                    f"src/model/data_block.h"
                ), internal=True
            )
        ),
        ast.Preprocessor(
            ast.Include(
                ast.Identifier(
                    f"src/codegen/plant/{system.get_id()}.h"
                ), internal=True
            )
        )
    ]

    # Retrieve all the block calls
    for block in unique_everseen(map(lambda node: node.name[6:], rec_find_all(lambda node: isinstance(node, ast.Identifier) and node.name.startswith("block_"), declarations))):
        preprocessors += [
            ast.Preprocessor(
                ast.Include(
                    ast.Identifier(
                        f"src/blocks/{block}.h"
                    ), internal=True
                )
            )
        ]        

    return ast.automation.TranslationUnit(declarations, preprocessors)