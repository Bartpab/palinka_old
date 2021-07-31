from ...model.automation import Plant
from ...model import ast
from ...model import damo

from . import system_builder

import itertools

def build_damo(plant: Plant) -> None:
    print("Build DAMO")
    plant.damo = damo.DataModel()
    
    system: System
    for system in plant.get_systems():
        imports: Iterator[Tuple[int, Data]] = map(lambda data: (damo.DataModelFlags.CONSUMER, data), system.get_imported_data())
        exports: Iterator[Tuple[int, Data]] = map(lambda data: (damo.DataModelFlags.PRODUCER, data), system.get_exported_data())
        
        for flag, data in itertools.chain(imports, exports):
            plant.damo.add(system, data, flag=flag)

def build(plant: Plant):
    build_damo(plant)
    systems: list[ast.automation.SystemDeclaration] = [system_builder.build(system) for system in plant.get_systems()]
    return ast.automation.PlantDeclaration(systems)

def build_plant_system(plant: Plant):
    pass
