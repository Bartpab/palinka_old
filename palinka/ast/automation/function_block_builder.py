from __future__ import annotations
from palinka.model.ast.assignment_expression import AssignmentExpression
from palinka.model.ast.identifier import Identifier
from palinka.model.ast.cast_expression import CastExpression

from palinka.types import base_type

from ...model.automation import FunctionBlock
from ...model.tec4 import Symbol
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
                # From the idb we get a pointer, we need to dereference to assign values
                # *lh_ptr = *rh_ptr
                lh = ast.UnaryExpression.unary(
                    ast.UnaryOperator('*'), 
                    ast.PrimaryExpression.identifier(
                        ast.Identifier(f'${c.get_target().get_global_id()}')
                    ).as_(ast.CastExpression)
                ).as_(ast.ConditionalExpression)
                
                rh = ast.UnaryExpression.unary(
                    ast.UnaryOperator('*'), 
                    ast.PrimaryExpression.identifier(
                        ast.Identifier(f'${c.get_source().get_global_id()}')
                    ).as_(ast.CastExpression)
                ).as_(ast.AssignmentExpression)
                
                op = ast.AssignmentExpression('=')
                
                statements.append(
                    ast.ExpressionStatement(
                        ast.AssignmentExpression.expr(
                            lh,
                            '=',
                            rh
                        )
                    ).as_statement()
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
            ast.PostfixExpression.fifth_case(
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