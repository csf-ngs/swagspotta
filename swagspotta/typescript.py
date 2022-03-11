from .base import RendererBase
from .util import logger
import typing


class TypescriptRenderer(RendererBase):
  @property 
  def template_dir(self): 
    return 'typescript'

  @property
  def models_tpl(self):
    return 'models.ts.j2'
  
  @property
  def class_tpl(self):
    return 'class.ts.j2'
  
  @property
  def ext(self):
    return 'ts'

  def render_class(self, classname, schema) -> typing.Tuple[typing.Optional[str], typing.List[dict]]:
    def field_def(name: str, prop_def: dict):
      field = { 'name': name, 'is_reference': False, 'readonly': False, 'multi': False }
      if '$ref' in prop_def:
        ref = prop_def['$ref'].replace('#/definitions/', '').replace('Schema', '')
        field['type'] = ref
        field['is_reference'] = True
      elif prop_def.get('format') == 'date-time':
        field['type'] = 'Date | null'
      elif prop_def['type'] == 'integer' or prop_def['type'] == 'float' or prop_def['type'] == 'long':
        field['type'] = 'number'
      elif prop_def['type'] == 'object':
        field['type'] = 'any'
      elif prop_def['type'] == 'array':
        ndef = field_def('', prop_def['items'])
        field['multi'] = True
        field['is_reference'] = ndef['is_reference']
        field['type'] = ndef['type']
        field['readonly'] = ndef['readonly']
      else:
        field['type'] = prop_def['type']

      if prop_def.get('readOnly', False):
        field['readonly'] = True
      return field

    template = self.get_class_template(classname)
    fields=[]
    for name, prop in schema.get('properties', {}).items():
      field = field_def(name, prop)
      fields.append(field)
    return template.render(classname=classname, fields=fields), fields