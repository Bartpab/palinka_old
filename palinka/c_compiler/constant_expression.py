from ..model import ast

def compile(node: ast.ConstantExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    return " ".join([dispatch(cnode, *args, **kwargs) for cnode in node])