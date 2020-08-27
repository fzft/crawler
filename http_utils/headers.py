from collections import Mapping
from requests.utils import default_user_agent
from requests.structures import CaseInsensitiveDict

class Headers(dict):
    def __init__(self, seq=None):
        super().__init__()
        if seq:
            self.update(seq)

    def __getitem__(self, key):
        return dict.__getitem__(self, self.normkey(key))

    def __setitem__(self, key, value):
        dict.__setitem__(self, self.normkey(key), self.normvalue(value))

    def get(self, key, def_val=None):
        return dict.get(self, self.normkey(key), self.normvalue(def_val))

    def setdefault(self, key, def_val=None):
        return dict.setdefault(self, self.normkey(key), self.normvalue(def_val))

    def update(self, seq):
        seq = seq.items() if isinstance(seq, Mapping) else seq
        iseq = ((self.normkey(k), self.normvalue(v)) for k, v in seq)
        super().update(iseq)

    def normkey(self, key):
        return key.lower()

    def normvalue(self, value):
        return value

    def pop(self, key, *args):
        return dict.pop(self, self.normkey(key), *args)

    def __contains__(self, key):
        return dict.__contains__(self, self.normkey(key))


def default_headers():

    return CaseInsensitiveDict({
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Accept-Encoding': ', '.join(('gzip', 'deflate')),
        'Accept': '*/*',
        'Connection': 'keep-alive',
    })

if __name__ == '__main__':
    h = Headers({'Set-Cookie':'set1'})
    from aiohttp import ClientResponse