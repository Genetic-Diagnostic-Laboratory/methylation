import click

from report.main import main as report_main


@click.group()
def report():
    """Report generation commands."""
    pass


@report.command("run")
def report_run():
    """Launch the methylation report generator."""
    report_main()
