from ..model import ast

def compile(node: ast.PostfixExpressionSingleOp, *args, **kwargs):
    return node.op