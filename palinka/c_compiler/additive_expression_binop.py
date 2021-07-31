from ..model import ast

def compile(node: ast.AdditiveExpressionBinop, *args, **kwargs):
    return node.op