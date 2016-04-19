#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce
import json
from operator import and_
from os import walk
from pathlib import Path
from subprocess import Popen, PIPE
import sys
import shutil


class FFProbeNotFoundError(Exception):
    pass


class NotAMediaFileError(Exception):
    pass


class CorruptedMediaError(Exception):
    def __init__(self, path, reason):
        self.reason = reason
        super(CorruptedMediaError, self).__init__(path)


_NOT_MEDIA = "Invalid data found when processing input"
_COMMAND = ('ffprobe', '-show_streams', '-print_format', 'json')

def scan(path, ignore_nonmedia=True, skip_failures=True, filters=()):
    for d, _, files in walk(path):
        for f in (Path(d).joinpath(x) for x in files):
            try:
                rc = probe_file(f)
                if not reduce(and_, (fi(rc) for fi in filters)):
                    continue
                yield probe_file(f)
            except NotAMediaFileError as e:
                if not ignore_nonmedia:
                    return dict(path=e.message, error='not a media file')
            except CorruptedMediaError as e:
                if not skip_failures:
                    return dict(path=e.message, error=e.reason)

def probe_file(path):

    # Skip non-regular files (e.g. socket/device handles)
    if not path.is_file():
        raise NotAMediaFileError(path.path)
    command = _COMMAND + (str(path),)
    with Popen(command, stdout=PIPE, stderr=PIPE) as p:
        stdout, stderr = p.communicate()
        stdout, stderr = stdout.decode('utf-8'), stderr.decode('utf-8')
        if p.returncode == 0:
            data = json.loads(stdout)
            data['path'] = str(path)
            return data
        elif _NOT_MEDIA in (stdout + stderr):
            raise NotAMediaFileError(str(path))
        else:
            raise CorruptedMediaError(str(path), stderr)


# Check to make sure that ffprobe is available.
if not shutil.which('ffprobe'):
    raise FFProbeNotFoundError('ffprobe installation was not found '
                               'on this system')
