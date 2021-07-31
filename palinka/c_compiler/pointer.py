from ..model import ast

def compile(node: ast.Pointer, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    parts = [dispatch(cnode, *args, **kwargs) for cnode in node]
    return "*" + " ".join(parts)