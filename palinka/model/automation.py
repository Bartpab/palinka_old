from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Tuple, Optional

import palinka.model.damo as damo
from palinka.utils import Database, DatabaseIndex
from palinka.types import DataType

from more_itertools import unique_everseen
from itertools import chain

class Data:    
    def get_id(self):
        raise NotImplementedError()

    def get_type(self):
        raise NotImplementedError()

    def __hash__(self):
        return hash((self.get_id(), self.get_type()))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __str__(self):
        return f"Data: {self.get_id()}, {self.get_type()}"

class Placeholder(Data):
    def __init__(self, id: str, type: DataType):
        self.id = id
        self.type = type

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type
    
class FunctionPlanPlaceholder(Data):
    def __init__(self, function_plan_id: str, sig_name: str, type: DataType):
        self.id = f"{function_plan_id}:{sig_name}"
        self.type = type

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type

class Signal(Data):
    def __init__(self, source: FunctionPlan, sig_name: str, type: DataType):
        if source is None:
            raise Exception("Cannot be None")
        self.source = source
        self.sig_name = sig_name
        self.type = type
    
    def get_id(self):
        return f"{self.source.get_global_id()}:{self.sig_name}"

    def get_type(self):
        return self.type

class FunctionBlockPort:
    def __init__(self, id: str, label: str, order: int, type: DataType):
        self.block: Optional[FunctionBlock] = None
        
        self.id = id
        self.order = order
        self.label = label
        self.type = type

    def get_type(self):
        return self.type

    def get_id(self):
        return self.id

    def get_function_block(self):
        return self.block

    def get_global_id(self):
        block_gid = "" if not self.block else self.block.get_global_id()
        return f"{block_gid}:{self.get_id()}"

    def get_data(self) -> Data:
        return Placeholder(self.get_global_id(), self.type)

class FunctionBlock:
    def __init__(self, id: str, label: str, type: str):
        self.type = type
        self.id = id
        self.label = label
        self.function_plan: Optional[FunctionPlan] = None
        self.ports: Database[FunctionBlockPort] = Database(id=DatabaseIndex(lambda port: port.get_id(), unique=True))

    def get_class(self):
        return self.type

    def get_id(self):
        return self.id
    
    def get_label(self):
        return self.label

    def add_port(self, port: FunctionBlockPort):
        port.block = self
        self.ports.add(port)
        return self

    def get_port(self, id: str) -> Optional[FunctionBlockPort]:
        return self.ports.get(id, index_name='id')

    def get_ports(self) -> Iterator[FunctionBlockPort]:
        return self.ports

    def has_port(self, id: str) -> bool:
        return self.ports.contains(id, index_name='id')

    def get_function_plan(self) -> Optional[FunctionPlan]:
        return self.function_plan

    def get_global_id(self):
        fp_gid = "" if not self.function_plan else self.function_plan.get_global_id()
        return f"{fp_gid}:{self.get_id()}"

class FunctionBlockConnection:
    def __init__(self, source: FunctionBlockPort, target: FunctionBlockPort):
        self.source = source
        self.target = target
    
    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

class FunctionPlanInput:
    def __init__(self, data: Data, target: FunctionBlockPort):
        self.data = data
        self.target = target
    
    def get_target(self) -> FunctionBlockPort:
        return self.target

    def get_data(self):
        return self.data

class FunctionPlanOutput:
    def __init__(self, data: Data, source: FunctionBlockPort):
        self.data = data
        self.source = source

    def get_source(self) -> FunctionBlockPort:
        return self.source

    def get_data(self):
        return self.data

class FunctionPlan:
    """
        Represents a function plan, aka an automation task.

        I -> [B->IC->B] -> O
    """
    def __init__(self, id_, label):
        self.id = id_
        self.label = label

        self.blocks: Database[FunctionBlock]                = Database(id=DatabaseIndex(lambda block: block.get_id(), unique=True))
        self.connections: Database[FunctionBlockConnection] = Database()
        self.inputs: Database[FunctionPlanInput]            = Database()
        self.outputs: Database[FunctionPlanOutput]          = Database()

    def get_global_id(self):
        return self.get_id()

    def get_id(self):
        return self.id

    def add_block(self, block: FunctionBlock):
        block.function_plan = self
        self.blocks.add(block)
        return self
    
    def has_block(self, block_id: str) -> bool:
        return self.blocks.contains(block_id, index_name='id')
    
    def get_block(self, block_id: str) -> bool:
        return self.blocks.get(block_id, index_name='id')
    
    def set_blocks(self, blocks: list[FunctionBlock]) -> bool:
        self.blocks: Database[FunctionBlock] = Database(id=DatabaseIndex(lambda block: block.id, unique=True))
        for block in blocks:
            self.blocks.add(block)

    def get_blocks(self) -> Iterator[FunctionBlockPort]:
        for block in self.blocks:
            yield block

    def create_connection(self, source_block_id: str, source_port_id: str, target_block_id: str, target_port_id: str):
        src = self.get_block(source_block_id)
        tgt = self.get_block(target_block_id)

        srcp = src.get_port(source_port_id)
        tgtp = tgt.get_port(target_port_id)

        self.add_connection(FunctionBlockConnection(srcp, tgtp))
        return self

    def add_connection(self, conn: FunctionBlockConnection):
        self.connections.add(conn)
    
    def get_connections(self):
        for conn in self.connections:
            yield conn

    def add_input(self, ipt: FunctionPlanInput):
        self.inputs.add(ipt)
        return self

    def create_input(self, function_plan_id: str, sig_name: str, target_block_id: str, target_port_id: str):
        tgt = self.get_block(target_block_id)
        tgtp = tgt.get_port(target_port_id)

        return self.add_input(
            FunctionPlanInput(
                FunctionPlanPlaceholder(
                    function_plan_id, 
                    sig_name, 
                    tgtp.get_type()
                ), tgtp
            )
        )

    def get_inputs(self) -> Iterator[FunctionPlanInput]:
        return self.inputs

    def create_output(self, sig_name: str, source_block_id: str, source_port_id: str):
        src = self.get_block(source_block_id)
        srcp = src.get_port(source_port_id)

        return self.add_output(
            FunctionPlanOutput(
                Signal(self, sig_name, srcp.get_type()),
                srcp
            )
        )

    def add_output(self, opt: FunctionPlanOutput):
        self.outputs.add(opt)
        return self

    def get_outputs(self) -> Iterator[FunctionPlanOutput]:
        return self.outputs

    def get_internal_data(self):
        for block in self.blocks:
            for port in block.ports:
                yield port.get_data()

    def get_imported_data(self) -> Iterator[Data]:
        return unique_everseen(map(lambda ipt: ipt.get_data(), self.inputs))
    
    def get_exported_data(self) -> Iterator[Data]:
        return unique_everseen(map(lambda ipt: ipt.get_data(), self.outputs))

class System:
    def __init__(self, name: str):
        self.name = name
        self.function_plans: Database[FunctionPlan] = Database(id=DatabaseIndex(lambda fp: fp.get_id(), unique=True))
        self.data_links: Database[DataLink] = Database()
    
    def __hash__(self):
        return hash(self.get_name())

    def __str__(self):
        return f"System: {self.get_name()}"

    def add_function_plan(self, fp: FunctionPlan):
        self.function_plans.add(fp)
        return self 
        
    def get_function_plans(self) -> Iterator[FunctionPlan]:
        return self.function_plans
    
    def has_data_links(self):
        return not self.data_links.is_empty()

    def add_data_link(self, data_link: DataLink):
        self.data_links.add(data_link)
    
    def get_data_links(self) -> Iterator[DataLink]:
        return self.data_links

    def get_id(self):
        return self.name

    def get_name(self):
        return self.name

    def get_imported_data(self) -> Iterator[Data]:
        return unique_everseen(
            chain(*[
                function.get_imported_data() for function in self.function_plans
            ])           
        )

    def get_exported_data(self) -> Iterator[Data]:
        return unique_everseen(
            chain(*[
                function.get_exported_data() for function in self.function_plans
            ])           
        )    

class DataLink:
    def __init__(self, source: System, target: System):
        self.source = source
        self.target = target
        self.data: list[Data] = []

    def get_source(self) -> System:
        return self.source
    
    def get_target(self) -> System:
        return self.target
    
    def get_data(self) -> Iterator[Data]:
        return self.data

    def __hash__(self):
        return hash(self.get_source(), self.get_target())
    
    def __str__(self):
        return f"<DATA-LINK>: {self.get_source()} -> {self.get_target()} [{len(self.data)}]"

class Plant:
    def __init__(self):
        self.systems: Database[System] = Database(
            name=DatabaseIndex(lambda system: system.get_name(), unique=True)
        )
        self.last_id = -1
        self.damo = damo.DataModel()
        self.data_links: Database[DataLink] = Database()
    
    def add_system(self, system: System):
        self.last_id += 1
        self.systems.add(system)
        system.index = self.last_id
        return self

    def get_system(self, name):
        return self.systems.get(name, index_name='name')

    def get_systems(self) -> Iterator[System]:
        return self.systems