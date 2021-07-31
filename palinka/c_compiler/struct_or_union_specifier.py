from ..model import ast

def compile(node: ast.StructOrUnionSpecifier, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    if node.is_first_case():
        p0 = dispatch(node.nodes[0], *args, **kwargs)
        p1 = dispatch(node.nodes[1], *args, **kwargs)
        p2 = " ".join([dispatch(cnode, *args, **kwargs) for cnode in node.nodes[1:]])
        return f"{p0} {p1} {{\n{p2}\n}}"
    elif node.is_second_case():
        p0 = dispatch(node.nodes[0], *args, **kwargs)
        p1 = " ".join([dispatch(cnode, *args, **kwargs) for cnode in node])
        return f"{p0} {{\n{p1}\n}}"
    elif node.is_third_case():
        p0 = dispatch(node.nodes[0], *args, **kwargs)
        p1 = dispatch(node.nodes[1], *args, **kwargs)
        return f"{p0} {p1}"
    else:
        raise Exception("Unknown case for StructSpecifier")