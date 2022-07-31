from background_task import background
from logging import getLogger

logger = getLogger(__name__)

@background(schedule=3)
def demo_task(message):
    print('kaka')
    logger.debug('demo_task. message={0}'.format(message))
