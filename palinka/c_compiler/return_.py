from ..model import ast

def compile(node: ast.Return, *args, **kwargs):
    return "return"