from ....model.automation import System
from ....model import ast

import palinka.ast.utils as astu

def build_source(system: System) -> ast.FunctionDefinition:
    """
        Build a the system's step function.
    """
    sys_namespace = f"sys_{system.get_slug_id()}"

    func_type_specifiers: list[ast.DeclarationSpecifier] = [ast.Void().as_type_specifier().as_declaration_specifier()]
    
    func_declarator: ast.Declarator = astu.func_declarator(
        f'{sys_namespace}_init',
        astu.param_list(
            astu.param_decl(
                [astu.struct_specifier("System_t").as_type_specifier().as_declaration_specifier()],
                astu.id_declarator("system", as_ptr=True)
            )
        )
    )   

    return ast.FunctionDefinition.create(
        func_type_specifiers,
        func_declarator,
        [],
        build_step_function_statements(system)
    )

def build_step_function_statements(system: System) -> ast.CompoundStatement:
    sys_namespace = f"sys_{system.get_slug_id()}"

    declarations: list[ast.Declaration] = []
    
    statements: list[ast.Statement] = []

    statements += [astu.assign_stmt(
        astu.attr_access_expr("sys", "app_base"),
        astu.attr_access_expr("sys", "base"),
    )]

    statements += [astu.assign_stmt(
         astu.attr_access_expr("sys", "nb_blocks"),
         astu.id_expr(f"&{system.get_id()}")
    )]

    statements += [astu.assign_stmt(
        astu.attr_access_expr("sys", "data_blocks"),
        astu.cast_expr(
            astu.typename(
                astu.struct_specifier("DataBlock_t").as_type_specifier(),
                as_ptr=True
            ),   
            astu.function_call_expr(
                "malloc",
                astu.mult_expr(
                    astu.sizeof(
                        ast.TypeName.create(
                            [astu.struct_specifier("DataBlock_t").as_type_specifier().as_declaration_specifier()],
                            None
                        )
                    ),
                    astu.constant_expr(system.get_number_of_data_blocks())
                )
                
            )
        )
    )]

    for db_id in system.get_data_block_ids():
        statements += [astu.assign_stmt(
            astu.attr_access_expr(
                astu.getitem_expr(
                    astu.attr_access_expr("sys", "data_blocks", arrow=False),
                    astu.id_expr(f"#{db_id}")
                ),
                "base"
            ),
            astu.getitem_expr(
                astu.attr_access_expr(
                    "sys",
                    "app_base"
                ),
                astu.id_expr(f"${db_id}")
            )
        )]
    
    statements += [astu.assign_stmt(
        astu.attr_access_expr("sys", "sys_base", arrow=False),
        astu.add_expr(
            astu.attr_access_expr("sys", "base", arrow=False),
            astu.function_call_expr(f"{sys_namespace}_app_memory_size")
        )
        
    )]

    return ast.CompoundStatement.create(declarations, statements)



