from ..model import ast

def compile(node: ast.If, *args, **kwargs):
    return "if"