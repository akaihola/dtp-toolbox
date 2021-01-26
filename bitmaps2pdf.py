#!/usr/bin/env python3

import logging
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas


def get_pdfpath(output: str, paths: List[str]) -> Path:
    if output:
        return Path(output)
    first, *rest = [Path(path) for path in paths]
    shortest_imgname = min(len(img.name) for img in [first] + rest)
    for length in range(shortest_imgname, 0, -1):
        if all(img.name[:length] == first.name[:length] for img in rest):
            if all(img.parent == first.parent for img in rest):
                pdfdir = first.parent
            else:
                pdfdir = Path.cwd()
            output_name = first.name[:length].rstrip(".")
            return Path(pdfdir / f"{output_name}.pdf")
    raise ValueError(
        "-o / --output missing and the target PDF file name counldn't be"
        " dertermined automatically"
    )


def main(opts: Namespace) -> None:
    pdfpath = get_pdfpath(opts.output, opts.imgpaths)
    if not opts.force and pdfpath.exists():
        raise OSError("File {pdfpath} exists. Use --force/-f option to overwrite.")
    canvas = Canvas(str(pdfpath), pagesize=A4, pageCompression=1)
    for imgpath in opts.imgpaths:
        widthpx, heightpx = Image.open(imgpath).size
        logging.info("%4d x %4d %s", widthpx, heightpx, imgpath)
        widthpt = 72.0 * widthpx / 300.0
        heightpt = 72.0 * heightpx / 300.0
        x = (A4[0] - widthpt) / 2.0
        ymarg = min((A4[1] - heightpt) / 2.0, x)
        y = A4[1] - ymarg - heightpt
        canvas.drawImage(imgpath, x, y, width=widthpt, height=heightpt)
        canvas.showPage()
    logging.info("%5d pages %s" % (len(opts.imgpaths), pdfpath))
    canvas.save()


def parse_cmdline():
    parser = ArgumentParser()
    parser.add_argument("-q", "--quiet", action="count")
    parser.add_argument("-f", "--force", action="store_true")
    parser.add_argument("-o", "--output")
    parser.add_argument("imgpaths", nargs="+")
    return parser.parse_args()


if __name__ == "__main__":
    opts = parse_cmdline()

    loglevel = 20 + 10 * (min(3, opts.quiet or 0))
    logging.basicConfig(level=loglevel, format="%(message)s")

    main(opts)
