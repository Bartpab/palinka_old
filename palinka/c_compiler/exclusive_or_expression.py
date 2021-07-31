from ..model import ast

def compile(node: ast.ExclusiveOrExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    elif node.is_second_case():
        return " ".join([dispatch(cnode, *args, **kwargs) for cnode in node])
    else:
        raise Exception("Unknown case for ExclusiveOrExpression.")