import sys
import yaml
import textwrap
import argparse
import functools
import subprocess
import os

class Astu:
    def __init__(self, backups={}, repositories={}):
        self.backups = backups
        self.repositories = repositories

    def cmd(method):
        @functools.wraps(method)
        def wrapper(self, args, **kwargs):
            backup = self.backups.get(args.backup, None)
            repository = self.repositories.get(args.repository, None)
            if not backup:
                print("No backup named that")
                sys.exit()
            if not repository:
                print("No repository named that")
                sys.exit()

            return method(self, backup, repository)
        return wrapper


    def _build_args(self):
        parser = argparse.ArgumentParser(description='Astu - Borg wrapper')
        subparsers = parser.add_subparsers(title='required arguments', metavar='<command>')
        backup_epilog = textwrap.dedent("""
        Starts backups
        """)
        subparser = subparsers.add_parser('backup',
                                          description=self.do_backup.__doc__,
                                          epilog=backup_epilog,
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          help='starts backup')
        subparser.add_argument("backup", metavar="BACKUP")
        subparser.add_argument("repository", metavar="REPOSITORY")
        subparser.set_defaults(func=self.do_backup)
        return parser

    def parse(self, args):
        """Parses arguments"""
        parser = self._build_args()
        self.args = parser.parse_args(args)

    def run(self):
        return self.args.func(self.args)


    # Commands
    def _run(self, cmd, env={}):
        process_env = {**os.environ.copy(), **env}
        process = subprocess.Popen(cmd, env=process_env, shell=True)
        process.wait()
        rc = process.returncode

    @cmd
    def do_init(self, repository):
        pass

    @cmd
    def do_backup(self, backup, repository):
        """Does the backup"""
        args = {}
        args["env"] = repository.get_env()
        args["cmd"] = "borg create"
        args["flags"] = backup.get_all_flags()
        args["repo"] = repository.repository + "::" + backup.name
        args["path"] = backup.dir
        cmd = "{env} {cmd} {flags} {repo} {path}".format(**args)
        return self._run(cmd, env={**repository.env, **backup.env})

    @cmd
    def do_prune(self, backup, repository):
        pass




