import os
import sys
import argparse

import re

BYTES_FINDER = re.compile(r'(\d+(?:\.\d+)?)\s?(k|K|m|M|g|G|t|T)?(B|b)?')
POWERS_D = {'k': 10**3, 'm': 10**6, 'g': 10**9, 't': 10**12}
POWERS_B = {'k': 2**10, 'm': 2**20, 'g': 2**30, 't': 2**40}


def r_scandir(path):
    '''List files and directories recursively.

    Parameters
    ----------
    path : string
        A path to a directory.

    Returns
    -------
    dir_iterator : iterator of DirEntry objects
        Iterator of DirEntry objects, same as `os.scandir`.
    '''
    for entry in os.scandir(path):
        yield entry
        if entry.is_dir():
            yield from r_scandir(entry.path)


def human2bytes(text, binary=True):
    '''Convert a human-readable file size spec to an integer number of bytes.

    Parameters
    ----------
    text : string
        The text to be converted.
    binary : bool, optional
        Whether to use binary multipliers (1024, 1024^2, etc) (default), or
        decimal ones (1000, 1000000, etc).

    Returns
    -------
    bytes_count : int
        The number of bytes matching the input text.

    Examples
    --------
    >>> human2bytes('4500')
    4500
    >>> human2bytes('1.5kb')
    1536
    >>> human2bytes('2MB', False)
    2000000
    '''
    parsed = BYTES_FINDER.match(text)
    if parsed is None:
        raise ValueError('Not a valid size spec: %s. Examples of valid '
                         'specs include 4500, 512MB, 20kb, and 2TB.' % text)
    value = float(parsed.group(1))
    mod = str.lower(parsed.group(2))
    multiplier = POWERS_B[mod] if binary else POWERS_D[mod]
    bytes_count = round(value * multiplier)
    return bytes_count


def flatten(indir, outdir, filetype='', minsize=0, maxsize=None):
    '''Place hardlinks in outdir to all files in nested directories in indir.

    Parameters
    ----------
    indir : string
        The input directory to flatten.
    outdir : string
        The output directory, where to place all the files in `indir`.
    filetype : string, optional
        Link only files with this extension.
    minsize : int, optional
        Link only files larger than this size.
    maxsize : int, optional
        Link only files smaller than this size.
    '''
    filetype = str.lower(filetype)
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    files = r_scandir(indir)
    for entry in files:
        info = entry.stat()
        if (entry.is_dir() or
                info.st_size < minsize or
                (maxsize is not None and info.st_size > maxsize)):
            continue
        if not entry.name.lower().endswith(filetype):
            continue
        src = os.path.abspath(entry.path)
        dst = os.path.join(outdir, entry.name)
        os.link(src, dst)


__version__ = '0.1'

def main():
    parser = argparse.ArgumentParser(description='foo')
    parser.add_argument('indir',
        help='Input directory to flatten.')
    parser.add_argument('outdir',
        help='Output directory: all files recursively found in <indir> '
             'will be placed here. Created if it doesn\'t exist.')
    parser.add_argument('-t', '--filetype',
        help='Only flatten files matching this extension.')
    parser.add_argument('-m', '--minsize', type=human2bytes,
        help='Find only files larger than this size. This can be a human-'
             'readable string, such as \'512kB\'.')
    parser.add_argument('-M', '--maxsize', type=human2bytes,
        help='Find only files smaller than this size. This can be a human-'
             'readable string, such as \'512kB\'.')

    parser.parse_args(sys.argv)

    flatten(parser.indir, parser.outdir, filetype=parser.filetype,
            minsize=parser.minsize, maxsize=parser.maxsize)
