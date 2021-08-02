from ..model import ast

def compile(node: ast.Include, *args, **kwargs):
    dispatch = kwargs["dispatcher"]
    if node.internal:
        return f'#include "{dispatch(node.nodes[0], *args, **kwargs)}"'
    else:
        return f'#include <{dispatch(node.nodes[0], *args, **kwargs)}>'