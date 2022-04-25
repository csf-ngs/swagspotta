from contextlib import contextmanager
from datetime import datetime
import re
import typing
from .base import TestBase
from swagspotta.python import PythonRenderer
import os


class TestPython(TestBase):
  def setUp(self):
    self.renderer = PythonRenderer()


  def test_double_class(self):
    defs = self._load_example()
    src = self.renderer.render(classes=['User', 'User'], definitions=defs['definitions'])
    self.assertIsNotNone(src)
    src=typing.cast(str, src)
    matches = len(re.findall(r'^class User', src, re.MULTILINE))
    self.assertEqual(matches, 1)

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
  
  
  def test_example_refs(self):
    defs = self._load_example()
    _, fields = self.renderer.render_class('Pet', defs['definitions']['Pet'])
    refs = [ f for f in fields if f['is_reference'] ]
    self.assertCountEqual(refs, [
      { 'name': 'category', 'is_reference': True, 'readonly': False, 'multi': False, 'type': 'Category' },
      { 'name': 'tags', 'is_reference': True, 'readonly': False, 'multi': True, 'type': 'Tag' },
    ])
  
  @contextmanager
  def _render_models(self):
    defs = self._load_example()
    src = self.renderer.render(classes=[
      'User', 'Category', 'Tag', 'Pet', 'Order'
    ], definitions=defs['definitions'])
    self.assertIsNotNone(src)
    src=typing.cast(str, src)

    with open(os.path.join(self.get_self_dir(), 'model.py'), 'w') as outfh:
      outfh.write(src)
    yield

    os.unlink(os.path.join(self.get_self_dir(), 'model.py'))

  def test_rendered_user(self):
    with self._render_models():
      # it's ok if your IDE shows an error here, the module file is wrritten by the 
      # contextmanager
      from .model import User, plainToUser, serializeUser # type: ignore

    struct = {
      'id': 12,
      'username': 'test.hase',
      'email': 'test.hase@testha.se',
      'firstName': 'Test',
      'lastName': 'Hase',
      'password': 'geheim',
      'phone': None,
      'userStatus': 0,
    }
    user = plainToUser(json=struct)
    self.assertIsInstance(user, User)
    self.assertEqual(user.id, 12)
    self.assertEqual(user.username, 'test.hase')
    self.assertIsNone(user.phone)

    serialized = serializeUser(user)
    self.assertDictEqual(serialized, struct)
  
  def test_rendered_datetime(self):
    with self._render_models():
      from .model import serializeOrder, plainToOrder # type: ignore
    
    struct = {
      'shipDate': "2021-07-27T09:46:50.598511+00:00",
    }
    order = plainToOrder(struct)
    self.assertIsInstance(order.shipDate, datetime)
    self.assertEqual(str(order.shipDate), '2021-07-27 09:46:50.598511+00:00')

    serialized = serializeOrder(order)
    self.assertEqual(serialized['shipDate'], struct['shipDate'])
  
  def test_rendered_pet(self):
    with self._render_models():
      from .model import Pet, plainToPet, serializePet, Category, Tag # type: ignore
    
    struct = {
      'id': 12,
      'category': {
        'id': 100,
        'name': 'testhase',
      },
      'name': 'Hase Test',
      'status': 'doing good',
      'photoUrls': [ 'eins', 'zwei', 'drei' ],
      'tags': [
        { 'id': 13, 'name': 'cute', },
        { 'id': 14, 'name': 'brown', },
      ]
    }
    pet = plainToPet(struct)
    self.assertIsInstance(pet, Pet)
    self.assertIsInstance(pet.category, Category)
    self.assertListEqual(pet.photoUrls, struct['photoUrls'])
    self.assertIsInstance(pet.tags[0], Tag)

    serialized = serializePet(pet)
    self.assertDictEqual(serialized, struct)

    struct['photoUrls'] = None
    self.assertListEqual(plainToPet(struct).photoUrls, [])
    struct['photoUrls'] = 'oink'
    self.assertListEqual(plainToPet(struct).photoUrls, [])
    struct.pop('photoUrls')
    self.assertListEqual(plainToPet(struct).photoUrls, [])

    struct['tags'] = None
    self.assertListEqual(plainToPet(struct).tags, [])
    struct['tags'] = 'something'
    self.assertListEqual(plainToPet(struct).tags, [])
    struct.pop('tags')
    self.assertListEqual(plainToPet(struct).tags, [])