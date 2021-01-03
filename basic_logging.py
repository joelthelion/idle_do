""" Non braindead basic logging configuration for python """
import logging
from logging import info, warning, debug, error

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO)
