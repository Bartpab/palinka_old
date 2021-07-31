from ..model import ast

def compile(node: ast.AssignmentExpressionOp, *args, **kwargs):
    return node.op