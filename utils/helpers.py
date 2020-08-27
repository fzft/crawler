import os

from utils import get_root_path


class _PackageBoundObject(object):

    def __init__(self, import_name, root_path=None):
        self.import_name = import_name
        if root_path is None:
            root_path = get_root_path(self.import_name)
        self.root_path = root_path

    def open_resource(self, resource, mode='rb'):
        if mode not in ('r', 'rb'):
            raise ValueError('Resources can only be opened for reading')
        return open(os.path.join(self.root_path, resource), mode)
