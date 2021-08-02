from __future__ import annotations

from typing import Optional, Union, Type, Union
from lxml import etree

from palinka.utils import Database, DatabaseIndex
from palinka.types import DataType, base_type

class SymbolTableEntry:
  def __init__(self, name: str, data_type: DataType):
    self.offset: int = 0
    self.name: str = name
    if data_type is None:
        raise Exception("data_type cannot be None.")
    self.type: DataType = data_type
  
  def get_offset(self):
      return self.offset

  def get_size(self):
      return self.type.get_size()

class SymbolTableSegment:
    def __init__(self, name: str):
        self.name    = name
        self.entries: Database[Union[SymbolTableEntry, SymbolTableSegment]] = Database(name=DatabaseIndex(lambda entry: entry.name, unique=True)) 
        self.offset  = 0
        self.size    = 0
        self.type = base_type
    
    def get_offset(self):
        return self.offset

    def get_size(self):
        return self.size

    def build(self):
        tail = 0
        size = 0
        
        for entry in self.entries:
            entry.offset = tail
            
            if isinstance(entry, SymbolTableSegment):
                entry.build()
                
            size += entry.get_size()
            tail += entry.get_size()
        
        self.size = size

    def __getitem__(self, name):
        return self.entries.get(name, index_name='name')

    def __contains__(self, name):
        return self.entries.contains(name, index_name='name')
    
class SymbolTable:
    def __init__(self):
        self.root = SymbolTableSegment('__global__')
        self.stack = [self.root]

    def get_size(self):
        return self.stack[0].get_size()

    def build(self):
        self.curr().build()

    def push(self, name: str):
        area = SymbolTableSegment(name)
        
        if name in self.curr() and isinstance(self.curr()[name], SymbolTableSegment):
            self.stack.append(self.curr()[name])
        
        elif name in self.curr() and not isinstance(self.curr()[name], SymbolTableSegment):
            raise Exception(f"A symbol table entry which is not a segment already exist with the same name {name}.")

        else:
            self.curr().entries.add(area)
            self.stack.append(area)

    def pop(self):
        self.stack.pop(-1)
    
    def curr(self) -> SymbolTableSegment:
        return self.stack[-1]

    def put(self, data_name: str, data_type: DataType):       
        if not isinstance(data_type, DataType):
            raise Exception("Expecting data_type to be an instance of DataType.")
        
        self.curr().entries.add(SymbolTableEntry(
            name=data_name, 
            data_type=data_type
        ))

    def get(self, data_path: str) -> Optional[Union[SymbolTableEntry, SymbolTableSegment]]:
        stack = data_path.split("/")
        
        if len(stack) == 2:
            segment = self.get_(stack[0])
            
            if segment:
                return segment[stack[1]]

            return None

        else:
            return self.get_(data_path)
            

    def get_(self, data_name: str) -> Optional[Union[SymbolTableEntry, SymbolTableSegment]]:
        stack = self.stack[:]

        while stack:
            area = stack.pop(-1)
            if data_name in area:
                return area[data_name]

        return None

def serialize(symbols: SymbolTable):
    return etree.tostring(_serialize(symbols.root), pretty_print=True)

def _serialize(segment_or_entry):
    if isinstance(segment_or_entry, SymbolTableEntry):
        return etree.Element("Entry", offset=str(segment_or_entry.offset), name=segment_or_entry.name, type=str(segment_or_entry.type), size=str(segment_or_entry.get_size()))
    else:
        node = etree.Element("Segment", offset=str(segment_or_entry.offset), name=segment_or_entry.name, type=str(segment_or_entry.type), size=str(segment_or_entry.get_size()))
        for entry in segment_or_entry.entries:
            node.append(_serialize(entry))
        return node