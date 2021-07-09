from abc import ABC, abstractmethod
from jinja2 import Environment, PackageLoader
import os.path

from jinja2.environment import Template

class RendererBase(ABC):
  def __init__(self):
    self.loader = PackageLoader('swagspotta', 'templates')
    self.env = Environment(loader=self.loader)

  @property
  @abstractmethod
  def template_dir(self) -> str:
    pass

  @property
  @abstractmethod
  def models_tpl(self) -> str:
    pass

  @property
  @abstractmethod
  def class_tpl(self) -> str:
    pass


  @abstractmethod
  def render(self, defs):
    pass

  def get_class_template(self) -> Template:
    return self.env.get_template(os.path.join(self.template_dir, self.class_tpl))
  
  def get_models_template(self) -> Template:
    return self.env.get_template(os.path.join(self.template_dir, self.models_tpl))

  
