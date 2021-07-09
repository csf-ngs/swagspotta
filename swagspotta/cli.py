import sys
import click_log
import click
from .util import logger
from .python import PythonRenderer
import json
import traceback


click_log.basic_config(logger)

@click.group()
@click_log.simple_verbosity_option(logger)
@click.pass_context
def cli(ctx):
    """KortApi - tickets, trellos, guns, girls and ganja"""

@cli.command(short_help='python models')
@click.argument('swagger', type=click.File('r'))
@click.option('--classes', '-c', multiple=True, help='class names')
@click.option('--out', '-o', type=click.File('w'), default=sys.stdout)
def python(swagger, classes, out):
  swagger = json.load(swagger)
  if not 'definitions' in swagger:
    raise click.ClickException(f"no definitions in {swagger.name}")
  try:
    models = PythonRenderer().render(classes=classes, definitions=swagger['definitions'])
  except Exception as exc:
    logger.debug(traceback.format_exc())
    raise click.ClickException(exc.__str__())
  out.write(models)

