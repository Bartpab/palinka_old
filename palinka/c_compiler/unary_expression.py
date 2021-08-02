from ..model import ast

def compile(node: ast.UnaryExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    
    if node.is_fifth_case():
        return f"sizeof({dispatch(node.nodes[1], *args, **kwargs)})"

    return " ".join([dispatch(cnode, *args, **kwargs) for cnode in node])