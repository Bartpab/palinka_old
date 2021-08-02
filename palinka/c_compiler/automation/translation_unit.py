import palinka.model.ast as ast

def compile(node: ast.automation.TranslationUnit, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    return "\n".join([dispatch(cnode, *args, **kwargs) for cnode in node])

