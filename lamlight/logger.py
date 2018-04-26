'''
learning.logger
~~~~~~~~~~~~~~~~
Module contains the logger which is user to log the process of lamlight

'''

import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s - %(message)s')
logger = logging.getLogger(name='lamlight')
