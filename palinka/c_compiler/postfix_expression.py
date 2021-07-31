from ..model import ast

def compile(node: ast.PostfixExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    elif node.is_second_case():
        lh = dispatch(node.nodes[0], *args, **kwargs)
        rh = dispatch(node.nodes[1], *args, **kwargs)
        return f"{lh}[{rh}]"
    elif node.is_third_case():
        lh = dispatch(node.nodes[0], *args, **kwargs)
        rh = ", ".join([dispatch(cnode, *args, **kwargs) for cnode in node.nodes[1:]])
        return f"{lh}({rh})"
    elif node.is_fourth_case() or node.is_fifth_case() or node.is_sixth_case() or node.is_seventh_case():
        return "".join([dispatch(cnode, *args, **kwargs) for cnode in node])
    else:
        raise Exception("Unknown case for PostfixExpression")
    