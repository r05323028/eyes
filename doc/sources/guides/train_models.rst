Train models
============

Built-in models
---------------

zh_core_eyes_md
###############

.. code-block:: bash

    spacy train config/spacy/zh_core_eyes_md.cfg --paths.train [TRAIN_FILE] --paths.dev [DEV_FILE] --output [OUTPUT_DIR] --initialize.vectors zh_core_web_md
