"""An iterable JSON dictionary with extra safety.

Part of Shellcuts by Tiger Sachse.
"""
import json
from pathlib import Path

class JSONDictionary:
    """Implements a dictionary that is iterable and handles JSON I/O."""

    def __init__(self, json_path):
        """Attempt to load the given JSON path."""
        self.__json_path = json_path

        if not Path(self.__json_path).exists():
            self.__contents = {}
        else:
            with open(self.__json_path, 'r') as f:
                self.__contents = json.load(f)


    def __delitem__(self, key):
        """Delete an item from the dictionary, if it exists."""
        if key in self.__contents:
            del self.__contents[key]


    def __getitem__(self, key):
        """Return a value from the dictionary, if it exists."""
        if key in self.__contents:
            return self.__contents[key]
        else:
            return None


    def __setitem__(self, key, value):
        """Set an item in the dictionary."""
        self.__contents[key] = value


    def __iter__(self):
        """Return an iterator for the dictionary."""
        return iter(self.__generate_items())


    def __generate_items(self):
        """Generate all items in the list."""
        for key in self.__contents.keys():
            yield key, self.__contents[key]


    def write(self):
        """Write the dictionary to a file."""
        with open(self.__json_path, 'w') as f:
            json.dump(self.__contents, f)
