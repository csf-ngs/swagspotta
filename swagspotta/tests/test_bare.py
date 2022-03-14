from .base import TestBase

class TestBare(TestBase):
  def test_example(self):
    self.assertIn('definitions', self._load_example())
  
  def test_classes(self):
    swagger = self._load_example()
    self.assertListEqual(
      ['Order', 'Category', 'User', 'Tag', 'Pet', 'ApiResponse'], 
      list(swagger['definitions'].keys())
    )

