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
        if self.Counter % (self.RetentionSpan * 2) == 0:
            self.__shrink_cache()
        return self.Counter

    def __shrink_cache(self):
        """
        Shrink cache by removing obselete items.
        """
        if len(self.CacheHit) == 0:
            return False

        max_val = max(self.CacheHit.values())
        obselete = list()
        for key, val in self.CacheHit.items():
            if max_val - val > self.RetentionSpan:
                obselete.append(key)
        for key in obselete:
            dict.pop(self, key)
            self.CacheHit.pop(key)

        return False

    def __getitem__(self, key):
        self.CacheHit[key] = self.Counter
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if len(self) >= self.CacheSize:
            self.__shrink_cache()
        self.CacheHit[key] = self.Counter
        dict.__setitem__(self, key, value)
