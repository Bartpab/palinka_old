from palinka.model.ast.identifier import Identifier
from typing import Iterator, Tuple

from ...model.automation import Plant, Data, System, DataLink
from ...model import ast
from ...model import damo
from ...utils import Database, TwoDimensionalIndex
from . import system_builder

import palinka.ast.utils as astu

import itertools

def build(plant: Plant):
    systems: list[ast.automation.SystemDeclaration] = [system_builder.build(system) for system in plant.get_systems()]
    
    return ast.automation.PlantDeclaration(
        systems, 
        ast.automation.TranslationUnit([
            build_init_function(plant),
            build_step_function(plant)
        ], [
            ast.Preprocessor(ast.Include(ast.Identifier("src/model/plant.h"), internal=True))
        ])
    )

def build_init_function(plant: Plant):
    declarations = []
    statements = []

    declarations.append(
        astu.struct_var_decl("Plant_t", "plant", as_ptr=True)
    )

    statements += [astu.assign_stmt(
        "plant", 
        astu.cast_expr(
            astu.typename(
                astu.struct_specifier("Plant_t").as_type_specifier(),
                as_ptr=True
            ),   
            astu.function_call_expr(
                "malloc",
                astu.sizeof(
                    ast.TypeName.create(
                        [astu.struct_specifier("Plant_t").as_type_specifier().as_declaration_specifier()],
                        None
                    )
                )
            )
        )
    )]
    
    statements += [astu.assign_stmt(
        astu.attr_access_expr("plant", "base"),
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

    statements += [astu.return_stmt("plant")]
    
    return astu.func_decl(
        [astu.struct_specifier("Plant_t")],
        astu.func_declarator(
            "init",
            None,
            as_ptr=True
        ),
        [],
        ast.CompoundStatement.create(declarations, statements)
    )


def build_step_function(plant: Plant):
    statements = []

    for system in plant.get_systems():
        statements += [astu.function_call_stmt(f"sys_{system.get_id()}_step", "plant")]
    
    return astu.func_decl(
        [ast.Void().as_type_specifier().as_declaration_specifier()],
        astu.func_declarator(
            "step", 
            astu.param_list(
                astu.param_decl(
                    [astu.struct_specifier("Plant_t").as_type_specifier().as_declaration_specifier()],
                    astu.id_declarator("plant", as_ptr=True)
                )
            )
        ), 
        [],
        ast.CompoundStatement.create([], statements)
    )





