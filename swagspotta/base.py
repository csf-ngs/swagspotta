from abc import ABC, abstractmethod
from jinja2 import Environment, PackageLoader, FileSystemLoader
import os.path
import shutil

from jinja2.environment import Template
from jinja2.exceptions import TemplateNotFound

class RendererBase(ABC):
  def __init__(self, class_template_dir=None):
    self.loader = PackageLoader('swagspotta', 'templates')
    if class_template_dir:
      self.class_template_dir = class_template_dir
      self.class_loader = FileSystemLoader(class_template_dir)
    else:
      self.class_loader = None
    self.env = Environment(loader=self.loader)

  @property
  @abstractmethod
  def ext(self) -> str:
    pass

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

  def get_class_template(self, classname: str) -> Template:
    class_tpl = f"{classname}.{self.ext}.j2"
    if self.class_loader:
      try:
        template = self.class_loader.load(self.env, class_tpl)
      except TemplateNotFound:
        _, fullpath, _ = self.loader.get_source(self.env, os.path.join(self.template_dir, self.class_tpl))
        shutil.copyfile(fullpath, os.path.join(self.class_template_dir, class_tpl))
        template = self.class_loader.load(self.env, class_tpl)
    else:
      template = self.env.get_template(os.path.join(self.template_dir, self.class_tpl))
    return template
  
  def get_models_template(self) -> Template:
    return self.env.get_template(os.path.join(self.template_dir, self.models_tpl))
