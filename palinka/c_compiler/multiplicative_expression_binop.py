from ..model import ast

def compile(node: ast.MultiplicativeExpressionBinop, *args, **kwargs):
    return node.op