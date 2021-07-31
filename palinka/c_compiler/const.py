from ..model import ast

def compile(node: ast.Const, *args, **kwargs):
    return "const"