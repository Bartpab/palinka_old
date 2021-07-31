from ..model import ast

def compile(node: ast.Break, *args, **kwargs):
    return "break"