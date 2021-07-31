from ..model import ast

def compile(node: ast.EnumSpecifier, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    if node.is_first_case():
        parts = [dispatch(cnode, *args, **kwargs) for cnode in node]
        enum_list = ',\n'.join(parts[1:])
        return "enum {parts[0]} {{\n{enum_list}\n}}"
    
    elif node.is_second_case():
        parts = [dispatch(cnode, *args, **kwargs) for cnode in node]
        enum_list = ',\n'.join(parts)     
        return "enum {{\n}{enum_list}\n}}"

    elif node.is_third_case():
        parts = [dispatch(cnode, *args, **kwargs) for cnode in node]
        return "enum {parts[0]}"   
    
    else:
        raise Exception("Uknown case for EnumSpecifier")