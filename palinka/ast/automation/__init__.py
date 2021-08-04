from . import plant

from typing import Iterator, Tuple

from ...model.automation import Plant, Data, System, DataLink, ScopedData
from ...model import ast
from ...model import damo
from ...utils import Database, TwoDimensionalIndex

import itertools

def build_damo(plant: Plant) -> None:
    plant.damo = damo.DataModel()
    
    system: System
    
    for system in plant.get_systems():
        imports: Iterator[ScopedData] = map(lambda scoped_data: (damo.DataModelFlags.CONSUMER, scoped_data), system.get_imported_data())
        exports: Iterator[ScopedData] = map(lambda scoped_data: (damo.DataModelFlags.PRODUCER, scoped_data), system.get_exported_data())
        
        for flag, scoped_data in itertools.chain(imports, exports):
            plant.damo.add(system, scoped_data.get_data(), namespace=scoped_data.get_namespace(), flag=flag)

def build_data_links(plant: Plant):
    """
        Based on the Data Model, we build the data links between systems
    """
    links: Database[DataLink] = Database(
        cmp=TwoDimensionalIndex(
            lambda link: (link.get_source(), link.get_target(), link.get_namespace()), 
            unique=True
        )
    )

    index = 0

    for entry_name in plant.damo.get_data_names():
        for producer in plant.damo.get_producers(entry_name):
            namespace: str = producer.get_namespace()
            producer_system: System = producer.get_system()
            data: Data= producer.get_data()
     
            consumers: list[damo.DataModelEntry] = plant.damo.get_consumers(entry_name, namespace)
                        
            for consumer in consumers:
                consumer_system = consumer.get_system()
                # Create the Data Link if it does not exist yet.
                if not links.contains((producer_system, consumer_system, namespace), index_name='cmp'):
                    links.add(DataLink(id=f"DLNK{index}", source=producer.get_system(), target=consumer.get_system(), namespace=namespace))
                    index += 1

                # Retrieve the Data Link and add the data in it
                link: link = links.get((producer.get_system(), consumer.get_system(), namespace), index_name='cmp')
                link.data.append(producer.get_data())


    # We now resolve the full path based on the plant's topology
    link: DataLink
    for link in links:
        path = plant.get_topology().find_shortest_path(link.get_source(), link.get_target(), link.get_namespace())
        
        if not path:
            raise Exception(f"No path exists from {link.get_source().get_id()} to {link.get_target().get_id()} in namespace {link.get_namespace()}.  ")

        link.set_path(path)
        plant.data_links.add(link)
        
        for system in link.get_path():
            system.add_data_link(link)


def build(plt: Plant) -> ast.automation.PlantDeclaration:
    build_damo(plt)
    build_data_links(plt)
    return plant.build(plt)
