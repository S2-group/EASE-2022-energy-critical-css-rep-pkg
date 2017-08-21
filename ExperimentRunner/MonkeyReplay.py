from Script import Script
import subprocess
import paths


class MonkeyReplayError(Exception):
    pass


# https://github.com/LoganD/MonkeyRunner
class MonkeyReplay(Script):
    def __init__(self, path, timeout=0, logcat_regex=None, monkeyrunner_path='monkeyrunner'):
        super(MonkeyReplay, self).__init__(path, timeout, logcat_regex)
        self.monkeyrunner = monkeyrunner_path
        self.logger.debug('Script path: %s' % self.path)
        # TODO: Check if jyson and the player files exist

    def execute_script(self, device):
        super(MonkeyReplay, self).execute_script(device)
        # https://docs.python.org/2/library/subprocess.html
        args = {
            'monkey': self.monkeyrunner,
            'plugins': ['jyson-1.0.2.jar'],
            'program': 'MonkeyReplay/replayLogic.py',
            'replay': self.path,
        }
        args['plugins'] = ' '.join(['-plugin %s' % p for p in args['plugins']])
        args = '{monkey} {plugins} {program} {replay}'.format(**args).split(' ')
        cmdp = subprocess.Popen(args, cwd=paths.ROOT_DIR, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output, error = cmdp.communicate()
        return_code = cmdp.wait()
        if return_code != 0:
            raise MonkeyReplayError(output)
        return return_code