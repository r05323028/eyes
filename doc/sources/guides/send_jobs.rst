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
            Args:
                * `board`: Board name.
                * `n_days`: Crawl only latest n days posts.
        * CRAWL_PTT_BOARD_LIST
            Args:
                * `top_n`: Crawl only top n boards.
        * CRAWL_PTT_TOP_BOARD_POSTS

            .. warning::
                Before you run this job, remember to crawl board list first.

                .. code-block:: bash

                    eyes job dispatch --job_type=CRAWL_PTT_BOARD_LIST
                
            Args:
                * `n_days`: Crawl only latest n days posts.
        * CRAWL_DCARD_LATEST_POSTS
            Args:
                * `forum_id`: Forum ID.
                * `n_days`: Crawl only latest n days posts.
        * CRAWL_DCARD_BOARD_LIST
            Args:
                * `top_n`: Crawl only top n forums.
        * CRAWL_WIKI_ENTITIES
    * Stats jobs
        * PTT_MONTHLY_SUMMARY
            Args:
                * `year`: Year.
                * `month`: Month.
                * `overwrite`: Whether to overwrite rows.
    * ML jobs
        * PTT_SPACY_PIPELINE
            Args:
                * `year`: Year.
                * `month`: Month.
                * `overwrite`: Whether to overwrite rows.

Send a job by command
---------------------

.. code-block:: bash

    eyes job dispatch --job_type JOB_TYPE --arg ...
