import palinka.model.ast as ast
from ...model.symbol_table import SymbolTable

def compile(node: ast.automation.DataBlockEntryDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    return ""


def build_symbol_table(node: ast.automation.DataBlockEntryDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    symbols: SymbolTable = kwargs['symbol_table']
    symbols.put(node.name, node.type)