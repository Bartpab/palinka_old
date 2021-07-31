from ..model import ast

def compile(node: ast.DirectDeclarator, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    
    # <direct-declarator> ::= <identifier>
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    # <direct-declarator> ::= <declarator>
    elif node.is_second_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    # <direct-declarator> ::= <direct-declarator> [<constant-expression>?]
    elif node.is_third_case():
        n1 = dispatch(node.case[0], *args, **kwargs)
        n2 = dispatch(node.case[1], *args, **kwargs) if node.case[1] else ""
        return f"{n1}[{n2}]"
    # <direct-declarator> ::= <direct-declarator> (<parameter-list>)
    elif node.is_fourth_case():
        n1 = dispatch(node.case[0], *args, **kwargs)
        n2 = dispatch(node.case[1], *args, **kwargs)
        return f"{n1}({n2})"
    # <direct-declarator> ::= <direct-declarator> (<identifier>*)
    elif node.is_fifth_case():
        n1 = dispatch(node.case[0], *args, **kwargs)
        n2 = " ".join([dispatch(cnode, *args, **kwargs) for cnode in node.nodes[1:]])
        return f"{n1}({n2})"
    else:
        raise Exception("Unknown case for DirectDeclarator...")