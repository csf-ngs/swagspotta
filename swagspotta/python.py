from .base import RendererBase
import typing
from .util import logger

class PythonRenderer(RendererBase):
  template_dir = 'python'
  models_tpl = 'models.py.j2'
  class_tpl = 'class.py.j2'
  ext = 'py'

  def render_class(self, classname, schema) -> typing.Tuple[typing.Text, typing.List[dict]]:
    def field_def(name: str, prop_def: dict):
      field = { 'name': name, 'is_reference': False, 'readonly': False, 'multi': False }
      if '$ref' in prop_def:
        ref = prop_def['$ref'].replace('#/definitions/', '').replace('Schema', '')
        field['type'] = ref
        field['is_reference'] = True
      elif prop_def.get('format') == 'date-time':
        field['type'] = 'datetime'
      elif prop_def['type'] == 'integer' or prop_def['type'] == 'long':
        field['type'] = 'int'
      elif prop_def['type'] == 'float':
        field['type'] = 'float'
      elif prop_def['type'] == 'object':
        field['type'] = 'dict'
      elif prop_def['type'] == 'array':
        ndef = field_def('', prop_def['items'])
        field['multi'] = True
        field['is_reference'] = ndef['is_reference']
        field['type'] = ndef['type']
        field['readonly'] = ndef['readonly']
      elif prop_def['type'] == 'string':
        field['type'] = 'str'
      elif prop_def['type'] == 'boolean':
        field['type'] = 'bool'
      else:
        field['type'] = prop_def['type']

      if prop_def.get('readOnly', False):
        field['readonly'] = True
      return field

    template = self.get_class_template(classname)
    fields = []
    for name, prop in schema.get('properties', {}).items():
      field = field_def(name, prop)
      fields.append(field)
    return template.render(classname=classname, fields=fields), fields