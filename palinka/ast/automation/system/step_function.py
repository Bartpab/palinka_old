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
        f'{sys_namespace}_step',
        astu.param_list(
            astu.param_decl(
                [astu.struct_specifier("Plant_t").as_type_specifier().as_declaration_specifier()],
                astu.id_declarator("plant", as_ptr=True)
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

    declarations: list[ast.Declaration] = [
        astu.struct_var_decl("System_t", "sys", as_ptr=True)
    ]
    
    statements: list[ast.Statement] = [
        astu.assign_stmt(
            "sys", 
            astu.function_call_expr("open_system", "plant", f"{system.get_address()}")
        )
    ]

    # We received data from other systems
    if system.get_importing_data_links():
        statements += [
            astu.function_call_stmt(f"{sys_namespace}_cpy_recv", astu.ref_expr("sys"))
        ]

    if system.get_relay_data_links():
        statements += [
            astu.function_call_stmt(f"{sys_namespace}_cpy_relay", "plant", astu.ref_expr("sys"))
        ]        

    for function_plan in system.get_function_plans():
        statements += [
            astu.function_call_stmt(
                f"fb_{function_plan.get_id()}",
                astu.ref_expr("sys")
            )
        ]

    # We send data to other systems
    if system.get_exporting_data_links():
        statements += [
            astu.function_call_stmt(f"{sys_namespace}_cpy_send", astu.ref_expr("sys"))
        ]

    statements += [
        astu.function_call_stmt("close_system", astu.ref_expr("sys"))
    ]

    return ast.CompoundStatement.create(declarations, statements)



