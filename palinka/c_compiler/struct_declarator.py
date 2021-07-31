from ..model import ast

def compile(node: ast.StructDeclarator, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    if node.is_first_case() or node.is_third_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    elif node.is_second_case():
        lh = dispatch(node.nodes[0], *args, **kwargs)
        rh = dispatch(node.nodes[1], *args, **kwargs)
        return f"{lh} : {rh}"