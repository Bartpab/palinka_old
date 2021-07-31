from ..model import ast

def compile(node: ast.Volatile, *args, **kwargs):
    return "volatile"