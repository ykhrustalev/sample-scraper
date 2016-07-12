import logging
import re

import requests
from lxml.html import fromstring

from context import Context

logger = logging.getLogger(__name__)


def url_wording(context):
    """
    :type context: Context
    """
    if re.match(r'^.*(category).*$', context.url):
        context.category += 1


def get_contents(context):
    """
    :type context: Context
    """
    r = requests.get(context.url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/51.0.2704.106 Safari/537.36'
    })
    r.raise_for_status()
    content = r.content
    context['content'] = content
    context['html'] = fromstring(content)


def open_graph_meta(context):
    html = context['html']
    meta = html.xpath('//meta[@property="og:type"]')
    if meta:
        content = meta[0].attrib['content']
        logger.debug("matched og:type %s", content)
        if content.lower() == 'product':
            context.product += 1
        if content.lower() == 'category':
            context.category += 1


def google_analytics_meta(context):
    """ Find things like
        'PageType','ProductPage'
        'PageType','MainCatalog'
        or
        'ecomm_pagetyp': 'category'
    """

    content = context['content']

    m = re.search(
        r'(pagetype[\'"](:?.){3,7}(:?product))',
        content,
        re.IGNORECASE | re.MULTILINE
    )
    if m:
        logger.debug('matched for product %s', m.group(1))
        context.product += 1

    m = re.search(
        r'(pagetype[\'"](:?.){3,7}(:?'
        r'maincatalog|catalog|category|list|landing))',
        content,
        re.IGNORECASE | re.MULTILINE
    )
    if m:
        logger.debug('matched for category %s', m.group(1))
        context.category += 1


def contains_paginator(context):
    """ pagePrevious / pageNext """
    html = context['html']

    if (html.xpath('//*[@class="pagePrevious"]') and
            html.xpath('//*[@class="pageNext"]')):
        context.category += 1
    elif (html.xpath('//*[@id="pagePrevious"]') and
              html.xpath('//*[@id="pageNext"]')):
        context.category += 1


def schema_reference(context):
    content = context['content']

    if ('http://schema.org/Product' in content or
                'http://schema.org/IndividualProduct' in content or
                'http://schema.org/ProductModel' in content or
                'http://schema.org/SomeProducts' in content):
        context.product += 1


def has_share_buttons(context):
    content = context['content']

    if 'share this' in content.lower():
        context.product += 1


def has_rating(context):
    html = context['html']

    if html.xpath('//*[@id="avgRating"]'):
        context.product += 1


REDUCERS = [
    url_wording,
    get_contents,
    open_graph_meta,
    google_analytics_meta,
    contains_paginator,
    schema_reference,
    has_share_buttons,
    has_rating,
]
