from ..model import ast

def compile(node: ast.Goto, *args, **kwargs):
    return "goto"