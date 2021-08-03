from palinka.model.ast import unary_expression
from palinka.model.ast.identifier import Identifier
from typing import Iterator, Tuple

from ...model.automation import Plant, Data, System, DataLink
from ...model import ast
from ...model import damo
from ...utils import Database, TwoDimensionalIndex
from . import system

import palinka.ast.utils as astu

import itertools

def build(plant: Plant):
    systems: list[ast.automation.SystemDeclaration] = [system.build(sys) for sys in plant.get_systems()]
    
    preprocessors =  [
        ast.Preprocessor(
            ast.Include(ast.Identifier("src/model/plant.h"), internal=True)
        ),
        ast.Preprocessor(
            ast.Include(ast.Identifier("pthread"))
        )
    ]
    
    return ast.automation.PlantDeclaration(
        systems, 
        ast.automation.TranslationUnit([
            build_init_function(plant)
        ],preprocessors)
    )

def build_init_function(plant: Plant):
    declarations = []
    statements = []

    declarations.append(
        astu.struct_var_decl("Plant_t", "plant", as_ptr=False)
    )

    statements += [astu.assign_stmt(
        astu.attr_access_expr("plant", "base", arrow=False),
        astu.cast_expr(
            astu.typename("char", as_ptr=True),     
            astu.function_call_expr(
                "malloc",
                astu.mult_expr(
                    astu.sizeof(
                        ast.TypeName.create(
                            [ast.Char().as_type_specifier().as_declaration_specifier()],
                            None
                        )
                    ),
                    astu.id_expr("@plant")
                )
            )
        )
    )]

    nb_systems = len(list(iter(plant.get_systems())))

    statements += [astu.assign_stmt(
        astu.attr_access_expr("plant", "systems", arrow=False),
        astu.cast_expr(
            astu.typename(
                astu.struct_specifier("System_t").as_type_specifier(),
                as_ptr=True
            ),   
            astu.function_call_expr(
                "malloc",
                astu.mult_expr(
                    astu.sizeof(
                        ast.TypeName.create(
                            [astu.struct_specifier("System_t").as_type_specifier().as_declaration_specifier()],
                            None
                        )
                    ),
                    ast.PrimaryExpression(ast.Constant(nb_systems))
                )
                
            )
        )
    )]

    statements += [astu.assign_stmt(
         astu.attr_access_expr("plant", "nb_systems", arrow=False),
         ast.PrimaryExpression(ast.Constant(nb_systems))
    )]

    for i, system in enumerate(plant.get_systems()):
        statements += [astu.assign_stmt(
            astu.attr_access_expr(
                astu.getitem_expr(
                    astu.attr_access_expr("plant", "systems", arrow=False),
                    astu.constant_expr(i)
                ),
                "offset"
            ),
            astu.id_expr(f"${system.get_id()}")
        ), astu.assign_stmt(
            astu.attr_access_expr(
                astu.getitem_expr(
                    astu.attr_access_expr("plant", "systems", arrow=False),
                    astu.constant_expr(i)
                ),
                "size"
            ),
            astu.id_expr(f"@{system.get_id()}")
        ), astu.function_call_stmt(
            "pthread_rwlock_init",
            astu.ref_expr(
                astu.attr_access_expr(
                    astu.getitem_expr(
                        astu.attr_access_expr("plant", "systems", arrow=False),
                        astu.constant_expr(i)
                    ),
                    "rwlock"
                )
            )

        ), astu.assign_stmt(
            astu.attr_access_expr(
                astu.getitem_expr(
                    astu.attr_access_expr("plant", "systems", arrow=False),
                    astu.constant_expr(i)
                ),
                "step"
            ),
            astu.id_expr(f"sys_{system.get_id()}_step")
        )]        

    statements += [astu.return_stmt("plant")]
    
    return astu.func_decl(
        [astu.struct_specifier("Plant_t")],
        astu.func_declarator(
            "init",
            None,
            as_ptr=False
        ),
        [],
        ast.CompoundStatement.create(declarations, statements)
    )