from datetime import datetime
import os
import time

class Watcher(object):
    def __init__(self):
        self.mtime_last = 0
        # path to file to watch
        self.file_name = '/Users/bhavrilesko/Downloads/aws_saml_credentials.txt'
        # path to morningstar env
        self.env_path = '/Users/bhavrilesko/Repos/Homestead/morningstar/.env'

    def watch(self):
        while True:
            time.sleep(5)
            mtime_cur = os.path.getmtime(self.file_name)
            if mtime_cur != self.mtime_last:
                self.work()
            self.mtime_last = mtime_cur

    def work(self):
        # get the values from the updated file
        source = open(self.file_name, 'rt')
        while True:
            line = source.readline()
            if not line:
                break

            if line.startswith('aws_access_key_id'):
                aws_access_key_id = line[20:]
            elif line.startswith('aws_secret_access_key'):
                aws_secret_access_key = line[24:]
            elif line.startswith('aws_session_token'):
                aws_session_token = line[20:]

        source.close()

        # read the old env to get contents and replace
        # aws credentials
        destination = open(self.env_path, 'rt')
        contents = ""
        while True:
            line = destination.readline()
            if not line:
                break

            if line.startswith('AWS_ACCESS_KEY_ID'):
                contents = contents + "AWS_ACCESS_KEY_ID=" + aws_access_key_id
            elif line.startswith('AWS_SECRET_ACCESS_KEY'):
                contents = contents + "AWS_SECRET_ACCESS_KEY" + aws_secret_access_key
            elif line.startswith('AWS_SESSION_TOKEN'):
                contents = contents + "AWS_SESSION_TOKEN" + aws_session_token
            else:
                contents = contents + line

        destination.close()

        # open the env again to overwrite contents
        destination = open(self.env_path, "wt")
        destination.write(contents)
        destination.close()

        # print update time to terminal
        now = datetime.now()
        print('Credentials updated at', now.strftime("%m/%d/%Y, %H:%M:%S"))

# start the file watcher the watcher
watcher = Watcher()
watcher.watch()