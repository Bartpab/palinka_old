from os import dup
from ..model import ast

def compile(node: ast.Declarator, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    parts = " ".join([dispatch(cnode, *args, **kwargs) for cnode in node])
    return f"{parts}"

