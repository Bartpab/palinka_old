from ..model import ast

def compile(node: ast.LogicalOrExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    elif node.is_second_case():
        lh = dispatch(node.nodes[0], *args, **kwargs)
        rh = dispatch(node.nodes[1], *args, **kwargs)
        return f"{lh} || {rh}"
    else:
        raise Exception("Unknown case for LogicalAndExpression.")