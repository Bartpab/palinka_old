import palinka.model.ast as ast
from ...model.symbol_table import SymbolTable

from ...utils import rec_find_all

def transform(node: ast.PrimaryExpression, *args, **kwargs):
    """
        If PrimaryExpression/Identifier($something), then replace it with PrimaryExpression/Constant(address in the symbol table behind something)
    """
    symbols: SymbolTable = kwargs['symbol_table']
    dispatch = kwargs['dispatcher']

    if isinstance(node.nodes[0], ast.Identifier):
        identifier = node.nodes[0].name
        if identifier.startswith("$") or identifier.startswith("@"):
            op = identifier[0]
            identifier = "".join(identifier[1:])
            entry = symbols.get(identifier)
            if entry:
                if op == "$":
                    value = entry.get_offset()
                elif op == "@":
                    value = entry.get_size()
                return ast.PrimaryExpression(ast.Constant(value))
    
    # We do not have this special use case
    node.nodes = [dispatch(cnode, *args, **kwargs) for cnode in node]
    return node