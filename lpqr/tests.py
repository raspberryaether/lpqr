#! /usr/bin/python
###############################################################################
"""\
a few examples/tests
"""

from lpqr.types import PixelRegion, LPQRImage
from lpqr.formatters import FormatterLibrary
from qrcode import QRCode
from hashlib import sha256

def printSeparator(prependNewline=False):
    """just prints a visual separator"""
    print ("\n" if prependNewline else "") + ("-" * 79)

def printDouble(x):
    """this was a hackish way when the formatters hadn't been written yet

    it prints the QR codes at double the width/height (because instead of 2
    pixels stacked vertically per character, each character is half of one
    square.

    it's been left here as an example.

    """
    printSeparator(True)
    for line in x.toLiteral():
        print (line
               .replace(".", "  ")
               .replace("#", "\xe2\x96\x88\xe2\x96\x88")
               .replace(" ", "  "))
    printSeparator()

def testRegions():
    """pixel-region test/example function

    this has most of the important stuff that pixel-regions can do.

    """
    printSeparator(True)
    x = PixelRegion((8, 8))
    print repr(x)
    print "pixel at (1, 1) is {}".format("on" if x[1,1] else "off")
    printSeparator()

    printSeparator(True)
    x[1,1] = True
    print repr(x)
    print "pixel at (1, 1) is {}".format("on" if x[1,1] else "off")
    printSeparator()

    printSeparator(True)
    y = PixelRegion.literal("####",
                            ".  .",
                            "####",
                            ".  .")
    print repr(y)
    x.paste(y, (0, 0))
    print repr(x)
    x.paste(y, (4, 4))
    print repr(x)
    printSeparator()

def buildQRRegion():
    qr = QRCode(box_size=1,
                border=1,
                image_factory=LPQRImage)
    qr.add_data(sha256("").hexdigest())
    qr.make()

    img = qr.make_image().get_image()
    return img

def testQR():
    printSeparator(True)
    img = buildQRRegion()
    print repr(img)
    printDouble(img)
    printSeparator()

def testFormatter():
    printSeparator(True)
    img = buildQRRegion()
    print FormatterLibrary.catalog()
    print FormatterLibrary.HalfBlockFormatter.catalog()
    formatter = FormatterLibrary.HalfBlockFormatter.utf8
    print "\n".join(formatter.format(img))
    printSeparator()

def test():
    for test in [testRegions,
                 testQR,
                 testFormatter]:
        test()

if __name__ == "__main__":
    test()
