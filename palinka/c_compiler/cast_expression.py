from ..model import ast

def compile(node: ast.CastExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    # <cast-expression> ::= <unary-expression>
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    # <cast-expression> ::= ( <type_name> ) <cast-expression>
    else:
        n1 = dispatch(node.nodes[0], *args, **kwargs)
        n2 = dispatch(node.nodes[1], *args, **kwargs)
        return f"({n1}) {n2}"