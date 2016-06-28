import yaml
from .repository import Repository
from .backup import Backup

class Config:
    def __init__(self):
        with open("./config.yml") as f:
            self.config = yaml.load(f.read())

    def get_backup(self, backup):
        for k,v in self.config["backups"].items():
            if k == backup:
                return Backup(k, **v)
        return None

    def get_backups(self):
        return [Backup(k, **v) for k,v in self.config["backups"].items()]

    def get_available_repositories(self):
        return [Repository(k, **v) for k,v in self.config["repositories"].items()]

    def get_repositories_for_backup(self, backup):
        repositories = []
        for k,v in self.config["backups"].items():
            if k == backup and v.get("repositories"):
                for name, values in v["repositories"].items():
                    repositories.append(Repository(name,**values))
        if not repositories:
            return self.get_available_repositories()
        return repositories

    def get_repository(self, backup, repo):
        repos = self.get_repositories_for_backup(backup)
        if not repos:
            repos = self.get_available_repositories()
        for i in repos:
            if i.confname == repo:
                return i





