'''Job commands
'''
import logging

import click

from eyes.job import Dispatcher, JobType, Job

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@click.group()
def job():
    '''Eyes Job Commands
    '''


@click.command()
@click.option(
    '--job_type',
    type=click.Choice([job.name for job in JobType]),
    help='Job name',
)
@click.option(
    '--board',
    required=True,
    help="Board name",
)
@click.option(
    '--n_days',
    type=int,
    help="Latest N day posts you need to crawl.",
)
def dispatch(
    job_type,
    board,
    n_days,
):
    '''Dispatch a job
    '''
    job_type = JobType[job_type]
    dispatcher = Dispatcher()

    if job_type == JobType.CRAWL_PTT_LATEST_POSTS:
        # check options
        if not n_days:
            raise Exception("n_days is required")

        # create job
        job = Job(
            job_type=job_type,
            payload={
                'n_days': n_days,
                'board': board
            },
        )

    # dispatch job
    logger.info('Dispatch job, %s', job)
    dispatcher.dispatch(job)


job.add_command(dispatch)
