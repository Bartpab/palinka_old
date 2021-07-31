from ..model import ast

def compile(node: ast.String, *args, **kwargs):
    return f'"{node.value}"'