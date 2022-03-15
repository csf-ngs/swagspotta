from abc import ABC, abstractmethod, abstractproperty
from jinja2 import Environment, PackageLoader, FileSystemLoader
import os.path
import shutil
import typing
from .util import logger

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


  def render(self, classes: typing.List[str], definitions: dict) -> typing.Optional[str]:
    class_defs: typing.List[str] = []
    all_defs = {}
    for classname in classes:
      schema_name = f"{classname}Schema"
      if not schema_name in definitions and not classname in definitions:
        raise Exception(f"schema {classname}/{schema_name} not found in definitions")
      logger.debug(f"Rendering {classname}")
      class_out, field_defs = self.render_class(classname, definitions.get(schema_name, definitions.get(classname)))
      if class_out is not None:
        class_defs.append(class_out)
      all_defs[classname]=field_defs

    logger.debug(f"Checking references...")
    refs = {}
    for classname, fdefs in all_defs.items():
      for fdef in fdefs:
        if fdef['is_reference']:
          refs[fdef['type']]=classname
    for classname in all_defs.keys():
      refs.pop(classname, None)
    for classname, referencing in refs.items():
      logger.warn(f"{classname} referenced by {referencing} is not rendered")

    logger.debug(f"Rendering models...")
    template = self.get_models_template()
    return template.render(classes=class_defs)
  
  @abstractmethod
  def render_class(self, classname, schema) -> typing.Tuple[typing.Optional[str], dict]:
    pass

  def _try_load(self, tpl: str, default: str) -> Template:
    if self.class_loader:
      try:
        template = self.class_loader.load(self.env, tpl)
      except TemplateNotFound:
        logger.debug(f"copy {default} to {tpl}")
        _, fullpath, _ = self.loader.get_source(self.env, os.path.join(self.template_dir, default))
        shutil.copyfile(typing.cast(str, fullpath), os.path.join(self.class_template_dir, tpl))
        template = self.class_loader.load(self.env, tpl)
    else:
      template = self.env.get_template(os.path.join(self.template_dir, default))
    return template

  def get_class_template(self, classname: str) -> Template:
    class_tpl = f"{classname}.{self.ext}.j2"
    return self._try_load(class_tpl, self.class_tpl)
  
  def get_models_template(self) -> Template:
    return self._try_load(self.models_tpl, self.models_tpl)