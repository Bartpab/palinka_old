import palinka.model.ast as ast
from ...model.symbol_table import SymbolTable

from ...utils import rec_find_all

def transform(node: ast.PrimaryExpression, *args, **kwargs):
    """
        If PrimaryExpression/Identifier($something), then replace it with PrimaryExpression/Constant(address in the symbol table behind something)
    """
    symbols: SymbolTable = kwargs['symbol_table']
    dispatch = kwargs['dispatcher']

    alias = list(map(lambda idt: idt.name, rec_find_all(lambda n: isinstance(n, ast.Identifier) and n.name.startswith('$'), node)))
    alias = "".join(alias[0][1:]) if alias else None

    if alias:
        entry = symbols.get(alias)
        if entry:
            addr = entry.get_offset()
            return ast.PrimaryExpression(ast.Constant(addr))
    
    # We do not have this special use case
    node.nodes = [dispatch(cnode, *args, **kwargs) for cnode in node]
    return node