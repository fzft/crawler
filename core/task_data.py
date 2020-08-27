from core.core_utils import make_signature
from collections import OrderedDict
from validators.validators import *


class NoDupOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if key in self:
            raise NameError('%s already defined' % key)
        super().__setitem__(key, value)


class StructMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases):
        return NoDupOrderedDict()

    def __new__(cls, clsname, bases, clsdict):
        fields = [key for key, val in clsdict.items() if isinstance(val, Descriptor)]
        for name in fields:
            clsdict[name].name = name
        clsobj = super().__new__(cls, clsname, bases, dict(clsdict))
        sig = make_signature(fields)
        setattr(clsobj, '__signature__', sig)
        return clsobj


class Structure(metaclass=StructMeta):
    def __init__(self, *args, **kwargs):
        self.data = kwargs
        for name, val in kwargs.items():
            setattr(self, name, val)


    def get_data(self):
        return self.data
