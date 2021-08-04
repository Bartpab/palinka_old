# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any
from .context import palinka
import os
import unittest
import random
import itertools

import palinka.model.automation as automation
import palinka.types as types

class UtilsTestSuite(unittest.TestCase):
    def test_database(self):
        from palinka.utils import Database, DatabaseIndex
        db: Database[dict[str, Any]] = palinka.utils.Database(index=DatabaseIndex(lambda entry: entry['index'], unique=True))

        db.add({'index': 0})
        db.add({'index': 1})

        assert db.contains(0, index_name='index')
        assert db.contains(1, index_name='index')

class EndToEndTestSuite(unittest.TestCase):
    """Basic test cases."""

    def binary_input(self, id, label):
        return automation.FunctionBlock(id, label, 'bin_input')\
                .add_port(automation.FunctionBlockPort('CH_1', 'Channel_1', 0, types.bool_type))\
                .add_port(automation.FunctionBlockPort('OPT01', 'Output:0', 0, types.bool_type))

    def binary_output(self, id, label):
        return automation.FunctionBlock(id, label, 'bin_output')\
                .add_port(automation.FunctionBlockPort('IPT01', 'Input:0', 0, types.bool_type))\
                .add_port(automation.FunctionBlockPort('CH_1', 'Channel_1', 0, types.bool_type))

    def test_e2e(self):
        # Create a fake plant
        plant = automation.Plant()\
            .add_system(automation.System("NET01"))\
            .add_system(
                automation.System("SYS01:IO:01")
                    .create_exported_data("FP01", "CH_1", types.bool_type, namespace='io')\
            )\
            .add_system(automation.System("SYS01:IM"))\
            .add_system(
                automation.System("SYS01")\
                    .add_function_plan(
                        automation.FunctionPlan("FP01", "Get_Binary_Input")\
                            .add_block(self.binary_input('B01', 'B01'))\
                            .create_input("FP01", "CH_1", "B01", "CH_1",    namespace="io")\
                            .create_output("X01", "B01", "OPT01",           namespace="plant_bus")
                    )
            )\
            .connect("SYS01", "SYS01:IM", network="io")\
            .connect("SYS01:IO:01", "SYS01:IM", network="io")\
            .add_system(
                automation.System('SYS02')\
                    .add_function_plan(
                        automation.FunctionPlan("FP02", "NEG")\
                            .add_block(
                                automation.FunctionBlock('B01', 'Block_01', 'neg')\
                                    .add_port(
                                        automation.FunctionBlockPort('IPT01', 'Input:0', 0, types.bool_type)
                                    )\
                                    .add_port(
                                        automation.FunctionBlockPort('OPT01', 'Output:0', 1, types.bool_type)
                                    )
                            )\
                          .add_block(
                                automation.FunctionBlock('B02', 'Block_02', 'neg')\
                                    .add_port(
                                        automation.FunctionBlockPort('IPT01', 'Input:0', 0, types.bool_type)
                                    )\
                                    .add_port(
                                        automation.FunctionBlockPort('OPT01', 'Output:0', 1, types.bool_type)
                                    )
                            )\
                            .create_connection("B01", "OPT01", "B02", "IPT01")\
                            .create_input("FP01", "X01", "B01", "IPT01", namespace="plant_bus")\
                            .create_output("X01", "B02", "OPT01", namespace="plant_bus")
                    )
            ).add_system(
                automation.System('SYS03')\
                    .add_function_plan(
                        automation.FunctionPlan("FP03", "Function_Plan_02")\
                            .add_block(
                                automation.FunctionBlock('B01', 'Block_01', 'bin_output')\
                                    .add_port(automation.FunctionBlockPort('IPT01', 'Input:0', 0, types.bool_type))
                            )\
                            .create_input("FP02", "X01", "B01", "IPT01", namespace="plant_bus")
                    )                
            )\
            .connect("SYS01", "NET01", network="plant_bus")\
            .connect("SYS02", "NET01", network="plant_bus")\
            .connect("SYS03", "NET01", network="plant_bus")

        # Parse the plant description into an AST
        ast = palinka.ast.automation.build(plant)

        # Compiling phase
        symbol_table = palinka.model.symbol_table.SymbolTable()
        raw_code = palinka.c_compiler.automation.compile(ast, symbol_table, [])

        # Create the project        
        palinka.writer.ProjectGenerator(os.path.join('tests', 'assets'))\
            .add_library(os.path.join("tests", "assets", "libs", "blocks"), "blocks")\
            .generate(raw_code, symbol_table)

if __name__ == '__main__':
    unittest.main()