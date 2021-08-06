from ....model.automation import System
from ....model import ast

import palinka.ast.utils as astu

def build_source(system: System) -> ast.FunctionDefinition:
    """
        Build a the system's step function.
    """
    sys_namespace = f"sys_{system.get_slug_id()}"

    return ast.FunctionDefinition.create(
        [ast.TypedefName(ast.Identifier("size_t")).as_type_specifier().as_declaration_specifier()],
        astu.func_declarator(f'{sys_namespace}_os_memory_size'),
        [],
        build_statements(system)
    )

def build_statements(system: System) -> ast.CompoundStatement:
    sys_namespace = f"sys_{system.get_slug_id()}"

    declarations: list[ast.Declaration] = []
    statements: list[ast.Statement] = []
   
    stack = list(system.get_data_block_ids())
    
    mem = astu.sizeof(astu.typename(astu.struct_specifier("SystemData_t").as_type_specifier()))
    
    statements += [astu.return_stmt(mem)]

    return ast.CompoundStatement.create(declarations, statements)



