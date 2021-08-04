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
         astu.attr_access_expr("sys", "nb_blocks", arrow=False),
         astu.id_expr(f"&{system.get_id()}")
    )]

    return ast.CompoundStatement.create(declarations, statements)



