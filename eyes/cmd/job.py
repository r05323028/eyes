'''Job commands
'''
import logging

import click

from eyes.job import Job, Jobs, JobType

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
    help="Board name",
)
@click.option(
    '--n_days',
    type=int,
    help="Latest N day posts you need to crawl.",
)
@click.option(
    '--top_n',
    type=int,
    default=30,
    help="Top N boards to be crawled.",
)
def dispatch(
    job_type,
    board,
    n_days,
    top_n,
):
    '''Dispatch a job
    '''
    job_type = JobType[job_type]
    jobs = Jobs()

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
        jobs.dispatch(job)

    if job_type == JobType.CRAWL_PTT_BOARD_LIST:
        if not top_n:
            raise Exception('top_n is required')

        job = Job(
            job_type=job_type,
            payload={
                'top_n': top_n,
            },
        )

        logger.info('Dispatch job, %s', job)
        jobs.dispatch(job)


job.add_command(dispatch)
