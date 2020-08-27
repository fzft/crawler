"""
XPath core_selectors based on lxml
"""
import warnings

import six
from parsel import Selector as _ParselSelector

from http_utils.http_response import HtmlResponse

__all__ = ['Selector', 'SelectorList']


def _st(response, st):
    return 'html'


def to_bytes(text, encoding=None, errors='strict'):
    """Return the binary representation of `text`. If `text`
    is already a bytes object, return it as-is."""
    if isinstance(text, bytes):
        return text
    if not isinstance(text, six.string_types):
        raise TypeError('to_bytes must receive a unicode, str or bytes '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.encode(encoding, errors)


def _response_from_text(text, st):
    return HtmlResponse(url='about:blank', encoding='utf-8',
              body=to_bytes(text, 'utf-8'))


class SelectorList(_ParselSelector.selectorlist_cls):
    def extract_unquoted(self):
        return [x.extract_unquoted() for x in self]

    def x(self, xpath):
        return self.select(xpath)

    def select(self, xpath):
        return self.xpath(xpath)


class Selector(_ParselSelector):

    __slots__ = ['response']
    selectorlist_cls = SelectorList

    def __init__(self, response=None, text=None, type=None, root=None, _root=None, **kwargs):
        if not(response is None or text is None):
           raise ValueError('%s.__init__() received both response and text'
                            % self.__class__.__name__)

        st = _st(response, type or self._default_type)

        if _root is not None:
            if root is None:
                root = _root
            else:
                warnings.warn("Ignoring deprecated `_root` argument, using provided `root`")

        if text is not None:
            response = _response_from_text(text, st)

        if response is not None:
            text = response.text

        self.response = response
        super().__init__(text=text, type=st, root=root, **kwargs)


