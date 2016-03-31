import json
from os import walk
from pathlib import Path
from subprocess import Popen
import sys


class NotAMediaFileError(Exception):
    pass


class CorruptedMediaError(Exception):
    def __init__(self. path, reason):
        self.reason = reason
        super(CorruptedMediaError, self).__init__(path)


class MediaAuditor(object):

    _NOT_MEDIA = "Invalid data found when processing input"
    _COMMAND = ('ffprobe', '-show_streams', '-print_format', 'json')

    @staticmethod
    def scan(path, ignore_nonmedia=True, skip_failures=True):
        for d, _, files in walk(path):
            for f in (Path(d).joinpath(x) for x in files):
                try:
                    yield self.probe_file(f)
                except NotAMediaFileError as e:
                    if not ignore_nonmedia:
                        return dict(path=e.message, error='not a media file')
                except CorruptedMediaError as e:
                    if not skip_failures:
                        return dict(path=e.message, error=e.reason)

    @staticmethod
    def probe_file(path):

        # Skip non-regular files (e.g. socket/device handles)
        if not path.is_file():
            continue
        command = MediaAuditor._COMMAND + (path.path,)
        with Popen(command, stdout=PIPE, stderr=PIPE) as p:
            output = p.read().decode('utf-8')
            code = p.wait()
            if code == 0:
                data = json.loads(output)
                data['path'] = path.path
            elif MediaAuditor._NOT_MEDIA in output:
                raise NotAMediaFileError(path.path)
            else:
                raise CorruptedMediaError(path.path, output)
