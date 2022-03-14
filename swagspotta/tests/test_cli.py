from click.testing import CliRunner

from swagspotta.cli import cli

from .base import TestBase

class TestCli(TestBase):

  def test_base(self):
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    self.assertEqual(result.exit_code, 0)

  def test_guess(self):
    runner = CliRunner()
    result = runner.invoke(cli, [f"{self.data_dir}/definition.json", 'guess-classes'])
    self.assertEqual(result.exit_code, 0)
    classes = result.output.splitlines()
    self.assertCountEqual(
      classes,
      ['-c Order', '-c Category', '-c User', '-c Pet', '-c Tag']
    )
  