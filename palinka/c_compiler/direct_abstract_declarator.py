from ..model import ast

def compile(node: ast.DirectAbstractDeclarator, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    # <direct-abstract-declarator> ::= ( <abstract-declarator> )
    if node.is_first_case():
        return "(" + dispatch(node.nodes[0], *args, **kwargs) + ")"
    # <direct-abstract-declarator> ::= <direct-abstract-declarator>? [<constant-expression>?]
    elif node.is_second_case():
        n1 = dispatch(node.case[0], *args, **kwargs) + " " if node.case[0] else ""
        n2 = " " + dispatch(node.case[1], *args, **kwargs) + " " if node.case[1] else ""
        return f"{n1}[{n2}]"
    # <direct-abstract-declarator> ::= <direct-abstract-declarator>? (<parameter-list>?)
    elif node.is_third_case():
        n1 = dispatch(node.case[0], *args, **kwargs) + " " if node.case[0] else ""
        n2 = " " + dispatch(node.case[1], *args, **kwargs) + " " if node.case[1] else ""
        return f"{n1}({n2})"        
    else:
        raise Exception("Uknown case for DirectAbstractDeclarator")