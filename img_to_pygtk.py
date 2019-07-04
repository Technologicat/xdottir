#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Written in 2011 by Bjarni R. Einarsson <http://bre.klaki.net/>
# This script is in the Public Domain.
#
# Converted in 2019 to Python 3 and PyGObject by Juha Jeronen.
#
# This is a simple tool for converting image files to compact PyGObject code for
# embedding in Python scripts.  It can read whatever formats PyGObject can.
#
# For a more general-purpose Python embedding tool, check out PyBreeder:
#  - http://pagekite.net/wiki/Floss/PyBreeder/
#
import base64
import sys
import zlib

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def image_to_code(varname, filename):
    img = Gtk.Image()
    img.set_from_file(filename)
    pb = img.get_pixbuf()
    pb64 = base64.b64encode(zlib.compress(pb.get_pixels(), 9))
    pb64 = pb64.decode("ascii")  # bytes -> str
    data = ''
    while len(pb64) > 0:
        data += "    '{}'\n".format(pb64[0:78])
        pb64 = pb64[78:]
    s = '{} = GdkPixbuf.Pixbuf.new_from_data({})'
    return s.format(varname, ', '.join(str(p) for p in [
                                   'zlib.decompress(base64.b64decode(\n{}\n     ))'.format(data[:-1]),
                                   'GdkPixbuf.Colorspace.RGB',
                                   pb.get_has_alpha(), pb.get_bits_per_sample(),
                                   pb.get_width(), pb.get_height(),
                                   pb.get_rowstride()]))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        args.append('PIXBUF')
        print(image_to_code(args[1], args[0]))
        print()
        print("# Imports you'll need to run that:\n"
              "import zlib\n"
              "import base64\n"
              "import gi\n"
              "gi.require_version('Gtk', '3.0')\n"
              "from gi.repository import GdkPixbuf")
    else:
        print('Usage: %s file.png [variable-name]' % sys.argv[0])
        sys.exit(1)
