

"""
example config for servers:
{
    "server_id": 123456789,
    "channel_id": 123456789,
    "time": 8,
    "birthdays": []
}

example config for dms:
{
    "user_id": 123456789,
    "time": 8,
    "birthdays": []
}
"""

class Manager:
    def create_config_server(self, server, channel, time):
        print(f"Created {server} config with {channel} {time}")

    def get_config_server(self, server):
        print(f"Got {server} config")

    def create_config_dm(self, user, time):
        print(f"Created {user} config with {time}")

    def get_config_dm(self, user):
        print(f"Got {user} config")


    def add_birthday(self, birthday, config):
        print(f"Added {birthday} to {config}")


    

