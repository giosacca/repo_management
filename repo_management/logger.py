""" logger module

A module to log the data from the repos.
"""

import logging
import sys

class RepoLogger(object):
    """
    A class that represents a logger.

    Attributes
    ----------
    logger : logging.RootLogger
        The logger.
    """

    def __init__(self):

        self.logger = logging.getLogger()

        logging.basicConfig(
            format = '%(asctime)s - [%(levelname)s] - %(message)s',
            level = logging.INFO,
            stream = sys.stderr
            )