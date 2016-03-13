#! /usr/bin/python
###############################################################################
"""\
provides formatter objects which return printer-friendly character sequences
"""
import os
import json

class Formatter(object):
    """abstract base class for formatters"""
    def __init__(self):
        if(self.__class__ == Formatter):
            raise TypeError

    @classmethod
    def parseDicts(cls, dicts):
        """create a dict of instances from a list of configuration dicts"""
        raise NotImplementedError

    def format(self, region):
        """format the given PixelRegion and return the results"""
        raise NotImplementedError

class HalfBlockFormatter(Formatter):
    """formats PixelRegions by using space, block and half-block characters"""
    def __init__(self, neither, bottom, top, both):
        self.neither = neither
        self.bottom = bottom
        self.top = top
        self.both = both

    @classmethod
    def parseDicts(cls, dicts):
        results = {}
        for dict_ in dicts:
            name = dict_["name"]
            formatter = cls(dict_["neither"],
                            dict_["bottom"],
                            dict_["top"],
                            dict_["both"])
            results.update({name: formatter})
        return results

    def transform(self, topRow, bottomRow):
        newRow = []
        for t, b in zip(topRow, bottomRow):
            if t and b:
                newRow.append(self.both)
            elif t and not b:
                newRow.append(self.top)
            elif b and not t:
                newRow.append(self.bottom)
            else:
                newRow.append(self.neither)
        return "".join(newRow)

    def format(self, region):
        rows = region.getRows()
        newRows = []
        while len(rows) >= 2:
            top = rows.pop(0)
            bottom = rows.pop(0)
            newRows.append(self.transform(top, bottom))
        if len(rows) == 1:
            top = rows.pop(0)
            bottom = [False for x in top]
            newRows.append(self.transform(top, bottom))
        return newRows

class FormatterLibraryNode(object):
    def __init__(self, dict_):
        self.library = dict_

    def __getattr__(self, key):
        obj = self.library[key]
        if isinstance(obj, Formatter):
            return obj
        else:
            return FormatterLibraryNode(obj)

    def catalog(self):
        return [x for x in self.library.iterkeys()]

def parseFormatters():
    directory = os.path.dirname(os.path.abspath(__file__))
    subclasses = [sub for sub in Formatter.__subclasses__()]
    print subclasses

    instances = {}
    for subclass in subclasses:
        filename = "".join([subclass.__name__, ".json"])
        try:
            with open(os.path.join(directory, filename)) as f:
                configurations = json.load(f)["instances"]
                category = subclass.__name__
                instances[category] = subclass.parseDicts(configurations)
        except IOError:
            # we assume this means there are none
            pass
    return instances

FormatterLibrary = FormatterLibraryNode(parseFormatters())
