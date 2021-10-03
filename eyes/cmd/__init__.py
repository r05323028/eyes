'''Eyes commands
'''
import logging

import click

from eyes.cmd.db import db
from eyes.cmd.job import job
from eyes.cmd.train import train

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
}


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    '''Eyes Command Line Tools
    '''


cli.add_command(db)
cli.add_command(job)
cli.add_command(train)
