import sys 
from typing import Optional

import palinka.model.ast as ast
import palinka.model.symbol_table as symbol_table

from .dispatch import compiler_dispatch, build_symbol_table_dispatch, transform_dispatch


def build_symbol_table(root: ast.automation.PlantDeclaration, symbols: symbol_table.SymbolTable):
    build_symbol_table_dispatch(
        root, 
        dispatcher=build_symbol_table_dispatch, 
        symbol_table=symbols
    )
    symbols.build()

def transform(root: ast.automation.PlantDeclaration, symbols: symbol_table.SymbolTable):
    return transform_dispatch(root, dispatcher=transform_dispatch, symbol_table=symbols)

def compile(root: ast.automation.PlantDeclaration, symbol_table: Optional[symbol_table.SymbolTable]) -> str:
    """
        Compile the automation's AST
    """
    symbol_table = symbol_table or symbol_table.SymbolTable()
    build_symbol_table(root, symbol_table)
    root = transform(root, symbol_table)
    return compiler_dispatch(root, dispatcher=compiler_dispatch)

    