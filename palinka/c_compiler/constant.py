from ..model import ast

def compile(node: ast.Constant, *args, **kwargs):
    return str(node.value)