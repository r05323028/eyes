Send jobs
=========

.. warning::
    Before you dispatch a job, remember to start a celery worker as a consumer.

    .. code-block:: bash

        celery -A eyes.celery worker

Jobs
----

Jobs repository of Eyes.

    * Crawl jobs
        * CRAWL_PTT_LATEST_POSTS
        * CRAWL_PTT_BOARD_LIST
        * CRAWL_PTT_TOP_BOARD_POSTS
        * CRAWL_DCARD_LATEST_POSTS
        * CRAWL_DCARD_BOARD_LIST
        * CRAWL_WIKI_ENTITIES
    * Stats jobs
        * PTT_MONTHLY_SUMMARY
    * ML jobs
        * PTT_SPACY_PIPELINE

Send a job by command
---------------------

.. code-block:: bash

    eyes job dispatch --job_type JOB_TYPE --arg ...
