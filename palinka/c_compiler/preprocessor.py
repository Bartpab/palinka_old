from ..model import ast

def compile(node: ast.Preprocessor, *args, **kwargs):
    dispatch = kwargs["dispatcher"]
    return "\n".join([dispatch(cnode, *args, **kwargs) for cnode in node])