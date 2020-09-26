"""
This module contains Cache class.
"""


class Cache(dict):
    """
    This modules is an extension to python dictionary
    This will have a smart cache cleanup functionality.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CacheHit = dict()
        self.Counter = 0
        self.CacheSize = 50
        self.RetentionSpan = 120

    def UpdateCounter(self, value=1):
        """
        Update the Counter attribute
        Then returns the updated counter value
        """
        self.Counter += value
        return self.Counter

    def __shrinkCache(self):
        print("Deleting obselete sprites")
        maxVal = max(self.CacheHit.values())
        obselete = list()
        for key, val in self.CacheHit.items():
            if maxVal - val > self.RetentionSpan:
                obselete.append(key)
        for key in obselete:
            dict.pop(self, key)
            self.CacheHit.pop(key)

    def __getitem__(self, key):
        self.CacheHit[key] = self.Counter
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if len(self) >= self.CacheSize:
            self.__shrinkCache()
        self.CacheHit[key] = self.Counter
        dict.__setitem__(self, key, value)
