from ..model import ast

def compile(node: ast.SizeOf, *args, **kwargs):
    return "sizeof"