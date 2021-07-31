from ..model import ast

def compile(node: ast.IterationStatement, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    if node.is_first_case():
        expr = dispatch(node.nodes[0], *args, **kwargs)
        stmt = dispatch(node.nodes[1], *args, **kwargs)
        return f"while ({expr}) {stmt}"
    elif node.is_second_case():
        expr = dispatch(node.nodes[1], *args, **kwargs)
        stmt = dispatch(node.nodes[0], *args, **kwargs)      
        return f"do {stmt} while ({expr})"
    elif node.is_third_case():
        n1 = dispatch(node.case[0], *args, **kwargs) if node.case[0] else ""
        n2 = dispatch(node.case[1], *args, **kwargs) if node.case[1] else ""
        n3 = dispatch(node.case[2], *args, **kwargs) if node.case[2] else ""
        n4 = dispatch(node.case[3], *args, **kwargs)
        return f"for ({n1};{n2};{n3}) {n4}"
    else:
        raise Exception("Unknown case for IterationStatement.")

