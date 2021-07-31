from palinka.c_compiler import dispatch
from ..model import ast

def compile(node: ast.Enumerator, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    # <enumerator> ::= <identifier>
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    # <enumerator> ::= <identifier> = <constant-expression>
    elif node.is_second_case():
        parts = [dispatch(cnode, *args, **kwargs) for cnode in node]
        return f"{parts[0]} = {parts[1]}"
    else:
        raise Exception("Unknown case for Enumerator")