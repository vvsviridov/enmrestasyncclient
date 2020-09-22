from collections import defaultdict


class FdnDict(defaultdict):

    def __init__(self, fdn=None):
        super(FdnDict, self).__init__(list)
        if fdn is not None:
            for kv in fdn.split(','):
                k, v = kv.split('=')
                self[k].append(v)

    def __call__(self, **kwargs):
        for k, v in kwargs.items():
            self[k].append(v)
        return ",".join([f'{k}={i}' for k, v in self.items() for i in v])
