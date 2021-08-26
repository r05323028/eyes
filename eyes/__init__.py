import logging

from rich.logging import RichHandler

# set logging
logging.basicConfig(
    level=logging.NOTSET,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True),
    ],
)

__version__ = '0.1.0'
