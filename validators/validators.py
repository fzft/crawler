# Descriptor Protocol
from core.exceptions import *

class Descriptor:
    def __init__(self, name=None, default=None):
        self.default = default
        self.name = name

    def __get__(self, instance, cls):
        # instance: is the instance being manipulated
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value or self.default

    def __delete__(self, instance):
        del instance.__dict__[self.name]


class Positive(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise RequestParamsError(description='Must be >= 0')
        super().__set__(instance, value)


# length check
class Sized(Descriptor):
    def __init__(self, *args, maxlen, **kwargs):
        self.maxlen = maxlen
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if len(value) > self.maxlen:
            raise RequestParamsError(description='Too long')
        super().__set__(instance, value)


import re


# Pattern match
class Regex(Descriptor):
    regex = None

    def __init__(self, *args, pat=None, **kwargs):
        self.pat = re.compile(pat)
        super().__init__(*args, **kwargs)

    def __set__(self, instance, value):
        if not self.pat.match(value):
            raise RequestParamsError(description='Invalid string')
        super().__set__(instance, value)


class MobileRegex(Regex):
    regex = "^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$"


class Typed(Descriptor):
    ty = object  # Expected type

    def __set__(self, instance, value):
        if not isinstance(value, self.ty):
            raise RequestParamsError(description='Expected %s' % self.ty)
        super().__set__(instance, value)


class Integer(Typed):
    ty = int


class Float(Typed):
    ty = float


class String(Typed):
    ty = str


# Minx
class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class SizedString(String, Sized):
    pass


class SizedRegexString(SizedString, Regex):
    pass
