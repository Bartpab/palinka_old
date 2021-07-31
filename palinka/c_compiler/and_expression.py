from ..model import ast

def compile(node: ast.AndExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    # <and-expression> ::= <equality-expression>
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    # <and-expression> ::= <and-expression> & <equality-expression>
    else:
        lh = dispatch(node.nodes[0], *args, **kwargs)
        rh = dispatch(node.nodes[1], *args, **kwargs)
        return f"{lh} & {rh}"

