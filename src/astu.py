import textwrap
import argparse
import functools
import subprocess
import os
import sys

from .config import Config
from .hooks import Hooks
from .backup import Backup

def cmd(method):
    """Replace the strings with the respective objects"""
    @functools.wraps(method)
    def wrapper(self, args, **kwargs):
        backup = None
        repository = None
        conf = Config()
        if "backup" in dir(args) and "repository" in dir(args):
            repository = conf.get_repository(args.backup, args.repository)
            backup = conf.get_backup(args.backup)
        elif "backup" in dir(args):
            backup = conf.get_backup(args.backup)
            repository = conf.get_repositories_for_backup(args.backup)

        if not backup:
            print("No backup named that")
            sys.exit()
        if not repository:
            print("No repository named that")
            sys.exit()

        method(self, backup, repository)
    return wrapper


def backup_object(l):
    for i in l:
        if isinstance(i, Backup):
            return i
    return None



def hook(action, pre=True, post=True):
    def decorator_func(func):
        def wrapper_func(*args, **kwargs):
            hook = None
            backup = backup_object(args)
            if backup:
                hook = Hooks(action, backup)

            if pre and hook:
                hook.pre_hook()

            retval = func(*args, **kwargs)

            if post and hook:
                hook.post_hook()

            return retval
        return wrapper_func
    return decorator_func



class Astu:


    def _build_args(self):
        common = argparse.ArgumentParser(add_help=False, prog=None)
        common.add_argument('-h', '--help', action='help', help='show this help message and exit')


        parser = argparse.ArgumentParser(description='Astu - Borg wrapper')
        subparsers = parser.add_subparsers(title='required arguments', metavar='<command>')

        # Backup
        backup_epilog = textwrap.dedent("""
        Starts backups
        """)
        subparser = subparsers.add_parser('backup',
                                          parents=[common],
                                          add_help=False,
                                          description=self.do_backup.__doc__,
                                          epilog=backup_epilog,
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          help='starts backup')
        subparser.add_argument("backup", metavar="BACKUP")
        subparser.add_argument("repository", metavar="REPOSITORY")
        subparser.add_argument('--dry', dest='dry_run',
                            action='store_true', default=False,
                            help='Dry run')
        subparser.set_defaults(func=self.do_backup)

        # Repositories
        backup_epilog = textwrap.dedent("""
        List repositores
        """)
        subparser = subparsers.add_parser('repositories',
                                          parents=[common],
                                          add_help=False,
                                          description=self.do_backup.__doc__,
                                          epilog=backup_epilog,
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          help='list available repositores')
        subparser.add_argument("backup", metavar="BACKUP")
        subparser.set_defaults(func=self.do_repositories)

        return parser

    def parse(self, args):
        """Parses arguments"""
        parser = self._build_args()
        self.args = parser.parse_args(args or ['-h'])

    def run(self):
        return self.args.func(self.args)


    # Commands
    def _run(self, cmd, env={}):
        if not self.args.dry_run:
            process_env = {**os.environ.copy(), **env}
            process = subprocess.Popen(cmd, env=process_env, shell=True)
            process.wait()
            rc = process.returncode
        else:
            print("Cmd: {0}".format(cmd))
            print("Env:")
            for k,v in env.items():
                print("{0} {1}".format(k,v))


    def repo_path(repo, name, prefix):
        pass


    @cmd
    def do_init(self, repository):
        pass


    @cmd
    @hook("backup")
    def do_backup(self, backup, repository):
        """Does the backup"""
        args = {}
        args["env"] = repository.get_env()
        args["cmd"] = "borg create"
        args["flags"] = backup.get_all_flags()
        # repo = self.repo_path(repository.repository, backup.name, backup.prefix)
        args["repo"] = ""
        args["path"] = backup.dir
        cmd = "{env} {cmd} {flags} {repo} {path}".format(**args)
        return self._run(cmd, env={**repository.env, **backup.env})


    @cmd
    def do_repositories(self, backup, repositories):
        print("Backup:")
        print("* {0}".format(backup.confname))
        print("\tName: {0}".format(backup.name))
        print("\tDirectory: {0}".format(backup.dir))

        print("Repositories:")
        for i in repositories:
            print("* {0}".format(i.confname))
            print("\tRepository: {0}".format(i.repository))


    @cmd
    def do_list(self, backup, repositories):
        pass


    @cmd
    def do_prune(self, backup, repository):
        pass




