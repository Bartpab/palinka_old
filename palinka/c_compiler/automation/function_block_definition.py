import palinka.model.ast as ast
from ...model.symbol_table import SymbolTable

def compile(node: ast.automation.FunctionBlockDefinition, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    return " ".join([dispatch(cnode, *args, **kwargs) for cnode in node.nodes[1:]])

def build_symbol_table(node: ast.automation.FunctionBlockDefinition, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    symbols: SymbolTable = kwargs['symbol_table']
    
    # Push a new segment
    symbols.push(node.get_name())

    
    for cnode in node:
        dispatch(cnode, *args, **kwargs)
    
    # Pop the segment
    symbols.pop()

def transform(node: ast.automation.FunctionBlockDefinition, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    symbols: SymbolTable = kwargs['symbol_table']
    symbols.push(node.get_name())
    node.nodes = [dispatch(cnode, *args, **kwargs) for cnode in node]
    symbols.pop()
    return node