from .base import TestBase
from swagspotta.python import PythonRenderer

class TestPython(TestBase):
  def setUp(self):
    self.renderer = PythonRenderer()

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
      'type': 'int'
    }, id_field)
  
  def test_example_types(self):
    defs = self._load_example()
    _, fields = self.renderer.render_class('User', defs['definitions']['User'])
    field_types = { f['name']: f['type'] for f in fields}
    self.assertDictEqual({
      'id': 'int',
      'username': 'str',
      'firstName': 'str',
      'lastName': 'str',
      'email': 'str',
      'password': 'str',
      'phone': 'str',
      'userStatus': 'int',
    }, field_types)
  
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
      'type': 'int',
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
      'type': 'str',
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
      'type': 'float',
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
      'type': 'int',
      'is_reference': False,
    }, fields[0])

  def test_types_datetime(self):
    _, fields = self.renderer.render_class('User', {
      'properties': {
        'testgrunz': {
          'type': 'str',
          'format': 'date-time',
        }
      }
    })
    self.assertDictContainsSubset({
      'name': 'testgrunz',
      'type': 'datetime',
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
      'type': 'int',
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
      'type': 'dict',
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
      'type': 'bool',
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
      'type': 'str',
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
      'type': 'str',
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


  
  def test_example_refs(self):
    defs = self._load_example()
    _, fields = self.renderer.render_class('Pet', defs['definitions']['Pet'])
    #print(fields)