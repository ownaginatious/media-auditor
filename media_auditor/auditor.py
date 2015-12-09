import json
import os
import subprocess
import logging
import sys
import tempfile

class MediaAuditor(object):

    LOGGER = logging.getLogger(__name__)
    NOT_MEDIA = "Invalid data found when processing input"

    def find_media_files(self):

        for d, subdirs, files in os.walk('/Users/dillon/Dropbox'):
            for f in files:
                f = d + "/" + f

                # Don't check non-regular files (e.g. socket/device handles)
                if not os.path.isfile(f):
                    continue

                with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:

                    p = subprocess.Popen(['ffprobe', '-show_streams', '-print_format', 'json', f],
                            stdout=stdout,
                            stderr=stderr)

                    code = p.wait()

                    stdout.seek(0)
                    stderr.seek(0)

                    out = stdout.read().decode('utf-8')
                    err = stderr.read().decode('utf-8')

                    if code == 0:
                        data = json.loads(out)
                        data['path'] = f
                        yield data
                    elif self.NOT_MEDIA in err:
                        self.LOGGER.debug("The file is not a media file '{}'".format(f))
                    else:
                       self.LOGGER.warn("Error probing '{}': {}...".format(f, err[0:30]))

logger = logging.getLogger(MediaAuditor.__name__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

ma = MediaAuditor()
print("Found {} media files".format(len([x for x in ma.find_media_files()])))
