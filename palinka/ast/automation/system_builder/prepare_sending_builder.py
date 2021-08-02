from __future__ import annotations
from palinka.model.ast.external_declaration import ExternalDeclaration

import palinka.ast.utils as astu
from ....types import base_type
from ....model.automation import DataLink, System
from ....model import ast

def build_source(system: System) -> list[ast.automation.ExternalDeclaration]:
    """
        Build a the system's step function.

        void prepare_sending_@system_name(System_t* sys)
        {
            ...
        }
    """

    decls: list[ast.automation.ExternalDeclaration] = [
        build_function(system)
    ]   

    for lnk in filter(lambda lnk: lnk.get_source() == system, system.get_data_links()):
        decls += [build_subfunction(lnk, system)]
    
    return decls

def build_function(system: System) -> ast.automation.ExternalDeclaration:
    fb_name = f"sys_{system.get_id()}_copy_to_sending_memory"
    
    fb_declarator: ast.Declarator = ast.Declarator.create(
        None,
        # step_system_@system.name(System_t* sys)
        ast.DirectDeclarator.call(
            # step_system_@system.name
            ast.DirectDeclarator.identifier(ast.Identifier(fb_name)),
            # System_t* sys
            ast.ParameterList.create(
                # System_t* sys
                ast.ParameterDeclaration.create(
                    # System_t
                    [
                        ast.DeclarationSpecifier.create(
                            ast.TypeSpecifier(
                                ast.StructOrUnionSpecifier.struct_identifier(
                                    ast.Identifier("System_t")
                                )
                            )
                        )
                    ],
                    ast.Declarator.create(
                        ast.Pointer.basic(),
                        ast.DirectDeclarator.identifier(
                            ast.Identifier("sys")
                        )
                    )
                )
            )
        )
    )

    db_definition = ast.automation.DataBlockDefinition([])

    declarations = []
    statements = []
    
    for lnk in filter(lambda lnk: lnk.get_source() == system, system.get_data_links()):
        fb_name = f"sys_{lnk.get_source().get_name()}_copy_to_sending_memory_for_{lnk.get_target().get_name()}"
        statements += [astu.function_call_stmt(fb_name, "sys")]


    return ast.FunctionDefinition.create(
        [ast.DeclarationSpecifier(ast.TypeSpecifier(ast.Void()))],
        fb_declarator,
        [],
        ast.CompoundStatement.create(declarations, statements)
    )    

def build_subfunction(lnk: DataLink, system: System) -> ast.automation.ExternalDeclaration:
    fb_name = f"sys_{lnk.get_source().get_name()}_copy_to_sending_memory_for_{lnk.get_target().get_name()}"
    
    fb_declarator: ast.Declarator = ast.Declarator.create(
        None,
        # step_system_@system.name(System_t* sys)
        ast.DirectDeclarator.call(
            # step_system_@system.name
            ast.DirectDeclarator.identifier(ast.Identifier(fb_name)),
            # System_t* sys
            ast.ParameterList.create(
                # System_t* sys
                ast.ParameterDeclaration.create(
                    # System_t
                    [
                        ast.DeclarationSpecifier.create(
                            ast.TypeSpecifier(
                                ast.StructOrUnionSpecifier.struct_identifier(
                                    ast.Identifier("System_t")
                                )
                            )
                        )
                    ],
                    ast.Declarator.create(
                        ast.Pointer.basic(),
                        ast.DirectDeclarator.identifier(
                            ast.Identifier("sys")
                        )
                    )
                )
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
        f"SENDING:{lnk.get_target().get_id()}"
    )

def build_subfunction_statements(lnk: DataLink, system: System) -> ast.CompoundStatement:
    declarations = []
    statements = []

    declarations += [
        astu.struct_var_decl("DataBlock_t", "idb", as_ptr=True),
        astu.struct_var_decl("DataBlock_t", "fp_idb", as_ptr=True)
    ]

    # idb = open_data_block(sys, $SENDING:@lnk.get_target().get_id());   
    statements += [astu.assign_stmt(
        "idb",
        astu.function_call_expr(
            'open_data_block', 
            'sys', 
            f"$SENDING:{lnk.get_target().get_id()}"
        )
    )]


    exporting_function_plans = []
    for data in lnk.get_data():
        for fp in system.get_function_plans():
            for output in fp.get_outputs():
                if output.get_data() == data:
                    exporting_function_plans.append((data, fp, output))
    
    for (data, function_plan, output) in exporting_function_plans:
        lh = astu.getitem_expr(
            astu.attr_access_expr("idb", "base"), 
            f"${data.get_id()}"
        )

        rh = astu.getitem_expr(
            astu.attr_access_expr("fp_idb", "base"),
            f"${function_plan.get_id()}/{output.get_source().get_global_id()}"
        )

        if data.get_type() != base_type:
            lh = astu.cast_expr(str(data.get_type()), lh, as_ptr=True)
            rh = astu.cast_expr(str(data.get_type()), lh, as_ptr=True)
        
        lh = astu.deref_expr(lh)
        rh = astu.deref_expr(rh)

        statements += [
            astu.assign_stmt("fp_idb", astu.function_call_expr("open_data_block", "sys", f"${function_plan.get_id()}")),
            astu.assign_expr(lh, rh)
        ]


    return ast.CompoundStatement.create(declarations, statements)