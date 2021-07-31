import palinka.model.ast as ast

def compile(node: ast.automation.DataBlockDefinition, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    return ""