from __future__ import annotations
from palinka.model.ast.external_declaration import ExternalDeclaration

import palinka.ast.utils as astu
from ....types import base_type
from ....model.automation import DataLink, System
from ....model import ast

def build_source(system: System) -> list[ast.automation.ExternalDeclaration]:
    """
        Build the system's copy recv routine.

        A data link is a pair consumer system/producer system. 

        A memory area in the consumer system is created to store all the information that are produced by the producer system.

        This routine will copy the data to function plans data blocks which are consumer of the information.

        The routine is called "sys_{system.get_id()}_cpy_recv"
    """
    if not system.get_importing_data_links():
        return []

    decls: list[ast.automation.ExternalDeclaration] = [
        build_function(system)
    ]   

    for lnk in filter(lambda lnk: lnk.get_target() == system, system.get_data_links()):
        decls += [build_subfunction(lnk, system)]
    
    return decls

def build_function(system: System) -> ast.automation.ExternalDeclaration:
    fb_name = f"sys_{system.get_slug_id()}_cpy_recv"
    
    fb_declarator = astu.func_declarator(
        fb_name,
        astu.param_list(
            astu.param_decl(
                astu.struct_specifier("System_t").as_type_specifier(),
                astu.id_declarator("sys", True)
            )
        )
    )

    db_definition = ast.automation.DataBlockDefinition([])

    declarations = []
    statements = []
    
    for lnk in filter(lambda lnk: lnk.get_target() == system, system.get_data_links()):
        fb_name = f"sys_{system.get_slug_id()}_cpy_recv_{lnk.get_id()}"
        statements += [astu.function_call_stmt(fb_name, "sys")]


    return ast.FunctionDefinition.create(
        [ast.Void().as_type_specifier().as_declaration_specifier()],
        fb_declarator,
        [],
        ast.CompoundStatement.create(declarations, statements)
    )    

def build_subfunction(lnk: DataLink, system: System) -> ast.automation.ExternalDeclaration:
    fb_name = f"sys_{system.get_slug_id()}_cpy_recv_{lnk.get_id()}"
    
    fb_declarator = astu.func_declarator(
        fb_name,
        astu.param_list(
            astu.param_decl(
                astu.struct_specifier("System_t").as_type_specifier(),
                astu.id_declarator("sys", True)
            )
        )
    )

    db_definition = ast.automation.DataBlockDefinition([
        ast.automation.DataBlockEntryDeclaration(data.get_id(), data.get_type()) for data in lnk.get_data()
    ])

    return ast.automation.FunctionBlockDefinition.create(
        db_definition,
        [ast.DeclarationSpecifier(ast.TypeSpecifier(ast.Void()))],
        fb_declarator,
        build_subfunction_statements(lnk, system),
        f"RECV:{lnk.get_id()}"
    )

def build_subfunction_statements(lnk: DataLink, system: System) -> ast.CompoundStatement:
    declarations = []
    statements = []

    declarations += [
        astu.struct_var_decl("DataBlock_t", "idb", as_ptr=False),
        astu.struct_var_decl("DataBlock_t", "fp_idb", as_ptr=False)
    ]

    statements += [astu.assign_stmt(
        "idb",
        astu.function_call_expr(
            'open_data_block', 
            'sys', 
            f"$RECV:{lnk.get_id()}"
        )
    )]

    consuming_function_plans = []
    
    for data in lnk.get_data():
        for fp in system.get_function_plans():
            for ipt in fp.get_inputs():
                if ipt.get_data() == data:
                    consuming_function_plans.append((data, fp, ipt))
    
    for (data, function_plan, ipt) in consuming_function_plans:
        lh = astu.getitem_expr(
            astu.attr_access_expr("fp_idb", "base", arrow=False), 
             f"${function_plan.get_id()}/{ipt.get_target().get_global_id()}"
        )

        rh = astu.getitem_expr(
            astu.attr_access_expr("idb", "base", arrow=False),
            f"${data.get_id()}"
        )

        if data.get_type() != base_type:
            lh = astu.cast_expr(str(data.get_type()), lh, as_ptr=True)
            rh = astu.cast_expr(str(data.get_type()), rh, as_ptr=True)
        
        lh = astu.deref_expr(lh)
        rh = astu.deref_expr(rh)

        statements += [
            astu.assign_stmt("fp_idb", astu.function_call_expr("open_data_block", "sys", f"${function_plan.get_id()}")),
            astu.assign_expr(lh, rh),
            astu.function_call_stmt(
                "close_data_block",
                astu.ref_expr("fp_idb")

            )
        ]
    
    statements.append(
            astu.function_call_stmt(
                "close_data_block",
                astu.ref_expr("idb")

            )        
    )


    return ast.CompoundStatement.create(declarations, statements)