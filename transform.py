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

    # Add Katex support, and fix its style.
    KATEX = """
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.2/dist/katex.min.css" integrity="sha384-bYdxxUwYipFNohQlHt0bjN/LCpueqWz13HufFEV1SUatKs1cm4L6fFgCi1jT643X" crossorigin="anonymous">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.2/dist/katex.min.js" integrity="sha384-Qsn9KnoKISj6dI8g7p1HBlNpVx0I8p1SvlwOldgi3IorMle61nQy4zEahWYtljaz" crossorigin="anonymous"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.2/dist/contrib/auto-render.min.js" integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05" crossorigin="anonymous"
        onload="renderMathInElement(document.body);"></script>
    <style> div.math { display: inherit; } </style>
"""
    head = soup.findAll('head')[0]
    katex = bs4.BeautifulSoup(KATEX, 'lxml')
    head.extend(katex.html.head.children)

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
