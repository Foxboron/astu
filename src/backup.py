class Backup:
    def __init__(self, confname, name="", dir="", env={}, exclude={}, options=[], repositories=[]):
        self.confname = confname
        self.name = name
        self.dir = dir
        self.exclude = exclude
        self.options = options
        self.env = env

    def _parse_options(self, options):
        return " ".join(["--{flag}".format(flag=i) for i in options])

    def _parse_list(self, name, l):
        return " ".join(["--{name}=\"{value}\"".format(name=name, value=i) for i in l])

    def get_all_flags(self):
        flags = {}
        flags["options"] = self._parse_options(self.options)
        flags["exclude"] = self._parse_list("exclude", self.exclude)
        return "{options} {exclude}".format(**flags)
