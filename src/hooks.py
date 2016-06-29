class Hooks:
    def __init__(self, hook, backup):
        print("Name of backup: {0}".format(backup.confname))

    def pre_hook(self):
        print("PRE HOOK")

    def post_hook(self):
        print("POST HOOK")
