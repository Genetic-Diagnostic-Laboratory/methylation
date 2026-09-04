import click

from cli import __version__
from cli.commands.analysis import analysis
from cli.commands.config import config
from cli.commands.report import report


@click.group()
# Stated explicitly: the frozen exe has no installed distribution for click to read
@click.version_option(version=__version__, prog_name="methyl")
def methyl():
    """Methylation analysis and reporting tools."""
    pass


methyl.add_command(analysis)
methyl.add_command(config)
methyl.add_command(report)


if __name__ == "__main__":
    methyl()
