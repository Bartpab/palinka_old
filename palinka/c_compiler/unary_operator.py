from ..model import ast

def compile(node: ast.UnaryOperator, *args, **kwargs):
    return node.op