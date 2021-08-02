from __future__ import annotations

from collections.abc import Callable, Iterator, Iterable
from typing import TypeVar, Generic, Any, Union, Type, Tuple, Optional

class TextBuilder:
    def __init__(self):
        self.lines = []
        self.stack = ['']
        self.max_width = 100
    
    def push(self, prefix):
        self.stack.append(prefix)

    def pop(self):
        self.stack.pop(-1)

    def add(self, txt):
        if txt is None:
            return

        for line in txt.split("\n"):
            if len(line) > self.max_width:
                acc = ""
                stack = line.split(' ')
                
                while stack:
                    curr = stack.pop(0)
                    if len(acc + curr) > self.max_width:
                        self.lines.append(self.stack[-1] + acc)
                        acc = " " * 4 + curr
                    else:
                        acc += curr + " "
                
                if len(acc) > 0:
                    self.lines.append(self.stack[-1] + acc)    
    
            else:
                self.lines.append(self.stack[-1] + line)
    
    def __str__(self):
        return "\n".join(self.lines)

def rec_find_all(predicate, node):
    stack = [node] if not isinstance(node, list) else node[:]
    while stack:
        node = stack.pop(0)
        if predicate(node):
            yield node
        stack += list(iter(node))

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

T = TypeVar('T')
I = TypeVar('I')

I1 = TypeVar('I1')
I2 = TypeVar('I2')

TwoDimIndex = Generic[I1, I2]

class DatabaseIndex(Generic[I, T]):
    def __init__(self, getter: Callable[[T], I], unique: bool = False):
        self.getter: Callable[[T], I] = getter
        self.unique: bool = unique       
        self.table: dict[I, list[int]] = {}
        self.indexes: list[I] = []

    def unindex_by_pk(self, pk: int):
        to_remove = []
        
        for idx, value in self.table.items():
            if value == pk:
                to_remove.append(idx)
        
        for idx in to_remove:
            self.table[idx].remove(pk)
            if not self.table:
                del self.table[idx]
                self.indexes.remove(idx)

    def __contains__(self, key: I) -> bool:
        return key in self.table

    def __iter__(self) -> Tuple[I, int]:
        for key, pk in self.table.items():
            yield key, pk

    def index(self, entry: T, pk: int):
        idx: I = self.getter(entry)
        
        if self.unique and idx in self.table:
            raise Exception(f"Duplicated index: {str(idx)} !")
        
        if idx not in self.table:
            self.table[idx] = []
            self.indexes.append(idx)

        self.table[idx].append(pk)
    
    def reset(self):
        self.table = {}
        self.indexes = []
    
    def get_indexes(self) -> Iterator[I]:
        return self.indexes

    def __getitem__(self, index: I) -> Union[int, list[int]]:
        if self.unique:
            return self.table[index][0] if index in self.table else None
        else:
            return self.table[index] if index in self.table else None

class TwoDimensionalIndex(DatabaseIndex[Tuple[I1, I2], T]):
    def __init__(self, getter: Callable[[T], Tuple[I1, I2]], unique: bool = False):
        self.unique = unique
        self.getter = getter
        self.table: dict[I1, dict[I2, list[int]]] = {}
        self.indexes: list[Tuple[I1, I2]] = []
    
    def unindex_by_pk(self, pk: int):
        to_remove = []
        for k1, t in self.table.items():
            for k2, value in t.items():
                if value == pk:
                    to_remove.append((k1, k2))
        
        for k1, k2 in to_remove:
            self.table[k1][k2].remove(pk)
            if not self.table[k1][k2]:
                del self.table[k1][k2]
                self.indexes.remove((k1, k2))
            
            if not self.table[k1]:
                del self.table[k1]

    def __contains__(self, key: Tuple[I1, I2]) -> bool:
        return key[0] in self.table and key[1] in self.table[key[0]]

    def get_indexes(self) -> Iterator[Tuple[I1, I2]]:
        return self.indexes

    def index(self, entry: T, pk: int):
        idx = self.getter(entry)
        
        if idx[0] not in self.table:
            self.table[idx[0]] = {}
        
        if idx[1] in self.table[idx[0]] and self.unique:
           raise Exception(f"Duplicated index: {str(idx)} !")            

        if idx[1] not in self.table[idx[0]]:
            self.table[idx[0]][idx[1]] = []
            self.indexes.append(idx)

        self.table[idx[0]][idx[1]].append(pk)
    
    def __getitem__(self, key: TwoDimIndex[I1, I2]) -> int:
        return self.table[key[0]][key[1]][0] if self.unique else self.table[key[0]][key[1]]

class UnallocatedType:
    def __init__(self):
        pass

Unallocated = UnallocatedType()

class Cursor(Generic[T]):
    def __init__(self, iterator: Iterator[Tuple[int, T]]):
        self.iterator = iterator
        self.current_pk = None
        self.current = None

    def get_current_pk(self):
        return self.current_pk

    def __iter__(self):
        return self

    def __next__(self):
        self.current_pk, self.current = next(self.iterator)
        return self.current

    def items(self):
        return self.iterator
        
class Query(Generic[T]):
    def __init__(self, database: Database[T]):
        self.database = database
        self.iterator = enumerate(database.entries)
    
    def by_index(self, index_name: str, predicate: Callable[[Any], bool]):
        filtered_pks = set(map(lambda e: e[1], filter(lambda e: predicate(e[0]), iter(self.database.indexes[index_name]))))
        self.iterator = filter(lambda e: e[0] in filtered_pks, self.iterator)
        return self

    def by_attribute(self, attr_name: str, predicate: Callable[[Any], bool]):
        self.iterator = filter(lambda _, entry: predicate(getattr(entry, attr_name)))
        return self

    def __iter__(self):
        return self.execute()

    def find_all(self):
        return list(iter(self))

    def find_one(self, default=None) -> T:
        results = list(iter(self))
        if len(results) > 1:
            raise Exception("More than one result was found !")
        
        elif len(results) == 1:
            return next(results)
        
        else:
            return default

    def execute(self) -> Cursor[T]:
        return Cursor(self.iterator)

class Database(Generic[T]):
    def __init__(self, **indexes: dict[str, DatabaseIndex[T]]):
        self.entries: list[Union[T, UnallocatedType]] = []
        self.indexes: dict[str, DatabaseIndex[T]] = indexes
    
    def query(self) -> Query[T]:
        return Query(self)

    def build_index(self, index_name):
        """ (Re)build the index """
        self.indexes[index_name].reset()
        
        for pk, entry in enumerate(self.entries):
            self.indexes[index_name].index(entry, pk)

    def get_indexer(self, index_name) -> Type[DatabaseIndex[Any, T]]:
        return self.indexes[index_name]

    def get(self, key_or_keys: Union[Any, int], index_name=None) -> Union[Optional[T], list[T]]:
        """
            Retrieve an entry or a list of entries

            If index is unique, or no index is set, return an entry . If the index is not unique, returns a list of entries
        """
        if index_name:
            key_or_keys: Union[int, list[int]] = self.indexes[index_name][key_or_keys]
        
        
        if isinstance(key_or_keys, Iterable):
            return [self.entries[key] for key in filter(lambda k: k is not None, key_or_keys)]
        else:
            return self.entries[key_or_keys] if key_or_keys is not None else None

    def contains(self, key: Union[Any, int], index_name=None) -> bool:
        if index_name:
            return key in self.indexes[index_name]
        
        return key in self.entries  

    def __getitem__(self, key_or_keys: Union[int, Iterable[int]]) -> Union[T, list[T]]:
        if isinstance(key_or_keys, Iterable):
            return [self.entries[key] for key in key_or_keys]
        else:
            return self.entries[key_or_keys]

    def __iter__(self):
        return Cursor(enumerate(self.entries))

    def remove_by_value(self, entry: T):
        to_remove: list[int] = []
        
        cursor = iter(self)
        
        for stored in cursor:
            if stored == entry:
                to_remove.append(cursor.get_current_pk())
        
        # To avoid rebuilding the index each time, we unallocate the database case 
        for pk in to_remove:
            self.entries[pk] = Unallocated

        # We free every unallocated cases after the last valid primary key
        last_valid_pk = max(
            filter(lambda e: e[1] != Unallocated, enumerate(self)), 
            default=len(self.entries),
            key=lambda e: e[0]
        )[0]

        self.entries = self.entries[:last_valid_pk]
    
    def concat(self, entries: Iterable[T]):
        for entry in entries:
            self.add(entry)

    def is_empty(self):
        return len(self.entries) == 0

    def add(self, entry: T):
        pk = min(
            filter(lambda e: id(e[1]) == id(Unallocated), enumerate(self)), 
            default=(len(self.entries),),
            key=lambda e: e[0]
        )[0]
        
        # Index the entry 
        for indexer in self.indexes.values():
            indexer.index(entry, pk)

        if pk == len(self.entries):
            self.entries.append(entry)
        else:
            self.entries[pk] = entry

    def set_index(self, index_name: str, indexer: Type[DatabaseIndex[T]]):
        self.indexes[index_name] = indexer
        self.build_index(index_name)


