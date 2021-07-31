from lxml import etree

def _get_xml_node(node):
    xml_node = etree.Element(node.__class__.__name__)
    
    for cnode in node:
        xml_node.append(_get_xml_node(cnode))
    
    return xml_node

def serialize_xml(node):
    return etree.tostring(
        _get_xml_node(node), 
        pretty_print=True
    )
