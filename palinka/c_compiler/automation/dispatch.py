from palinka.model.ast.automation.plant_declaration import PlantDeclaration
import palinka.model.ast as ast
import palinka.c_compiler.dispatch as base_dispatcher

from . import external_declaration
from . import function_block_definition
from . import plant_declaration
from . import system_declaration
from . import translation_unit
from . import data_block_definition
from . import data_block_entry_declaration
from . import primary_expression

MODULE_DISPATCHER_MAP = [
    (ast.automation.ExternalDeclaration, external_declaration),
    (ast.automation.FunctionBlockDefinition, function_block_definition),
    (ast.automation.PlantDeclaration, plant_declaration),
    (ast.automation.SystemDeclaration, system_declaration),
    (ast.automation.TranslationUnit, translation_unit),
    (ast.automation.DataBlockDefinition, data_block_definition),
    (ast.automation.DataBlockEntryDeclaration, data_block_entry_declaration)
]

MODULE_SYMBOL_TABLE_DISPATCHER_MAP = [
    (ast.automation.PlantDeclaration, plant_declaration),
    (ast.automation.SystemDeclaration, system_declaration),
    (ast.automation.FunctionBlockDefinition, function_block_definition),
    (ast.automation.DataBlockEntryDeclaration, data_block_entry_declaration)
]

MODULE_TRANSFORM_DISPATCHER_MAP = [
    (ast.automation.PlantDeclaration, plant_declaration),
    (ast.automation.SystemDeclaration, system_declaration),
    (ast.automation.FunctionBlockDefinition, function_block_definition),
    (ast.PrimaryExpression, primary_expression)
]

COMPILER_DISPATCHER_MAP = base_dispatcher.build_dispatcher_map(MODULE_DISPATCHER_MAP, 'compile')
BUILD_SYMBOL_TABLE_DISPATCHER_MAP = base_dispatcher.build_dispatcher_map(MODULE_SYMBOL_TABLE_DISPATCHER_MAP, 'build_symbol_table')
TRANSFORM_DISPATCHER_MAP = base_dispatcher.build_dispatcher_map(MODULE_TRANSFORM_DISPATCHER_MAP, 'transform')

compiler_dispatch = base_dispatcher.build_dispatcher(COMPILER_DISPATCHER_MAP, fallback=base_dispatcher.compiler_dispatch)

def default_build_symbol_table_dispatch(node, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    for cnode in node:
        dispatch(cnode, *args, **kwargs)

build_symbol_table_dispatch = base_dispatcher.build_dispatcher(BUILD_SYMBOL_TABLE_DISPATCHER_MAP, fallback=default_build_symbol_table_dispatch)

def default_transform_dispatch(node, *args, **kwargs):
    dispatch = kwargs['dispatcher']
    node.nodes = [dispatch(cnode, *args, **kwargs) for cnode in node]
    return node

transform_dispatch = base_dispatcher.build_dispatcher(TRANSFORM_DISPATCHER_MAP, fallback=default_transform_dispatch)