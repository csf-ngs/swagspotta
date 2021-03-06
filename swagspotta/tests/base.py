import unittest
import os.path
import json

class TestBase(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    cls.data_dir = cls.get_data_dir()

  @classmethod
  def get_data_dir(cls) -> str:
    return os.path.join(cls.get_self_dir(), 'share')
  
  @classmethod
  def get_self_dir(cls) -> str:
    return os.path.realpath(os.path.dirname(__file__))

  
  def _load_example(self) -> dict:
    with open(f'{self.data_dir}/definition.json') as def_fh:
      swagger = json.load(def_fh)
    return swagger
