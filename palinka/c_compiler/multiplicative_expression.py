from ..model import ast

def compile(node: ast.MultiplicativeExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    elif node.is_second_case():
        lh = dispatch(node.nodes[0], *args, **kwargs)
        op = dispatch(node.nodes[1], *args, **kwargs)
        rh = dispatch(node.nodes[2], *args, **kwargs)
        return f"{lh} {op} {rh}"
    else:
        raise Exception("Unknown case for MultiplicativeExpression.")