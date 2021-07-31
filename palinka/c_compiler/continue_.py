from ..model import ast

def compile(node: ast.Continue, *args, **kwargs):
    return "continue"