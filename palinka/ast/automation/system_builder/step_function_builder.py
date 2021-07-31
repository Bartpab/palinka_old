from ....model.automation import System
from ....model import ast

def build(system: System) -> ast.FunctionDefinition:
    """
        Build a the system's step function.

        void step_system_@system_name(System_t* sys)
        {
            ...
        }
    """
    func_type_specifiers: list[ast.DeclarationSpecifier] = [ast.DeclarationSpecifier(ast.TypeSpecifier(ast.Void()))]
    
    func_declarator: ast.Declarator = ast.Declarator.create(
        None,
        # step_system_@system.name(System_t* sys, DataBlock_t* idb)
        ast.DirectDeclarator.call(
            # step_system_@system.name
            ast.DirectDeclarator.identifier(ast.Identifier(f'step_system_{system.get_id()}')),
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


    return ast.FunctionDefinition.create(
        func_type_specifiers,
        func_declarator,
        [],
        build_step_function_statements(system)
    )

def build_step_function_statements(system: System) -> ast.CompoundStatement:
    declarations: list[ast.Declaration] = []
    statements: list[ast.Statement] = []

    for function_plan in system.get_function_plans():
        # We make the function block call statement.
        # FB call args are always (System_t* sys, DataBlock_t* idb)
        function_name: ast.PostfixExpression = ast.PrimaryExpression.identifier(ast.Identifier(f"fb_{function_plan.get_id()}")).as_(ast.PostfixExpression)
        function_args: list[ast.AssignmentExpression] = [
            ast.PrimaryExpression.identifier(ast.Identifier('sys')).as_(ast.AssignmentExpression)
        ]

        function_call: ast.Statement = ast.ExpressionStatement(
            ast.PostfixExpression.call(
                function_name,
                function_args
            ).as_expression()
        ).as_statement()

        statements += [
            function_call
        ]

    return ast.CompoundStatement.create(declarations, statements)



