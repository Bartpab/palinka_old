from ..model import ast

def compile(node: ast.ShiftExpressionBinop, *args, **kwargs):
    return node.op