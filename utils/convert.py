#!/usr/bin/env python3

import io
import bz2
import csv
import gzip
import json
import pathlib
import argparse
import subprocess
from typing import Optional, Union


def decompressor_7z(file_path: str):
    """"Return a file-object that decompresses data using 7z."""
    p = subprocess.Popen(
        ['7z', 'e', '-so', file_path],
        stdin=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
    )
    return io.TextIOWrapper(p.stdout, encoding='utf-8')


def compressor_7z(file_path: str):
    """"Return a file-object that compresses data using 7z."""
    p = subprocess.Popen(
        ['7z', 'a', '-si', file_path],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    return io.TextIOWrapper(p.stdin, encoding='utf-8')


def smart_open(path: Union[str, pathlib.Path],
               mode: Optional[str] = None,
               encoding: Optional[str] = 'utf-8'):
    """Open a file, decompressing it if necessary."""

    ext = pathlib.Path(path).suffix
    path_str = str(path)

    if ext == '.7z' or ext == '.lzma':
        f = decompressor_7z(path_str)
    elif ext == '.bz2':
        mode = 'rb' if mode is None else mode
        f = bz2.open(path_str, mode=mode)
    elif ext == '.gz':
        mode = 'rb' if mode is None else mode
        f = gzip.open(path_str, mode=mode)
    else:
        f = path.open(mode)

    return f


def output_writer(path: str, compression: Optional[str]):
    """Write data to a compressed file."""
    if compression == '7z':
        return compressor_7z(path + '.7z')
    if compression == 'bz2':
        return bz2.open(path + '.bz2', 'wt', encoding='utf-8')
    elif compression == 'gzip':
        return gzip.open(path + '.gz', 'wt', encoding='utf-8')
    else:
        return open(path, 'wt', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('files',
                        metavar='FILE',
                        type=pathlib.Path,
                        nargs='+',
                        help='A list of files to process.'
                        )
    parser.add_argument('-o', '--output-dir',
                        type=pathlib.Path,
                        default=pathlib.Path('output'),
                        help='Output directory for processed results [default: ./output].',
                        )
    parser.add_argument('--output-compression',
                        choices={None, '7z', 'bz2', 'gzip'},
                        required=False,
                        default=None,
                        help='Output compression format [default: None].',
                        )

    args = parser.parse_args()

    if not args.output_dir.exists():
        args.output_dir.mkdir(parents=True)

    outfile_name = args.files[0].with_suffix('').stem + '.csv'
    outfile = output_writer(path=str(args.output_dir/outfile_name),
                            compression=args.output_compression)
    writer = csv.writer(outfile, delimiter='\t')
    writer.writerow(['user_name', 'id_talk_page', 'uw_name',
                     'category', 'timestamp', 'transcluded'])

    for afile in args.files:
        with smart_open(afile, mode='rt', encoding='utf-8') as infile:
            for line in infile:
                data = json.loads(line)
                
                # keys:
                # user_warnings_recieved, user_warnings_stats, name, id_talk_page
                # user_warnings_recieved:
                #   - category
                #   - parameters
                #     - timestamp
                #     - options
                #   - transcluded
                #   - user_warning_name
                user_name = data['name']
                id_talk_page = int(data['id_talk_page'])

                for uw in data['user_warnings_received']:
                    uw_name = uw['user_warning_name']
                    category = uw['category']
                    transcluded = 1 if uw['transcluded'] else 0
                    for uw_param in uw['parameters']: 
                        timestamp = uw_param['timestamp']

                        writer.writerow([user_name, id_talk_page, uw_name,
                                         category, timestamp, transcluded])

    outfile.close()
    exit(0)
