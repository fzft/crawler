import parsel
import six
from w3lib.encoding import html_to_unicode, resolve_encoding, http_content_type_encoding, html_body_declared_encoding
from w3lib.html import strip_html5_whitespace
import demjson
from .headers import Headers
import re

from core.core_utils import parse_to_html


def to_unicode(text, encoding=None, errors='strict'):
    """Return the unicode representation of a bytes object `text`. If `text`
    is already an unicode object, return it as-is."""
    if isinstance(text, six.text_type):
        return text
    if not isinstance(text, (bytes, six.text_type)):
        raise TypeError('to_unicode must receive a bytes, str or unicode '
                        'object, got %s' % type(text).__name__)
    if encoding is None:
        encoding = 'utf-8'
    return text.decode(encoding, errors)


def obsolete_setter(setter, attrname):
    def newsetter(self, value):
        c = self.__class__.__name__
        msg = "%s.%s is not modifiable, use %s.replace() instead" % (c, attrname, c)
        raise AttributeError(msg)

    return newsetter


class Response(object):
    def __init__(self, url, status=200, headers=None, body=b'', flags=None, request=None):
        self._cookies = []
        if hasattr(headers, 'getall'):
            for hdr in headers.getall('Set-Cookie', ()):
                self.load_cookies(hdr)
        self.headers = Headers(headers or {})
        self.status = int(status)
        self._set_body(body)
        self.url = url

    def load_cookies(self, rawdata):
        if isinstance(rawdata, str):
            self._cookies.append(rawdata)

    @property
    def meta(self):
        try:
            return self.request.meta
        except AttributeError:
            raise AttributeError(
                "Response.meta not available, this response "
                "is not tied to any request"
            )

    def _get_body(self):
        return self._body

    def _set_body(self, body):
        if body is None:
            self._body = b''
        elif not isinstance(body, bytes):
            raise TypeError(
                "Response body must be bytes. "
                "If you want to pass unicode body use TextResponse "
                "or HtmlResponse.")
        else:
            self._body = body

    body = property(_get_body, obsolete_setter(_set_body, 'body'))

    def __str__(self):
        return "<%d %s>" % (self.status, self.url)

    __repr__ = __str__

    @property
    def text(self):
        """For subclasses of TextResponse, this will return the body
        as text (unicode object in Python 2 and str in Python 3)
        """
        raise AttributeError("Response content isn't text")

    def css(self, *a, **kw):
        """Shortcut method implemented only by responses whose content
        is text (subclasses of TextResponse).
        """

    def xpath(self, *a, **kw):
        """Shortcut method implemented only by responses whose content
        is text (subclasses of TextResponse)."""


class HtmlResponse(Response):
    _DEFAULT_ENCODING = 'ascii'

    def __init__(self, *args, **kwargs):
        self._encoding = kwargs.pop('encoding', None)
        self._cached_benc = None
        self._cached_ubody = None
        self._cached_selector = None
        super().__init__(*args, **kwargs)

    @property
    def encoding(self):
        return self._declared_encoding() or self._body_inferred_encoding()

    def _body_declared_encoding(self):
        return html_body_declared_encoding(self.body)

    def _declared_encoding(self):
        return self._encoding or self._headers_encoding() \
               or self._body_declared_encoding()

    def body_as_unicode(self):
        """Return body as unicode"""
        return self.text

    def _headers_encoding(self):
        content_type = self.headers.get(b'Content-Type', b'')
        return http_content_type_encoding(to_unicode(content_type))

    @property
    def text(self):
        """ Body as unicode """
        # access self.encoding before _cached_ubody to make sure
        # _body_inferred_encoding is called
        benc = self.encoding
        if self._cached_ubody is None:
            charset = 'charset=%s' % benc
            self._cached_ubody = html_to_unicode(charset, self.body)[1]
        return parse_to_html(self._cached_ubody)

    @property
    def json(self):
        return demjson.decode(self.text)

    def re_findall(self, pattern):
        result = re.compile(pattern).findall(self.text)
        return result

    def re_findfirst(self, pattern):
        result = self.re_findall(pattern)
        if result:
            return result[0]
        return ''

    def css_findfirst(self, query):
        return self.css_find_by_index(self, query)

    def css_find_by_index(self, query, idx=0, default=''):
        result = self.css(query).extract()
        if len(result) >= (idx + 1):
            return result[idx]
        return default

    def _auto_detect_fun(self, text):
        for enc in (self._DEFAULT_ENCODING, 'utf-8', 'cp1252'):
            try:
                text.decode(enc)
            except UnicodeError:
                continue
            return resolve_encoding(enc)

    @property
    def selector(self):
        from http_utils.unified import Selector
        if self._cached_selector is None:
            self._cached_selector = Selector(self)
        return self._cached_selector

    def xpath(self, query, **kwargs):
        return self.selector.xpath(query, **kwargs)

    def css(self, query):
        return self.selector.css(query)


def _url_from_selector(sel):
    # type: (parsel.Selector) -> str
    if isinstance(sel.root, six.string_types):
        # e.g. ::attr(href) result
        return strip_html5_whitespace(sel.root)
    if not hasattr(sel.root, 'tag'):
        raise ValueError("Unsupported selector: %s" % sel)
    if sel.root.tag not in ('a', 'link'):
        raise ValueError("Only <a> and <link> elements are supported; got <%s>" %
                         sel.root.tag)
    href = sel.root.get('href')
    if href is None:
        raise ValueError("<%s> element has no href attribute: %s" %
                         (sel.root.tag, sel))
    return strip_html5_whitespace(href)
