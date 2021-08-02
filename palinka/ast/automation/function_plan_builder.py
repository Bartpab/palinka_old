from __future__ import annotations

from ...model.automation import FunctionPlan, Data
from ...model import ast

from . import function_block_builder

def build_source(fp: FunctionPlan) -> ast.automation.FunctionBlockDefinition:
    fb_name = f"fp_{fp.get_id()}"
    
    fb_declarator: ast.Declarator = ast.Declarator.create(
        None,
        # step_system_@system.name(System_t* sys, DataBlock_t* idb)
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

    return ast.automation.FunctionBlockDefinition.create(
        build_data_block_definition(fp),
        [ast.DeclarationSpecifier(ast.TypeSpecifier(ast.Void()))],
        fb_declarator,
        build_statements(fp),
        fp.get_id()
    )

def build_statements(function_plan: FunctionPlan) -> ast.CompoundStatement:
    declarations = []
    statements = []

    declarations += [
        ast.Declaration.create([  # DataBlock_t* idb;
            ast.DeclarationSpecifier.create(
                ast.TypeSpecifier.create(
                        ast.StructOrUnionSpecifier.struct_identifier(ast.Identifier('DataBlock_t'))
                    )
                )
        ], [
            ast.InitDeclarator.create(
                ast.Declarator.create(
                    ast.Pointer.basic(),
                    ast.DirectDeclarator.identifier(ast.Identifier('idb'))
                )
            )
        ])
    ]

    # We "open" the data block to pass it to the FB call
    # Translate into:
    #   idb = open_data_block(sys, $DataBlock:@segment.seg_name);   

    # open_data_block(sys, $DataBlock:@segment.seg_name)
    rh = ast.PostfixExpression.call(
        ast.PrimaryExpression.identifier(ast.Identifier("open_data_block")).as_(ast.PostfixExpression),
        [
            ast.PrimaryExpression.identifier(
                ast.Identifier(
                    'sys'
                )
            ).as_(ast.AssignmentExpression),
            ast.PrimaryExpression.identifier(
                ast.Identifier(
                    f'${function_plan.get_global_id()}'
                )
            )
        ]
    ).as_(ast.AssignmentExpression)

    # idb
    lh: ast.ConditionalExpression = ast.PrimaryExpression.identifier(ast.Identifier('idb')).as_(ast.ConditionalExpression)

    # idb = open_data_block(sys, $DataBlock:@segment.seg_name);  
    open_data_block = ast.ExpressionStatement(
        ast.AssignmentExpression.expr(lh, '=', rh).as_expression()
    ).as_statement()

    statements += [open_data_block]


    for block in function_plan.get_blocks():
        statements += function_block_builder.build(block)
    
    return ast.CompoundStatement.create(declarations, statements)

def build_data_block_entry(data: Data) -> ast.automation.DataBlockEntryDeclaration:
    return ast.automation.DataBlockEntryDeclaration(data.get_id(), data.get_type())

def build_data_block_definition(function_plan: FunctionPlan) -> ast.automation.DataBlockDefinition:
    return ast.automation.DataBlockDefinition([build_data_block_entry(entry) for entry in function_plan.get_internal_data()])