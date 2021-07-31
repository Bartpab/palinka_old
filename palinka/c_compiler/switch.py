from ..model import ast

def compile(node: ast.Switch, *args, **kwargs):
    return "switch"