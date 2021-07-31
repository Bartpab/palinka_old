from ..model import ast

def compile(node: ast.StructDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    p0 = " ".join([dispatch(cnode, *args, **kwargs) for cnode in node.case[0]])
    p1 = ", ".join([dispatch(cnode, *args, **kwargs) for cnode in node.case[1]])
    return f"{p0} {p1}"