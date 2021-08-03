from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Tuple, Optional

import palinka.model.damo as damo
from palinka.utils import Database, DatabaseIndex
from palinka.types import DataType
from palinka.helpers import c_id

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
    def __init__(self, data: Data, target: FunctionBlockPort, namespace: str = None):
        self.data = data
        self.namespace = namespace
        self.target = target
    
    def get_target(self) -> FunctionBlockPort:
        return self.target

    def get_data(self):
        return self.data

class FunctionPlanOutput:
    def __init__(self, data: Data, source: FunctionBlockPort, namespace: str = None):
        self.data = data
        self.namespace = namespace
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

    def create_input(self, function_plan_id: str, sig_name: str, target_block_id: str, target_port_id: str, namespace: str = None):
        tgt = self.get_block(target_block_id)
        tgtp = tgt.get_port(target_port_id)

        return self.add_input(
            FunctionPlanInput(
                FunctionPlanPlaceholder(
                    function_plan_id, 
                    sig_name, 
                    tgtp.get_type()
                ), tgtp, namespace
            )
        )

    def get_inputs(self) -> Iterator[FunctionPlanInput]:
        return self.inputs

    def create_output(self, sig_name: str, source_block_id: str, source_port_id: str, namespace: str = None):
        src = self.get_block(source_block_id)
        srcp = src.get_port(source_port_id)

        return self.add_output(
            FunctionPlanOutput(
                Signal(self, sig_name, srcp.get_type()),
                srcp,
                namespace
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
        return unique_everseen(map(lambda ipt: (ipt.namespace, ipt.get_data()), self.inputs))
    
    def get_exported_data(self) -> Iterator[Data]:
        return unique_everseen(map(lambda ipt: (ipt.namespace, ipt.get_data()), self.outputs))

class BaseSystem:
    BUS_SYSTEM = 1

    def __init__(self, name):
        self.name = name
    
    def get_function_plans(self):
        raise NotImplementedError()
    
    def has_data_links(self) -> bool:
        raise NotImplementedError()
    
    def get_data_links(self) -> Iterator[DataLink]:
        raise NotImplementedError()

class System:
    def __init__(self, id: str):
        self.address = None
        self.id = id
        self.function_plans: Database[FunctionPlan] = Database(id=DatabaseIndex(lambda fp: fp.get_id(), unique=True))
        self.data_links: Database[DataLink] = Database()

    def __hash__(self):
        return hash(self.get_id())

    def __str__(self):
        return f"System: {self.get_id()}"

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
    
    def get_relay_data_links(self) -> Iterable[DataLink]:
        return list(filter(lambda lnk: lnk.is_relay(self), self.get_data_links()))

    def get_exporting_data_links(self) -> Iterable[DataLink]:
        return list(filter(lambda lnk: lnk.is_source(self), self.get_data_links()))

    def get_importing_data_links(self) -> Iterable[DataLink]:
        return list(filter(lambda lnk: lnk.is_target(self), self.get_data_links()))

    def get_id(self):
        return str(self.id)

    def get_address(self):
        return self.address

    def get_slug_id(self):
        return c_id(self.get_id())

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
    def __init__(self, index: str, source: System, target: System, namespace: str = None):
        self.index = str(index)
        self.path = [source, target]
        self.source = source
        self.target = target
        self.namespace = namespace
        self.data: list[Data] = []

    def get_id(self):
        return self.index
    
    def get_namespace(self) -> str:
        return self.namespace

    def is_source(self, system: System) -> bool:
        return self.path[0] == system
    
    def is_relay(self, system: System) -> bool:
        try:
            idx = self.path.index(system)
            if idx >= len(self.path) -1 or idx <= 0:
                return False
            else:
                return True
        except ValueError:
            return False        

    def is_target(self, system: System) -> bool:
        return self.path[-1] == system

    def set_path(self, path: list[System]):
        if path[0] != self.get_source() and path[-1] != self.get_target():
            raise Exception("Invalid path, the source and target of the path must be the same as the data link.")
        
        self.path = path

    def get_path(self) -> list[System]:
        return self.path

    def add_relay(self, system: System):
        """
            Add a system as a relay of the data link's chain
        """
        self.path.insert(-1, system)

    def next(self, system: System) -> Optional[System]:
        try:
            idx = self.path.index(system)
            if idx >= len(self.path) -1:
                return None
            else:
                return self.path[idx + 1]
        except ValueError:
            return None

    def previous(self, system: System) -> Optional[System]:
        try:
            idx = self.path.index(system)
            if idx <= 0:
                return None
            else:
                return self.path[idx - 1]
        except ValueError:
            return None        

    def get_source(self) -> System:
        return self.source
    
    def get_target(self) -> System:
        return self.target
    
    def get_data(self) -> Iterator[Data]:
        return self.data

    def __hash__(self):
        return hash(self.get_source(), self.get_target())
    
    def __str__(self):
        return f"<DATA-LINK>: [{self.get_namespace()}] {self.get_source()} -> {self.get_target()} [{len(self.data)}]"

class TopologyEdge:
    def __init__(self, s0: System, s1: System, network: str):
        self.s0 = s0
        self.s1 = s1
        self.network = network
    
    def is_connecting(self, sys: System):
        return sys == self.s0 or sys == self.s1

    def other_one(self, sys: System):
        if self.s0 == sys:
            return self.s1
        else:
            return self.s0

    def get_network(self) -> str:
        return self.network

    def __str__(self) -> str:
        return f"<TOPOLOGY_EDGE>: [{self.network}] {self.s0} -- {self.s1}"

class Topology:
    def __init__(self):
        self.edges: Database[TopologyEdge] = Database()
    
    def connect(self, sys0: System, sys1: System, network: str):
        self.edges.add(TopologyEdge(sys0, sys1, network))

    def neighbors(self, sys, network: str):
        for edge in self.edges:
            if edge.is_connecting(sys) and edge.get_network() == network:
                yield edge

    def find_shortest_path(self, source: System, target: System, network: str) -> list[System]:
        visited = []
        stack = [(source, [])]
        
        while stack:
            sys, path = stack.pop(0)
            
            if sys not in visited:
                visited.append(sys)
            else:
                continue

            np = path[:] + [sys]

            # Found you
            if sys == target:
                return np
            
            for edge in self.neighbors(sys, network):
                ngh = edge.other_one(sys)
                stack.append((ngh, np[:]))

        return []

class Plant:
    def __init__(self):
        self.systems: Database[System] = Database(
            name=DatabaseIndex(lambda system: system.get_id(), unique=True)
        )
        self.topology = Topology()
        self.last_id = -1
        self.damo = damo.DataModel()
        self.data_links: Database[DataLink] = Database()

    def get_topology(self) -> Topology:
        return self.topology

    def connect(self, sys0: str, sys1: str, network: str) -> Plant:
        sys0 = self.get_system(sys0)
        sys1 = self.get_system(sys1)  
        self.topology.connect(sys0, sys1, network)
        return self

    def add_system(self, system: System) -> Plant:
        self.last_id += 1
        self.systems.add(system)
        system.address = self.last_id
        return self

    def get_system(self, name) -> Optional[System]:
        return self.systems.get(name, index_name='name')

    def get_systems(self) -> Iterator[System]:
        return self.systems