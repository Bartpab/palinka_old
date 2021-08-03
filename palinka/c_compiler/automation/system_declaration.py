from palinka.c_compiler import dispatch
import palinka.model.ast as ast
from palinka.utils import TextBuilder as TB
from ...model.symbol_table import SymbolTable

def compile(node: ast.automation.SystemDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    tb = TB()
    
    sys_name = node.get_label()

    tb.add(f"/// BEGIN FILE {sys_name}.h ///")
    tb.add(dispatch(node.nodes[0], *args, **kwargs))
    tb.add("/// END FILE ///")

    tb.add(f"/// BEGIN FILE {sys_name}.c ///")
    tb.add(dispatch(node.nodes[1], *args, **kwargs))
    tb.add("/// END FILE ///")


    return str(tb)

def build_symbol_table(node: ast.automation.SystemDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    symbols: SymbolTable = kwargs['symbol_table']
    
    # Push a new segment
    symbols.push(node.get_id())

    for cnode in node:
        dispatch(cnode, *args, **kwargs)
    
    # Pop the segment
    symbols.pop()

def transform(node: ast.automation.SystemDeclaration, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    symbols: SymbolTable = kwargs['symbol_table']
    symbols.push(node.get_id())
    node.nodes = [dispatch(cnode, *args, **kwargs) for cnode in node]
    symbols.pop()
    return node