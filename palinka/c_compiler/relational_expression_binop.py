from ..model import ast

def compile(node: ast.RelationalExpressionBinop, *args, **kwargs):
    return node.op