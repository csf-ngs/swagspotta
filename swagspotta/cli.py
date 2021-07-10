from swagspotta.typescript import TypescriptRenderer
import sys
import click_log
import click
from .util import logger
from .python import PythonRenderer
import json
import traceback
import re


click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
@click.argument('swagger', type=click.File('r'))
@click.pass_context
def cli(ctx, swagger):
  """Spotta - spit out classes from swagger/openapi2 defs"""
  swagger = json.load(swagger)
  if not 'definitions' in swagger:
    raise click.ClickException(f"no definitions in {swagger.name}")
  ctx.obj = swagger

@cli.command(short_help='guess classes')
@click.pass_obj
def guess_classes(obj):
  for name in obj['definitions'].keys():
    if re.search(r'(Response|Request)Schema', name) or re.search(r'(Create|Update|Post)Schema', name):
      continue
    click.echo(f"-c {name}")

@cli.command(short_help='python classes')
@click.option('--classes', '-c', multiple=True, help='class names (can be specified multiple times)')
@click.option('--class-templates', '-t', type=click.Path(file_okay=False, writable=True, exists=True), help='directory with class specific templates')
@click.option('--out', '-o', type=click.File('w'), default=sys.stdout, help='default to stdout')
@click.pass_obj
def python(obj, classes, class_templates, out):
  try:
    models = PythonRenderer(class_template_dir=class_templates).render(classes=classes, definitions=obj['definitions'])
  except Exception as exc:
    logger.debug(traceback.format_exc())
    raise click.ClickException(exc.__str__())
  out.write(models)

@cli.command(short_help='typescript classes')
@click.option('--classes', '-c', multiple=True, help='class names (can be specified multiple times)')
@click.option('--class-templates', '-t', type=click.Path(file_okay=False, writable=True, exists=True), help='directory with class specific templates')
@click.option('--out', '-o', type=click.File('w'), default=sys.stdout, help='default to stdout')
@click.pass_obj
def typescript(obj, classes, class_templates, out):
  try:
    models = TypescriptRenderer(class_template_dir=class_templates).render(classes=classes, definitions=obj['definitions'])
  except Exception as exc:
    logger.debug(traceback.format_exc())
    raise click.ClickException(exc.__str__())
  out.write(models)

