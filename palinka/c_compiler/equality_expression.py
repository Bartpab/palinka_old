from ..model import ast

def compile(node: ast.EqualityExpression, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    
    # <equality-expression> ::= <relational-expression>
    if node.is_first_case():
        return dispatch(node.nodes[0], *args, **kwargs)
    # <equality-expression> ::= <equality-expression> <equality-expression-binop> <relational-expression>
    elif node.is_second_case():
        return " ".join([dispatch(cnode, *args, **kwargs) for cnode in node])
    else:
        raise Exception("Unknown case for EqualityExpression.")
         
