from . import plant_builder
from . import system_builder
from . import function_plan_builder
from . import function_block_builder

from typing import Iterator, Tuple

from ...model.automation import Plant, Data, System, DataLink
from ...model import ast
from ...model import damo
from ...utils import Database, TwoDimensionalIndex
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

def build_data_links(plant: Plant):
    """
        Based on the Data Model, we build the data links between systems
    """
    links: Database[DataLink] = Database(
        composite_target_source=TwoDimensionalIndex(
            lambda link: (link.get_source(), link.get_target()), 
            unique=True
        )
    )

    for entry_name in plant.damo.get_data_names():
        producer: damo.DataModelEntry = plant.damo.get_producer(entry_name)
        consumers: list[damo.DataModelEntry] = plant.damo.get_consumers(entry_name)
                
        # Don't have the producer of the data, cannot do anything...
        if producer is None:
            continue
        
        for consumer in consumers:
            print(f'{producer.get_system().get_id()} -{entry_name}-> {consumer.get_system().get_id()}')
            # Create the Data Link if it does not exist yet.
            if not links.contains((producer.get_system(), consumer.get_system()), index_name='composite_target_source'):
                links.add(DataLink(source=producer.get_system(), target=consumer.get_system()))

            # Retrieve the Data Link and add the data in it
            link: link = links.get((producer.get_system(), consumer.get_system()), index_name='composite_target_source')
            link.data.append(producer.get_data())

    # We give a reference to the data link to each target/source systems
    link: DataLink
    for link in links:
        plant.data_links.add(link)
        link.get_source().add_data_link(link)
        link.get_target().add_data_link(link)

def build(plant: Plant) -> ast.automation.PlantDeclaration:
    build_damo(plant)
    build_data_links(plant)
    return plant_builder.build(plant)
