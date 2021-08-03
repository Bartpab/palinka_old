from __future__ import annotations
from palinka.model.ast.assignment_expression import AssignmentExpression
from palinka.model.ast.cast_expression import CastExpression

import palinka.ast.utils as astu

from palinka.types import base_type

from ...model.automation import FunctionBlock
from ...model import ast

def build(block: FunctionBlock) -> list[ast.Statement]:
    """
        Returns a list of statements based on the segment's symbol functionality

        - Build input assignments
        - Build the function call
    """
    statements: list[ast.Statement] = []

    statements += build_input_assignments(block)
    statements += build_function_call(block)
    
    return statements

def build_input_assignments(block: FunctionBlock) -> list[ast.Statement]:
    """
        Retrieve the inputs of the symbol from the outputs of the preceding symbols.

        Symbol's function are called as regular function calls.

        IO of symbol's function are stored in the instance data block of the called function block.
    """    
    statements: list[ast.Statement] = []
    
    for port in block.get_ports():
        for c in block.get_function_plan().get_connections():
            if port == c.get_target():

                lh = astu.getitem_expr(
                    astu.attr_access_expr("idb", "base", arrow=False), 
                    f"${c.get_target().get_global_id()}"
                )

                rh = astu.getitem_expr(
                    astu.attr_access_expr("idb", "base", arrow=False),
                    f"${c.get_source().get_global_id()}"
                )

                if c.get_target().get_type() != base_type:
                    lh = astu.cast_expr(str(c.get_target().get_type()), lh, as_ptr=True)
                
                if c.get_source().get_type() != base_type:
                    rh = astu.cast_expr(str(c.get_source().get_type()), rh, as_ptr=True)
                
                lh = astu.deref_expr(lh)
                rh = astu.deref_expr(rh)

                statements.append(
                    astu.assign_stmt(lh, rh)
                )

    return statements


def build_function_call(block: FunctionBlock) -> list[ast.Statement]:
    function_name: ast.PostfixExpression = ast.PrimaryExpression.identifier(
        ast.Identifier(f"block_{block.get_class()}")
    ).as_(ast.PostfixExpression)
    
    args: list[ast.AssignmentExpression] = []
    
    for p in block.get_ports():
        # Recast lefthand
        # (p.get_type()*)
        typename_recast: ast.TypeName = ast.TypeName.create(
            [ast.SpecifierQualifier(
                ast.TypeSpecifier(
                    ast.TypedefName(
                        ast.Identifier(
                            p.get_type().get_name()
                        )
                    )
                )
            )],
            ast.AbstractDeclarator.basic_ptr()
        )

        # idb->base[$entry_offset]
        get_from_idb: CastExpression = ast.PostfixExpression.second_case(
            ast.PostfixExpression.fourth_case(
                ast.PrimaryExpression.identifier(
                    ast.Identifier('idb')
                ).as_(ast.PostfixExpression),
                ast.Identifier(f'base')
            ),
            ast.PrimaryExpression.identifier(
                ast.Identifier(f'${p.get_global_id()}')
            ).as_expression()
        ).as_(ast.CastExpression)

        if p.get_type() != base_type:
            arg: AssignmentExpression = ast.CastExpression.expr(
                typename_recast,
                get_from_idb
            ).as_(ast.AssignmentExpression)
        else:
            arg: AssignmentExpression = get_from_idb.as_(AssignmentExpression)

        args.append(arg)

    # We create a statement in the form of pic_OR(args)
    return [ast.ExpressionStatement(
        ast.PostfixExpression.call(
            function_name,
            args
        ).as_expression()
    ).as_statement()]