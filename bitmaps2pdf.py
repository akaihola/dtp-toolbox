#!/usr/bin/env python
# -*- coding: utf-8 -*-


# CONFIGURATION ########################################################


# END OF CONFIGURATION #################################################


from optparse import OptionParser
import logging
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import Image
from os.path import exists


def unittest():
    from doctest import testmod
    testmod()


def main(filepaths, opts):
    if len(filepaths) == 1:
        imgpaths = filepaths[:1]
        pdfpath = '%s.pdf' % imgpaths[0].rsplit('.', 1)[0]
    else:
        imgpaths = filepaths[:-1]
        pdfpath = filepaths[-1]
    if not opts.force and exists(pdfpath):
        raise OSError('File %r exists. '
                      'Use --force/-f option to overwrite.' % pdfpath)
    c = canvas.Canvas(pdfpath, pagesize=A4, pageCompression=1)
    for imgpath in imgpaths:
        widthpx, heightpx = Image.open(imgpath).size
        logging.info('%4d x %4d %s' % (widthpx, heightpx, imgpath))
        widthpt = 72.0*widthpx/300.0
        heightpt = 72.0*heightpx/300.0
        x = (A4[0] - widthpt) / 2.0
        ymarg = min((A4[1] - heightpt) / 2.0, x)
        y = A4[1] - ymarg - heightpt
        c.drawImage(imgpath, x, y,
                    width=widthpt,
                    height=heightpt)
        c.showPage()
    logging.info('%5d pages %s' % (len(imgpaths), pdfpath))
    c.save()


if __name__ == '__main__':
    p = OptionParser()
    p.usage = 'usage: %prog imgfile [imgfile ...] outfile.pdf'
    p.add_option('-u', '--unittest', action='store_true')
    p.add_option('-q', '--quiet', action='count')
    p.add_option('-f', '--force', action='store_true')
    (opts, args) = p.parse_args()

    loglevel = 20 + 10*(min(3, opts.quiet or 0))
    logging.basicConfig(level=loglevel, format='%(message)s')

    if opts.unittest:
        unittest()

    else:
        main(args, opts)

