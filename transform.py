#!/usr/bin/env python

import sys
import os
import pathlib
import magic
import multiprocessing as mp

import tqdm
import bs4
from selectolax.parser import HTMLParser


def _read(fname):
    if 'gzip compressed' in magic.from_file(fname):
        import gzip
        f = gzip.open(fname)
    else:
        f = open(fname, 'rb')
    html = f.read().decode('utf-8')
    f.close()
    return html


def process(fname):
    if not fname.endswith('.html'):
        return

    html = _read(fname)

    tree = HTMLParser(html)
    for selector in [
            "div.bd-sidebar",
            "div.header-article",
            "footer.footer-article",
            "script"]:
        for node in tree.css(selector):
            node.decompose()

    soup = bs4.BeautifulSoup(tree.html, "lxml")
    for mc in soup.findAll(attrs={"id": 'main-content'}):
        # Change its id because CSS limits its width to 70%.
        # We don't want this limit inside zeal/dash.
        mc['id'] = 'main-content-custom'

    with open(fname, 'w') as f:
        f.write(str(soup))


if __name__ == '__main__':
    path = os.path.abspath(sys.argv[1])
    if os.path.isfile(path):
        process(path)
    elif os.path.isdir(path):
        files = pathlib.Path(path).glob("**/*.html")
        files = [os.fspath(x) for x in files]
        pool = mp.Pool(int(os.cpu_count() * 1.5))
        for _ in tqdm.tqdm(
            pool.imap_unordered(process, files, chunksize=20),
            total=len(files)
        ):
            pass
        pool.close()
