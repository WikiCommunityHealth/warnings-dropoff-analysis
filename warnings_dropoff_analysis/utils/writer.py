from typing import Optional
import gzip
import bz2
import subprocess
import io

def compressor_7z(file_path: str) -> io.TextIOWrapper:
    """"Return a file-object that compresses data written using 7z."""
    p = subprocess.Popen(
        ['7z', 'a', '-si', file_path],
        stdin=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    return io.TextIOWrapper(p.stdin, encoding='utf-8')


def output_writer(path: str, compression: Optional[str]) -> io.TextIOWrapper:
    """Write data to a compressed file."""
    if compression == '7z':
        return compressor_7z(path + '.7z')
    if compression == 'bz2':
        return bz2.open(path + '.bz2', 'wt', encoding='utf-8')
    elif compression == 'gzip':
        return gzip.open(path + '.gz', 'wt', encoding='utf-8')
    else:
        return open(path, 'wt', encoding='utf-8')