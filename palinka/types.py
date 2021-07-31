from __future__ import annotations

class DataType:
    VALUE = 0
    PTR = 1
    REF = 2

    @staticmethod
    def from_type_id(type_id) -> DataType:
        if type_id in ["4", "9"]:
            return bool_type
        elif type_id in ["3", "8", "101", "1", "2", "12", "19", "0"]:
            return real_type
        else:
            raise Exception(f"Unknown type id {type_id}")

    def __init__(self, name, size, type=0):
        if len(name) == 0:
            raise Exception("Empty name")
        self.name = name
        self.size = size
        self.type = type
    
    def get_name(self):
        return self.name

    def is_value(self):
        return self.type == 0

    def as_value(self):
        return DataType(self.name, 1, DataType.VALUE)

    def as_ptr(self):
        raise Exception("Nope")
        return DataType(self.name, 1, DataType.PTR)

    def get_size(self):
        return self.size
    
    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name, self.size)) 
    
    def __str__(self):
        return self.name

base_type       = DataType('char', 1)
bool_type       = DataType('char', 1)
integer_type    = DataType('int', 2)
float_type      = DataType('float', 4)
real_type       = DataType('double', 8)

