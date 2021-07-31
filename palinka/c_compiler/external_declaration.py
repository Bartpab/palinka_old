from ..model import ast

def compile(node: ast.ExternalDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    return dispatch(node.nodes[0], *args, **kwargs)