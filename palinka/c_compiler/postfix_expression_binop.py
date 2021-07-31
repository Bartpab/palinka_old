from ..model import ast

def compile(node: ast.PostfixExpressionBinaryOp, *args, **kwargs):
    return node.op