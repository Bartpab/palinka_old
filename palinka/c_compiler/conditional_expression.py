from ..model import ast

def compile(node: ast.ConditionalExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    # <conditional-expression> ::= <logical-or-expression>
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    # <conditional-expression> ::= <logical-or-expression> ? <expression> : <conditional-expression>
    else:
        parts = [dispatch(cnode, *args, **kwargs) for cnode in node]
        return f'{parts[0]} ? {parts[1]} : {parts[2]}'