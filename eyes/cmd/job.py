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
    '--forum_id',
    help="Dcard forum id",
)
@click.option(
    '--n_days',
    type=int,
    help="Latest N day posts you need to crawl.",
)
@click.option(
    '--top_n',
    type=int,
    default=None,
    help="Top N boards to be crawled.",
)
def dispatch(
    job_type,
    board,
    forum_id,
    n_days,
    top_n,
):
    '''Dispatch a job
    '''
    job_type = JobType[job_type]
    jobs = Jobs()

    if job_type in [
            JobType.CRAWL_PTT_LATEST_POSTS,
            JobType.CRAWL_DCARD_LATEST_POSTS,
    ]:

        if job_type == JobType.CRAWL_DCARD_LATEST_POSTS:
            if not forum_id:
                raise Exception('forum_id is required')

            job = Job(job_type=job_type,
                      payload={
                          'n_days': n_days,
                          'forum_id': forum_id,
                      })

        if job_type == JobType.CRAWL_PTT_LATEST_POSTS:
            if not board:
                raise Exception('board is required')

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

    if job_type in [
            JobType.CRAWL_PTT_BOARD_LIST,
            JobType.CRAWL_DCARD_BOARD_LIST,
    ]:
        job = Job(
            job_type=job_type,
            payload={
                'top_n': top_n,
            },
        )

        logger.info('Dispatch job, %s', job)
        jobs.dispatch(job)


job.add_command(dispatch)
