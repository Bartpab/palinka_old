from __future__ import annotations

import palinka.ast.utils as astu

from ...model.automation import FunctionPlan, Data
from ...model import ast

from . import function_block

def build_source(fp: FunctionPlan) -> ast.automation.FunctionBlockDefinition:
    fb_name = f"fp_{fp.get_slug_id()}"

    return ast.automation.FunctionBlockDefinition.create(
        build_data_block_definition(fp),
        [ast.Void().as_type_specifier().as_declaration_specifier()],
        astu.func_declarator(
            fb_name,
            astu.param_list(
                astu.param_decl(
                    astu.struct_specifier("System_t").as_type_specifier().as_declaration_specifier(),
                    astu.id_declarator("sys", as_ptr=True)
                )
            )
        ),
        build_statements(fp),
        fp.get_id()
    )

def build_statements(function_plan: FunctionPlan) -> ast.CompoundStatement:
    declarations = []
    statements = []

    declarations += [astu.struct_var_decl("DataBlock_t", "idb", as_ptr=False),]

    statements += [astu.assign_stmt(
        "idb",
        astu.function_call_expr(
            'open_data_block', 
            'sys', 
            f'#{function_plan.get_id()}'
        )
    )]


    for block in function_plan.get_blocks():
        statements += function_block.build(block)
    
    # We do not forget to close the data block
    statements.append(
            astu.function_call_stmt(
                "close_data_block",
                astu.ref_expr("idb")

            )        
    )

    return ast.CompoundStatement.create(declarations, statements)

def build_data_block_entry(data: Data) -> ast.automation.DataBlockEntryDeclaration:
    return ast.automation.DataBlockEntryDeclaration(data.get_id(), data.get_type())

def build_data_block_definition(function_plan: FunctionPlan) -> ast.automation.DataBlockDefinition:
    return ast.automation.DataBlockDefinition([build_data_block_entry(entry) for entry in function_plan.get_internal_data()])