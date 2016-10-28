import os.path
import subprocess

class Hooks:
    def __init__(self, hook, backup):
        print("Name of backup: {0}".format(backup.confname))
        self.hook_path = os.path.abspath(".")+"/hooks/{0}".format(backup.confname)
        self.hook = hook
        print(self.hook_path)

    def _run(self, cmd, env={}):
        if os.path.isfile(cmd):
            process_env = {**os.environ.copy(), **env}
            process = subprocess.Popen(cmd, env=process_env, shell=True)
            process.wait()
            rc = process.returncode
        else:
            print("Error, no such hook")

    def pre_hook(self):
        self._run("{0}/pre-{1}".format(self.hook_path,self.hook))

    def post_hook(self):
        self._run("{0}/post-{1}".format(self.hook_path,self.hook))
