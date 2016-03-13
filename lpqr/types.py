#! /usr/bin/python
###############################################################################
"""\
provides data types for use with lpqr
"""

class PixelRegion(object):
    """represents a rectangle of pixels.

    an X value of 0 signifies the leftmost column; a Y value
    of 0 signifies the topmost row.

    """
    def __init__(self, size_x, size_y):
        """bitfield: a matrix of pixels"""
        self.bitfield = [[False for x in xrange(size_x)]
                         for y in xrange(size_y)]
        self.width = size_x
        self.height = size_y

    def __getitem__(self, (x, y) ):
        """gets the value of the pixel at the specified location"""
        self.checkIndex((x, y))
        return self.bitfield[y][x]

    def __setitem__(self, (x, y), val):
        """sets the value of the pixel at the specified location"""
        self.checkIndex((x, y))
        self.bitfield[y][x] = bool(val)

    @classmethod
    def literal(cls, *patternLines):
        """creates a new PixelRegion from the given pattern.

        use the character '#' for True pixels.
        use the character '.' for False pixels.

        suggested usage:
            # makes a V shape:
            PixelRegion.literal("#...#",
                                ".#.#.",
                                "..#..")

        """
        width, height = 0, 0
        for line in patternLines:
            height += 1
            width = max(width, len(line))

        region = PixelRegion(width, height)
        parser = {"#": True, ".": False}

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
                outputRow += "#" if bit else "."
            output.append(outputRow)
        return output

    def paste(self, other, (x_left, y_top)):
        """pastes the given PixelRegion object onto this one"""
        if ((other.width - x_left) > self.width or
            (other.height - y_top) > self.height):
            raise ValueError

        x_slice = slice(x_left, x_left + other.width)
        for index, row in enumerate(other.getRows()):
            self.bitfield[index + y_top][x_slice] = row
