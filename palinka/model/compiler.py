from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Type, Optional, Any, Tuple

from palinka.utils import Database, DatabaseIndex, TwoDimensionalIndex
from palinka.types import DataType
from palinka.model.tec4 import Symbol, Segment

def data_type_to_size(type):
  if type == "char":
    return 1

class SymbolTableEntry:
  def __init__(self, name: str, data_type: Type[DataType], symbolink: Optional[str] = None):
    self.address: int = 0
    self.name: str = name
    self.type: Type[DataType] = data_type
    self.symbolink: Optional[str] = symbolink
  
  def is_symbolic(self):
    return self.symbolink is not None
  
  def get_real_entry(self):
    return self.symbolink

  def set_symbolink(self, entry_name: str):
      self.symbolink = entry_name

class SymbolTable:
  """ Represents the symbol table used to compile the Tec4 code """
  def __init__(self):
      self.entries: Database[SymbolTableEntry] = Database(name=DatabaseIndex(lambda entry: entry.name, unique=True))
      self.tail = 0

  def concat(self, table: SymbolTable):
    for entry in table.entries:
      self.entries.add(entry)

  def build(self, base: int = 0):
    """
      Build the symbolic table

      Set the addresses for each non-symbolic entry within the table, from base
      Then, set the address for each symbolic entry based on the real entry's address.
    """
    self.tail = base
    
    for entry in self.entries:
      if not entry.is_symbolic():
        entry.address = self.tail
        self.tail += entry.type.get_size()
    
    for entry in self.entries:
      if entry.is_symbolic():     
        entry.address = self.entries.get(entry.get_real_entry(), index_name="name").get_address()

  def put(self, name: str, data_type: Type[DataType], symbolink: Optional[str] = None):
    self.entries.add(SymbolTableEntry(
      name=name,
      data_type=data_type,
      symbolink=symbolink
    ))

  def get(self, name) -> SymbolTableEntry:
    return self.entries.get(key=name, index_name="name")

  def address(self, name) -> int:
    self.get(name).address

  def __iter__(self) -> Iterator[SymbolTableEntry]:
    return iter(self.entries)

class SegmentOutput:
  """ Represent a signal emitted by the segment """
  def __init__(self, data_type: Type[DataType], sig_name: str, source_symbol_id: str, source_port_nr: str, source_segment_id: str):
    self.source_segment_id = source_segment_id
    self.source_symbol_id = source_symbol_id
    self.source_port_nr = source_port_nr
    self.data_type = data_type
    self.sig_name = sig_name
  
  def external_name(self) -> str:
    return f"{self.source_segment_id}:{self.sig_name}"
  
  def internal_name(self) -> str:
    return f"{self.source_segment_id}:{self.source_symbol_id}:{self.source_port_nr}"

  def as_data(self) -> SegmentData:
      return SegmentData(self.external_name(), self.data_type)

class SegmentInternalConnection:
  def __init__(self, seg_id, z_loc_id, z_port_nr, q_loc_id, q_port_nr):
    self.seg_id = seg_id
    self.target_loc_id = z_loc_id
    self.source_loc_id = q_loc_id
    self.target_port_nr = z_port_nr
    self.source_port_nr = q_port_nr
  
  def names(self) -> Tuple[str, str]:
    return (
      f"{self.seg_id}:{self.source_loc_id}:{self.source_port_nr}",
      f"{self.seg_id}:{self.target_loc_id}:{self.target_port_nr}"
    )

class SegmentData:
    def __init__(self, name: str, data_type: Type[DataType]):
      self.type: Type[DataType] = data_type
      self.name: str = name

class SegmentInput:
  """ Represent a segment input """
  def __init__(self, source_segment_id, sig_name, data_type, target_symbol_id, target_port_nr, target_segment_id):
    self.source_segment_id = source_segment_id
    self.sig_name = sig_name
    self.data_type = data_type
    self.target_symbol_id = target_symbol_id
    self.target_port_nr = target_port_nr
    self.target_segment_id = target_segment_id
  
  def external_name(self) -> str:
    return f"{self.source_segment_id}:{self.sig_name}"
 
  def internal_name(self) -> str:
    return f"{self.target_segment_id}:{self.target_symbol_id}:{self.target_port_nr}"

  def as_data(self) -> SegmentData:
      return SegmentData(self.external_name(), self.data_type)

  def match(self, output) -> bool:
      return self.external_name() == output.external_name()

class SegmentCompilerContext:
  def __init__(self, data):
    self.data: Segment = data
    self.symbols = []
    self.connections = []
    self.outputs = []
    self.inputs = []
    self.symbol_table = SymbolTable()

  def symbols(self) -> Iterable[Symbol]:
    return self.symbols

class CommunicationLink:
    """
      Represent a communication link between two systems
    """
    def __init__(self, source: str, target: str, data: dict[str, Any]):
      self.source = source
      self.target = target
      self.data = data 

class SystemCompilerContext:
  def __init__(self, name: str):
    self.name: str = name

class AutomationSystemCompilerContext(SystemCompilerContext):
  def __init__(self, name, data):
    SystemCompilerContext.__init__(self, name)
    self.data = data
    self.segment_contexts = []
    self.as_as_links = []
    self.symbol_table = SymbolTable()
  
  def add_segment_context(self, segment_context):
    self.segment_contexts.append(segment_context)
  
  def get_segment_contexts(self):
    return self.segment_contexts

  def add_inter_as_link(self, link):
    self.as_as_links.append(link)

  def get_inter_as_links(self) -> Iterable[CommunicationLink]:
    return self.as_as_links

  def outputs(self) -> Iterator[SegmentOutput]:
    for segment in self.segment_contexts:
      for output in segment.outputs:
        yield output
  
  def inputs(self) -> Iterator[SegmentInput]:
    for segment in self.segment_contexts:
      for input in segment.inputs:
        yield input    

class TopologyCompilerContext:
  def __init__(self):
    self.systems = []
  
  def __getitem__(self, key) -> Type[SystemCompilerContext]:
    return next(filter(lambda sys_ctx: sys_ctx.name == key), self.systems)

  def add_system(self, system: Type[SystemCompilerContext]):
    self.systems.append(system)
  
  def get_systems(self) -> Iterable[Type[SystemCompilerContext]]:
    return self.system_contexts

class CompilerContext:
  def __init__(self):
    self.topology = TopologyCompilerContext()

  def get_topology(self) -> TopologyCompilerContext:
    return self.topology

