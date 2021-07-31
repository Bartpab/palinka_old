from ..model import ast

def compile(node: ast.SelectionStatement, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    
    if node.is_first_case():
        expr = dispatch(node.nodes[1], *args, **kwargs)
        stmt = dispatch(node.nodes[2], *args, **kwargs)
        return f"if ({expr}) {stmt}"

    elif node.is_second_case():
        expr = dispatch(node.nodes[1], *args, **kwargs)
        if_stmt = dispatch(node.nodes[2], *args, **kwargs)
        else_stmt = dispatch(node.nodes[3], *args, **kwargs)
        return f"if ({expr}) {if_stmt} else {else_stmt}"
    
    elif node.is_third_case():
        expr = dispatch(node.nodes[1], *args, **kwargs)
        stmt = dispatch(node.nodes[2], *args, **kwargs)
        return f"switch ({expr}) {stmt}"       
    
    else:
        raise Exception("Unknown case for SelectionStatement.")