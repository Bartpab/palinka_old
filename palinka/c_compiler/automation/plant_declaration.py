import palinka.model.ast as ast
from ...model.symbol_table import SymbolTable

from palinka.utils import TextBuilder as TB

def compile(node: ast.automation.PlantDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']

    tb = TB()

    tb.add("/// BEGIN DIRECTORY plant ///")
    tb.add("\n".join([dispatch(cnode, *args, **kwargs) for cnode in node]))
    tb.add("/// END DIRECTORY ///")

    return str(tb)

def build_symbol_table(node: ast.automation.PlantDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    symbols: SymbolTable = kwargs['symbol_table']
    symbols.push('plant')
    
    for cnode in node:
        dispatch(cnode, *args, **kwargs)
    
    symbols.pop()

def transform(node: ast.automation.PlantDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    symbols: SymbolTable = kwargs['symbol_table']
    symbols.push('plant')
    node.nodes = [dispatch(cnode, *args, **kwargs) for cnode in node]
    symbols.pop()
    return node