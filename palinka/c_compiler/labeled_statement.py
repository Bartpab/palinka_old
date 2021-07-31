from ..model import ast

def compile(node: ast.LabeledStatement, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    
    if node.is_first_case():
        lh = dispatch(node.nodes[0], *args, **kwargs)
        rh = dispatch(node.nodes[1], *args, **kwargs)
        return f"{lh}: {rh}"
    elif node.is_second_case():
        lh = dispatch(node.nodes[0], *args, **kwargs)
        rh = dispatch(node.nodes[1], *args, **kwargs)
        return f"case {lh}: {rh}"
    elif node.is_third_case():
        rh = dispatch(node.nodes[0], *args, **kwargs)
        return f"default: {rh}"
    else:
        raise Exception("Unknown case for LabeledStatement")