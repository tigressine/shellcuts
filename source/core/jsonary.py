"""An iterable JSON dictionary with extra safety.

In the future, this class may be updated to extend dict directly, thus
eliminating some redundancy and inefficiencies.

Part of Shellcuts by Tiger Sachse.
"""
import json
from pathlib import Path

class Jsonary:
    """A JSON dictionary that is iterable and handles JSON I/O."""
    def __init__(self, json_path):
        """Attempt to load the given JSON path."""
        self.__json_path = json_path

        if not Path(self.__json_path).exists():
            self.__contents = {}
        else:
            with open(self.__json_path, 'r') as f:
                self.__contents = json.load(f)


    def __delitem__(self, key):
        """Delete an item from the jsonary, if it exists."""
        if key in self.__contents:
            del self.__contents[key]


    def __getitem__(self, key):
        """Return a value from the jsonary, if it exists."""
        if key in self.__contents:
            return self.__contents[key]
        else:
            return None


    def __setitem__(self, key, value):
        """Set an item in the jsonary."""
        self.__contents[key] = value


    def __iter__(self):
        """Return an iterator for the jsonary."""
        return iter(self.__generate_items())


    def __len__(self):
        """Return the size of the jsonary."""
        return len(self.__contents)


    def __contains__(self, key):
        """Return whether a key is in the jsonary."""
        return key in self.__contents


    def __generate_items(self):
        """Generate all items in the jsonary."""
        for key in self.__contents.keys():
            yield key, self.__contents[key]


    def write(self):
        """Write the jsonary to a file."""
        with open(self.__json_path, 'w') as f:
            json.dump(self.__contents, f)
