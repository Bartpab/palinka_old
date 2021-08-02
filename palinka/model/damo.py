from typing import Optional, Iterator

from palinka.model.automation import Data
from palinka.model.automation import System
from palinka.utils import Database, DatabaseIndex, TwoDimensionalIndex
from palinka.types import DataType

class DataModelEntry:
  def __init__(self, system: System, data: Data, flag: int):
    self.system: System  = system
    self.data = data
    self.flag = flag
  
  def get_data(self) -> Data:
    return self.data

  def get_system(self) -> System:
    return self.system

  def get_id(self):
    return self.data.get_id()
  
  def __str__(self):
    return f"<DAMO>: {self.get_system()}, {self.get_data()}, {'producer' if DataModelFlags.PRODUCER == self.flag else 'consumer'}"

class DataModelFlags:
  CONSUMER: int = 0b0
  PRODUCER: int = 0b1

class DataModel:
  def __init__(self):
    self.entries: Database[DataModelEntry] = Database(
        #system_name=DatabaseIndex(lambda entry: entry.system_name),
        id=DatabaseIndex(lambda entry: entry.get_id()),
        composite_system_data=TwoDimensionalIndex(lambda entry: (entry.get_system(), entry.get_id()), unique=True),
        composite_data_pc=TwoDimensionalIndex(lambda entry: (entry.get_id(), entry.flag & 0b1)),
        composite_system_pc=TwoDimensionalIndex(lambda entry: (entry.get_system(), entry.flag & 0b1))
    )

  def get_data_names(self) -> Iterator[str]:
      return self.entries.get_indexer('id').get_indexes()

  def get_producer(self, data_id: str) -> Optional[DataModelEntry]:
    for entry in self.entries:
      if entry.get_id() == data_id and entry.flag == DataModelFlags.PRODUCER:
        return entry
    
    return None

  def get_consumers(self, data_id: str) -> Iterator[DataModelEntry]:
    for entry in self.entries:
      if entry.get_id() == data_id and entry.flag == DataModelFlags.CONSUMER:
        yield entry
    
  def __iter__(self):
    return iter(self.entries)

  def __getitem__(self, data_id):
    return self.entries.get(data_id, index_name='id')

  def contains(self, system: System, data_id: str) -> bool:
      return self.entries.contains(key=(system, data_id), index_name='composite_system_data')

  def add(self, system: System, data: Data, flag: int = 0) :
    """
      system_id: str of the system managing the data
      data_id: str of the data
      data_type: Type of the data
      flag: 0b1:
        - First byte: 0 = Consumer, 1 = Producer
    """
    if not self.contains(system, data.get_id()):
      self.entries.add(
        DataModelEntry(
          system=system,
          data=data,
          flag=flag
        )
      )