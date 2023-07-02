


class BotDev:
    def __init__(self, nickname: str, id: int, dev: bool, tester: bool):
        self.nickname = nickname
        self.id = id
        self.dev = dev
        self.tester = tester

    @classmethod
    def get_users(cls):
        return [
            cls("gibbal", 698905167629647882, dev=True, tester=True),
            cls("bruh", 9, dev=True, tester=True),
            cls("neonz", 748576224435109899, dev=False, tester=True),
        ]  # is storing notable botdev users like this better than using a dict outside the class? idk
    
    def __repr__(self):
        return f"BotDev(nickname={self.nickname}, id={self.id}, dev={self.dev}, tester={self.tester})"

