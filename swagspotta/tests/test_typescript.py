from contextlib import contextmanager
import typing
from .base import TestBase
from swagspotta.typescript import TypescriptRenderer
import os


class TestTypescript(TestBase):
  def setUp(self):
    self.renderer = TypescriptRenderer()

  @contextmanager
  def _render_models(self):
    defs = self._load_example()
    src = self.renderer.render(classes=[
      'User', 'Category', 'Tag', 'Pet', 'Order'
    ], definitions=defs['definitions'])
    self.assertIsNotNone(src)
    src=typing.cast(str, src)

    with open(os.path.join(self.get_self_dir(), 'model.ts'), 'w') as outfh:
      outfh.write(src)
    yield

    os.unlink(os.path.join(self.get_self_dir(), 'model.ts'))

  def test_simple(self):
    defs = self._load_example()
    _, fields = self.renderer.render_class('Category', defs['definitions']['Category'])
    self.assertCountEqual(['id', 'name'], [ f['name'] for f in fields ])
    id_field = next(filter(lambda f: f['name']=='id', fields))
    self.assertDictEqual({
      'name': 'id',
      'is_reference': False,
      'readonly': False,
      'multi': False,
      'type': 'number'
    }, id_field)
  
  def test_types_int(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'integer'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'number',
      'is_reference': False,
    }, fields[0])

  def test_types_str(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'string'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'string',
      'is_reference': False,
    }, fields[0])
  
  def test_types_float(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'float'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'number',
      'is_reference': False,
    }, fields[0])

  def test_types_long(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'long'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'number',
      'is_reference': False,
    }, fields[0])

  def test_types_datetime(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'string',
          'format': 'date-time',
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'Date | null',
      'is_reference': False,
    }, fields[0])

  def test_types_number(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'number'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'number',
      'is_reference': False,
    }, fields[0])

  def test_types_object(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'object'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'any',
      'is_reference': False,
    }, fields[0])

  def test_types_boolean(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'boolean'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'boolean',
      'is_reference': False,
    }, fields[0])

  def test_types_unknown(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'schweindl'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'schweindl',
      'is_reference': False,
    }, fields[0])
  
  def test_readonly(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'string',
          'readOnly': False,
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'readonly': False
    },fields[0])

    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'string',
          'readOnly': True,
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'readonly': True
    },fields[0])
  
  def test_multi(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'manyGrunz': {
          'type': 'array',
          'items': {
            'type': 'string'
          }
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'manyGrunz',
      'multi': True,
      'type': 'string',
      'readonly': False
    }, fields[0])

    _, fields = self.renderer.render_class('User', {
      'properties': {
        'manyGrunz': {
          'type': 'array',
          'items': {
            'type': 'string',
            'readOnly': True,
          }
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'manyGrunz',
      'multi': True,
      'type': 'string',
      'readonly': True,
      'is_reference': False,
    }, fields[0])

  def test_refs(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'grunzref': {
          '$ref': '#/definitions/Grunz'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'grunzref',
      'is_reference': True,
      'type': 'Grunz'
    }, fields[0])

    _, fields = self.renderer.render_class('User', {
      'properties': {
        'grunzref': {
          '$ref': '#/definitions/GrunzSchema'
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'grunzref',
      'is_reference': True,
      'type': 'Grunz'
    }, fields[0])
  
  def test_has_many(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'grunzrefs': {
          'type': 'array',
          'items': {
            '$ref': '#/definitions/Grunz',
          },
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'grunzrefs',
      'is_reference': True,
      'type': 'Grunz',
      'multi': True,
    }, fields[0])


  def test_example_types(self):
    defs = self._load_example()
    _, fields = self.renderer.render_class('User', defs['definitions']['User'])
    field_types = { f['name']: f['type'] for f in fields}
    self.assertDictEqual({
      'id': 'number',
      'username': 'string',
      'firstName': 'string',
      'lastName': 'string',
      'email': 'string',
      'password': 'string',
      'phone': 'string',
      'userStatus': 'number',
    }, field_types)
  
  
  def test_example_refs(self):
    defs = self._load_example()
    _, fields = self.renderer.render_class('Pet', defs['definitions']['Pet'])
    refs = [ f for f in fields if f['is_reference'] ]
    self.assertCountEqual(refs, [
      { 'name': 'category', 'is_reference': True, 'readonly': False, 'multi': False, 'type': 'Category' },
      { 'name': 'tags', 'is_reference': True, 'readonly': False, 'multi': True, 'type': 'Tag' },
    ])
  
  def test_rendered(self):
    with self._render_models():
      pass