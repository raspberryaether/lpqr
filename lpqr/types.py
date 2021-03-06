#! /usr/bin/python
###############################################################################
"""\
provides data types for use with lpqr
"""

import qrcode.image.base

class PixelRegion(object):
    """represents a rectangle of pixels.

    an X value of 0 signifies the leftmost column; a Y value
    of 0 signifies the topmost row.

    """
    LITERAL_GRAMMAR = {True: "#", False: ".", None: " "}

    def __init__(self, (width, height), defaultValue=None):
        """bitfield: a matrix of pixels"""
        self.bitfield = [[defaultValue for x in xrange(width)]
                         for y in xrange(height)]
        self.width = width
        self.height = height

    def __getitem__(self, (x, y) ):
        """gets the value of the pixel at the specified location"""
        self.checkIndex((x, y))
        return self.bitfield[y][x]

    def __setitem__(self, (x, y), val):
        """sets the value of the pixel at the specified location"""
        self.checkIndex((x, y))
        self.bitfield[y][x] = None if val is None else bool(val)

    def __repr__(self):
        prefix = "PixelRegion("
        argList = []
        for i, line in enumerate(self.toLiteral()):
            argList.append('"{}"'.format(line))

        separation = ",\n" + " " * len(prefix)
        reprOut = prefix + separation.join(argList) + ")"
        return reprOut

    @classmethod
    def literal(cls, *patternLines):
        """creates a new PixelRegion from the given pattern.

        refer to the LITERAL_GRAMMAR constant for usage

        example suggested usage (with default LITERAL_GRAMMAR):
            # makes a V shape:
            PixelRegion.literal("#...#",
                                ".#.#.",
                                "..#..")

        """
        width, height = 0, 0
        for line in patternLines:
            height += 1
            width = max(width, len(line))

        region = PixelRegion((width, height))
        parser = {value: key for key, value
                  in cls.LITERAL_GRAMMAR.iteritems()}

        for y_index, line in enumerate(patternLines):
            for x_index, character in enumerate(line):
                region[x_index, y_index] = parser[character]

        return region

    def checkIndex(self, (x, y)):
        if not (0 <= x < self.width and
                0 <= y < self.height):
            raise IndexError

    def getRows(self):
        return list(self.bitfield)

    def getColumns(self):
        return zip(self.bitfield)

    def toLiteral(self):
        """gets a list of lines in the PixelRegion.literal() format"""
        output = []
        for row in self.bitfield:
            outputRow = ""
            for bit in row:
                outputRow += self.LITERAL_GRAMMAR[bit]
            output.append(outputRow)
        return output

    def paste(self, other, (x_left, y_top)):
        """pastes the given PixelRegion object onto this one"""
        if ((other.width - x_left) > self.width or
            (other.height - y_top) > self.height):
            raise ValueError

        for rowIndex, row in enumerate(other.getRows()):
            for colIndex, character in enumerate(row):
                y = rowIndex + y_top
                x = colIndex + x_left
                if character is not None:
                    self.bitfield[y][x] = character

class LPQRImage( qrcode.image.base.BaseImage ):
    """implementation of qrcode module's image-processing base class"""

    kind = "lpqr"
    allowed_kinds = (kind,)

    def drawrect(self, row, col):
        box = PixelRegion(2 * (self.box_size,), True)
        location = (col * self.box_size + self.border,
                    row * self.box_size + self.border)
        self._img.paste(box, location)

    def save(self, stream, kind=None):
        for line in self._img.toLiteral(self):
            stream.write(line + "\n")

    def new_image(self, **kwargs):
        totalSize = ((self.border * 2) +
                     (self.width * self.box_size))
        return PixelRegion(2 * (totalSize,))

    def get_image(self, **kwargs):
        """temporary(?) override of qrcode library function

        it looks as if this function has an error-- it ought to return the
        object's _img attribute and instead it tries to return _img resulting
        in a NameError. This override fixes that.

        """
        return self._img
