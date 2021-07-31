import palinka.model.ast as ast

def compile(node: ast.automation.ExternalDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    return dispatch(node.nodes[0], *args, **kwargs)