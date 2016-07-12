import logging

logger = logging.getLogger(__name__)


class Context(dict):
    """ Helper to keep aggregated state during url processing """

    @property
    def url(self):
        return self['url']

    @property
    def category(self):
        return self.get('_category', 0)

    @category.setter
    def category(self, val):
        logger.debug('category value set to %s', val)
        self['_category'] = val

    @property
    def product(self):
        return self.get('_product', 0)

    @product.setter
    def product(self, val):
        logger.debug('product value set to %s', val)
        self['_product'] = val

    @property
    def probabilities_formatted(self):
        total = self.category + self.product
        if total:
            category = 100.0 * self.category / total
            product = 100.0 * self.product / total
        else:
            category = product = 0
        items = (
            ('category', '%s%%' % category, '(score: %s)' % self.category),
            ('product', '%s%%' % product, '(score: %s)' % self.product),
        )
        return '\n'.join(map(lambda x: ' '.join(x), items))
