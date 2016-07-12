#!/usr/bin/env python

import argparse
import logging
import sys

from handler import handle_url

logger = logging.getLogger(__name__)

USAGE = """ Simple utility to identify whether url belongs to category page
or product.

"""


def parse_opts():
    """ Parse cli call arguments
    :rtype: object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("urls",
                        nargs='+',
                        help="URLs to check", )
    parser.add_argument("--verbose", "-v",
                        default=False,
                        action="store_true",
                        help="Use debug level logging", )

    args = parser.parse_args()
    return args


def configure_logging(options):
    level = logging.DEBUG if options.verbose else logging.INFO
    logging.basicConfig(level=level)

    # known verbose logger
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def main():
    args = parse_opts()
    configure_logging(args)

    rc = 0
    results = []
    for url in args.urls:
        handled, value = handle_url(url, args)
        if not handled:
            rc = 1
            results.append('%s failed with error: %s' % (url, value))
            continue

        results.append('%s is\n%s' % (url, value, ))

    print '*' * 79
    print '\n\n'.join(results)
    print '*' * 79

    sys.exit(rc)


if __name__ == '__main__':
    main()
