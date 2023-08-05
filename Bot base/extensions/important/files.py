class Files:
    statuses = [
        "Making cakes",
        "Making cookies",
        "Making pies",
        "Making bread",
    ]

    papiez = "https://www.youtube.com/watch?v=2yusdx60_aw"

async def setup(bot):
    bot.files = Files()