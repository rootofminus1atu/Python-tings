


class BotDev:
    def __init__(self, name, dev: bool, tester: bool):
        self.name = name
        self.dev = dev
        self.tester = tester

    @classmethod
    def get_users(cls):
        return [
            cls("bud", dev=True, tester=True),
        ]