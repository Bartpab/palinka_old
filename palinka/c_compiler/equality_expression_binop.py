from ..model import ast

def compile(node: ast.EqualityExpressionBinop, *args, **kwargs):
    return node.op