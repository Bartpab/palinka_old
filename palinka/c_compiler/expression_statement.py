from ..model import ast

def compile(node: ast.ExpressionStatement, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    parts = []
    if node.nodes:
        parts.append(dispatch(node.nodes[0], *args, **kwargs))
    
    parts.append(";")

    return "".join(parts)