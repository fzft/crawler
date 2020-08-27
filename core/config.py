import errno
import types
import sys
import os
from utils import get_root_path
# from utils.utils import *


def import_string(import_name, silent=False):
    import_name = str(import_name).replace(':', '.')
    try:
        try:
            a = __import__(import_name)
        except ImportError:
            if '.' not in import_name:
                raise
            else:
                return sys.modules[import_name]
        module_name, obj_name = import_name.rsplit('.', 1)
        try:
            module = __import__(module_name, None, None, [obj_name])
        except ImportError:
            module = import_string(module_name)

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        if not silent:
            pass


class Config(dict):
    def __init__(self, import_name, defaults=None):
        dict.__init__(self, defaults or {})
        self.root_path = get_root_path(import_name)
        self.from_pyfile('settings.py')
        profile_active = self.get('PROFILE_ACTIVE')
        if profile_active is not None:
            self.from_pyfile('settings-%s.py' % profile_active)

    def from_pyfile(self, filename, silent=False):
        filename = os.path.join(self.root_path, filename)
        d = types.ModuleType('config')
        d.__file__ = filename
        try:
            with open(filename, mode='rb') as config_file:
                exec(compile(config_file.read(), filename, 'exec'), d.__dict__)
        except IOError as e:
            if silent and e.errno in (errno.ENOENT, errno.EISDIR):
                return False
            e.strerror = 'Unable to load configuration file (%s)' % e.strerror
            raise
        self.from_object(d)
        return True

    def from_object(self, obj):
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def __getattr__(self, item):
        return self[item]

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
