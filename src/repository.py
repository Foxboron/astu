class Repository:
    def __init__(self, confname, repository="", env={}, prune={}):
        self.confname = confname
        self.repository=repository
        self.env = env
        self.prune = prune

    def get_prune():
        return

    def get_env(self):
        return " ".join(["{key}={value}".format(key=k, value=v) for k,v in self.env.items()])

    def get_repository():
        pass

