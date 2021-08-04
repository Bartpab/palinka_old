from ...model.automation import Plant
from ...model import ast
from . import system

import palinka.ast.utils as astu


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
                    astu.id_expr("&plant")
                )
                
            )
        )
    )]

    statements += [astu.assign_stmt(
         astu.attr_access_expr("plant", "nb_systems", arrow=False),
         astu.id_expr("&plant")
    )]

    for i, system in enumerate(plant.get_systems()):
        sys_namespace = f"sys_{system.get_slug_id()}"

        statements += [astu.assign_stmt(
            astu.attr_access_expr(
                astu.getitem_expr(
                    astu.attr_access_expr("plant", "systems", arrow=False),
                    astu.id_expr(f"#{system.get_id()}")
                ),
                "offset"
            ),
            astu.id_expr(f"${system.get_id()}")
        ), astu.assign_stmt(
            astu.attr_access_expr(
                astu.getitem_expr(
                    astu.attr_access_expr("plant", "systems", arrow=False),
                    astu.id_expr(f"#{system.get_id()}")
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
                        astu.id_expr(f"#{system.get_id()}")
                    ),
                    "rwlock"
                )
            )

        ), astu.assign_stmt(
            astu.attr_access_expr(
                astu.getitem_expr(
                    astu.attr_access_expr("plant", "systems", arrow=False),
                    astu.id_expr(f"#{system.get_id()}")
                ),
                "step"
            ),
            astu.id_expr(f"{sys_namespace}_step")
        ), astu.function_call_stmt(
            f"{sys_namespace}_init",
            astu.getitem_expr(
                    astu.attr_access_expr("plant", "systems", arrow=False),
                    astu.id_expr(f"#{system.get_id()}")
            )
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