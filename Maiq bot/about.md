# Mai'q the Liar

A general all-purpose discord bot inspired by the Khajiit "Mai'q" from The Elder Scrolls games. Currently serves as both a prototype for a different bot created for a friend and as a way for me to improve. The code is maintained regularly.

# Features
- A bunch of fun commands like `/cat`, `/calculate`, `/translate` which do what you expect them to do.
- Info commands that are generally fit for any server.
- `/warn` commands for moderation purposes.
- An automod system. You can prohibit words 
- Timed and schedules events (for example adding a heart reaction to a post in channel X).

# To be added:
- A birthday reminder system.
- Music playing capabilities.
- Making Mai'q talk with the help of chatgpt, instead of just keeping a list of example responses.

# Details
The warn and automod systems were built using a mongodb database. Currently it's operated via `PyMongo`, but I'm about to transition to `Motor`, to keep my db-related methods non-blocking. 
