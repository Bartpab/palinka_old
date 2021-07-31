from ..model import ast

def compile(node: ast.Initializer, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    elif node.is_second_case():
        il = dispatch(node.nodes[0], *args, **kwargs)
        return f"{{{il}}}"
    elif node.is_third_case():
        il = dispatch(node.nodes[0], *args, **kwargs)
        return f"{{{il},}}"
    else:
        raise Exception("Unknown case for Initializer.")