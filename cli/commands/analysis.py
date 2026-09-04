import click

from analysis.main import main as analysis_main


@click.group()
def analysis():
    """Analysis pipeline commands."""
    pass


@analysis.command("run")
def analysis_run():
    """Launch the interactive analysis tool."""
    analysis_main()
