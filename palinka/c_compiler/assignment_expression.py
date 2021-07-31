from ..model import ast

def compile(node: ast.AssignmentExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    
    parts = " ".join(dispatch(cnode, *args, **kwargs) for cnode in node)
    return parts