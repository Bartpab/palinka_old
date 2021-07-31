from __future__ import annotations

from collections.abc import Iterable
from typing import Union, Optional
from palinka.utils import Database, DatabaseIndex

class Topology:
  def __init__(self):
    self.systems = []
  
  def add_system(self, system):
    self.systems.append(system)
    return self

  def get_systems(self):
    return self.systems

class AutomationSystem:
  def __init__(self, name):
    self.attrib = {
      'name': name
    }
  
  def __contains__(self, key):
    return key in self.attrib    
  
  def __getitem__(self, key):
    return self.attrib[key]
  
  def __setitem__(self, key, value):
    self.attrib[key] = value

class Diagram:
  def __init__(self, tool_version, database_version, library_version, diagram_version, diagram_increment, 
                plan_id, plan_name, last_change_date, target_system, max_loc_id, connections, symbols, segments):
    
    self.attrib = {
      'tool_version': tool_version,
      'database_version': database_version,
      'library_version': library_version,
      'diagram_version': diagram_version,
      'diagram_increment': diagram_increment,
      'plan_id': plan_id,
      'plan_name': plan_name,
      'last_change_data': last_change_date,
      'target_system': target_system,
      'max_loc_id': max_loc_id,
      'connections': connections,
      'symbols': [],
      'segments': segments
    }

    symbol_db = Database(loc_id=DatabaseIndex(lambda symbol: symbol['loc_id'], unique=True))

    for symbol in symbols:
      symbol_db.add(symbol)
    
    self.attrib['symbols'] = symbol_db

  def __contains__(self, key):
    return key in self.attrib    
  
  def __getitem__(self, key) -> Union[str, list[Connection], list[Symbol], list [Segment]]:
    return self.attrib[key]
  
  def __setitem__(self, key, value):
    self.attrib[key] = value

  def segment(self, seg_id) -> Optional[Segment]:
    for seg in self['segments']:
      if seg['seg_id'] == seg_id:
        return seg
    
    return None
    
  def get_segments(self) -> Iterable[Segment]:
    return self['segments']

  def owned_segments(self, indexed=True)  -> Iterable[Segment]:
    if indexed:
      segments = {}
    else:
      segments = []
      
    for segment in self['segments']:
      if segment.is_owned(self['plan_id']):
        if indexed:
          segments[segment['seg_id']] = segment
        else:
          segments.append(segment)
    
    return segments
  
  def connections(self) -> Iterable[Connection]:
    return self['connections']
  
  def symbols(self, only_connected=False) -> Iterable[Symbol]:
    if only_connected:
      symbols = []
      for symbol in self['symbols']:
        for connection in self.connections():
          if connection.is_connecting_symbol(symbol):
            symbols.append(symbol)
            break
          
    else:
      symbols = self['symbols']
    
    return symbols
    
class Symbol:
  def __init__(self, inst_name, loc_id, seg_id, pic_id, pic_name, pic_version, guid, symbol_type, ports, 
                pic_version_guid, gen_variant, sub_gen_variant, comment, 
                openio_id, openio_ix, pic_graphic_version_guid, 
                sequence_fixed, sequence_predecessor):
    
    self.attrib = {
      'ports': Database(
        port_nr=DatabaseIndex(lambda port: port['port_nr'], unique=True)
      ),
      'inst_name': inst_name,
      'loc_id': loc_id,
      'seg_id': seg_id,
      'pic_id': pic_id,
      'pic_name': pic_name,
      'pic_version': pic_version,
      'guid': guid,
      'symbol_type': symbol_type,
      'pic_version_guid': pic_version_guid,
      'gen_variant': gen_variant,
      'sub_gen_variant': sub_gen_variant,
      'comment': comment,
      'sequence_fixed': sequence_fixed,
      'openio_id': openio_id,
      'openio_ix': openio_ix,
      'pic_graphic_version_guid': pic_graphic_version_guid,
      'sequence_predecessor': sequence_predecessor
    }

    for port in ports:
      self['ports'].add(port)

  def get_port_by_name(self, name):
    return next(filter(lambda p: p['port_name'] == name, self['ports']))

  def get_port_by_nr(self, port_nr):
    return next(filter(lambda p: p['port_nr'] == port_nr, self['ports']))

  def __contains__(self, key):
    return key in self.attrib    
 
  def __getitem__(self, key) -> Union[str, list[Port]]:
    return self.attrib[key]
  
  def __setitem__(self, key: str, value):
    self.attrib[key] = value

  def is_type(self, pic_name):
    return self['pic_name'] == pic_name
    
class Port:
  def __init__(self, **attrib):
    self.attrib = attrib
  
  def __contains__(self, key):
    return key in self.attrib
  
  def __getitem__(self, key):
    return self.attrib[key]
  
  def __setitem__(self, key, value):
    self.attrib[key] = value

class Param:
  def __init__(self, **attrib):
    self.attrib = attrib
  
  def __getitem__(self, key):
    return self.attrib[key]
  
  def __setitem__(self, key, value):
    self.attrib[key] = value

class GlobalConnection:
  def __init__(self, q_plan_id, q_seg_id, q_data_type, q_sub_type, z_plan_id, z_seg_id, z_data_type, z_sub_type, sig_name):
    self.attrib = {
      'q_plan_id': q_plan_id,
      'q_seg_id': q_seg_id,
      'q_data_type': q_data_type,
      'q_sub_type': q_sub_type,
      'z_plan_id': z_plan_id,
      'z_seg_id': z_seg_id,
      'z_data_type': z_data_type,
      'z_sub_type': z_sub_type,
      'sig_name': sig_name
    }
  
  def __getitem__(self, key):
    return self.attrib[key]
  
  def __setitem__(self, key, value):
    self.attrib[key] = value

  def get_sig_name(self):
    return self['sig_name']

  def get_target(self) -> dict[str, str]:
    return {
      'plan_id': self['z_plan_id'],
      'seg_id': self['z_seg_id'],
      'data_type': self['z_data_type']
    }

  def get_source(self) -> dict[str, str]:
    return {
      'plan_id': self['q_plan_id'],
      'seg_id': self['q_seg_id'],
      'data_type': self['q_data_type']
    }

class Connection:
  def __init__(self, loc_id, q_loc_id, q_port_nr, z_loc_id, z_port_nr, seg_id, darst, guid, global_connection):
    self.attrib = {
      'loc_id': loc_id,
      'q_loc_id': q_loc_id,
      'q_port_nr': q_port_nr,
      'z_loc_id': z_loc_id,
      'z_port_nr': z_port_nr,
      'seg_id': seg_id,
      'darst': darst,
      'guid': guid,
      'global_connection': global_connection
    }
  
  def __getitem__(self, key):
    return self.attrib[key]
  
  def __setitem__(self, key, value):
    self.attrib[key] = value
  
  def is_global_connection(self):
    return 'global_connection' in self.attrib and self.attrib['global_connection'] is not None
  
  def global_connection(self):
    return self.attrib['global_connection']
    
  def is_connecting_symbol(self, symbol):
    loc_id = symbol['loc_id']
    return self['q_loc_id'] == loc_id or self['z_loc_id'] == loc_id
  
  def is_target(self, symbol):
    return self['z_loc_id'] == symbol['loc_id']
  
  def is_source(self, symbol):
    return self['q_loc_id'] == symbol['loc_id']
  
class ASData:
  def __init__(self, seg_id, sequence_predecessor, sequence_fixed, 
                block_sequence_state, es_as, es_apf, es_vf, es_cycle, es_hw_cycle, es_package, es_package_group, es_comment,
                pcs7_res_id, pcs7_task, pcs7_gear, pcs7_phase, pcs7_comment, pcs7_extra_tasks, 
                pcs7_failsafe, pcs7_super_rtgroup, T3000_rt, T3000_cycle, T3000_F, T3000_FM458):
    
    self.attrib = {
      'seg_id': seg_id,
      'sequence_predecessor': sequence_predecessor,
      'sequence_fixed': sequence_fixed,
      'block_sequence_state': block_sequence_state,
      'es_as': es_as,
      'es_apf': es_apf,
      'es_vf': es_vf,
      'es_cycle': es_cycle,
      'es_hw_cycle': es_hw_cycle,
      'es_package': es_package,
      'es_package_group': es_package_group,
      'es_comment': es_comment,
      'pcs7_res_id': pcs7_res_id,
      'pcs7_task': pcs7_task,
      'pcs7_gear': pcs7_gear,
      'pcs7_phase': pcs7_phase,
      'pcs7_comment': pcs7_comment,
      'pcs7_extra_tasks': pcs7_extra_tasks,
      'pcs7_failsafe': pcs7_failsafe,
      'pcs7_super_rtgroup': pcs7_super_rtgroup,
      'T3000_rt': T3000_rt,
      'T3000_cycle': T3000_cycle,
      'T3000_F': T3000_F,
      'T3000_FM458': T3000_FM458
    }

  def __contains__(self, key):
    return key in self.attrib
  
  def __getitem__(self, key):
    return self.attrib[key]
  
  def __setitem__(self, key, value):
    self.attrib[key] = value
    
class Segment:
  def __init__(self, seg_id, seg_name, plan_id, plan_name, guid, description, fb, fb_defining_node, fkz, fkz_defining_node, om_display, as_data):
    self.attrib = {
      'seg_id': seg_id,
      'seg_name': seg_name,
      'plan_id': plan_id,
      'plan_name': plan_name,
      'guid': guid,
      'description': description,
      'fb': fb,
      'fb_defining_node': fb_defining_node,
      'fkz': fkz,
      'fkz_defining_node': fkz_defining_node,
      'om_display': om_display,
      'as_data': as_data
    }
  
  def __getitem__(self, key):
    return self.attrib[key]
  
  def __contains__(self, key):
    return key in self.attrib
  
  def __setitem__(self, key, value):
    self.attrib[key] = value
  
  def symbols(self):
    return self['symbols']
  
  def is_owned(self, plan_id):
    return self['plan_id'] == plan_id


