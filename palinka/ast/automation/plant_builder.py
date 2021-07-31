from ...model.automation import Plant
from ...model import ast

from . import system_builder

def build(plant: Plant):
    systems: list[ast.automation.SystemDeclaration] = [system_builder.build(system) for system in plant.get_systems()]
    return ast.automation.PlantDeclaration(systems)

def build_plant_system(plant: Plant):
    pass
