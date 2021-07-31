from ..model import ast

def compile(node: ast.Identifier, *args, **kwargs):
    return node.name