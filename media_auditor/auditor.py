import json
import os
import subprocess

NOT_MEDIA = "Invalid data found when processing input"

for d, subdirs, files in os.walk("."):
    for f in files:
        f = d + "/" + f

        # Don't check non-regular files (e.g. socket/device handles)
        if not os.path.isfile(f):
            continue

        p = subprocess.Popen(['ffprobe', '-show_streams', '-print_format', 'json', f],\
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        code = p.wait()
        stdout, stderr = p.communicate()
        stdout, stderr = stdout.decode("utf-8"), stderr.decode("utf-8")
        if code == 0:
            print("Data discovered for: '%s'" % f)
            data = json.loads(stdout)
            for num, data in enumerate(data['streams']):
                print('%s: %s' % (num, data['codec_name']))
        elif NOT_MEDIA in stderr:
            print("File '%s' is not a media file" % f)
        else:
            print("Error reading '%s': %s" % (f, stderr))
