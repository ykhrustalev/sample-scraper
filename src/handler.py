import logging

from context import Context
from reducers import REDUCERS

logger = logging.getLogger(__name__)


def handle_url(url, options):
    """ Handle url, use all defined handlers to find page type

    :param str url: page's url
    :param object options:  additional cli options
    :return: identification result and page value|error message
    :rtype: tuple of (bool, str)
    """
    try:
        context = Context(url=url)
        logger.debug("Handling %s", url)
        for reducer in REDUCERS:
            logger.debug("Before %s", reducer.__name__)
            try:
                reducer(context)
                logger.debug("After %s", reducer.__name__)
            except Exception:
                logger.exception("Failed on %s", reducer.__name__)
                raise

        logger.debug("Done")
        logger.debug("")
        return True, context.probabilities_formatted

    except Exception, e:
        logger.exception('Failed to handle url %s', url)
        return False, str(e)
