# Usage Bot

This is the code for the [Usage
Bot](https://commons.wikimedia.org/wiki/User:Usage_Bot) on Wikimedia
Commons and on the OpenStreetMap Wiki.  It is based on the
[pywikibot](https://www.mediawiki.org/wiki/Manual:Pywikibot) framework.

## Requirements

To run the bot on a random Linux box, you will probably want a
suitable Python virtual environment.  Run `./mkvenv venv` to create a
virtual environment called `venv` based on `requirements.txt`.

You'll need a suitable `user-config.py`.  This will need to override a
few settings from Pywikibot's `config.py`.  You'll probably want to set:

* `family = 'commons'`
* `mylang = 'commons'`
* `usernames['commons']['commons']` to the bot's user name on Commons
* `usernames['osm']['en']` to the bot's user name on the OSM Wiki
* `authenticate['commons.wikimedia.org']` to the bot's OAuth tokens (see [Manual:Pywikibot/OAuth/Wikimedia](https://www.mediawiki.org/wiki/Manual:Pywikibot/OAuth/Wikimedia))
* `password_file` to the name of a file containing a [bot password](https://www.mediawiki.org/wiki/Manual:Pywikibot/BotPasswords) for the OSM Wiki
* `user_agent_description` to something identifying who is running the bot.

The settings relating to Commons or the OSM Wiki are only required for
those wikis that the bot will be updating.

Any OAuth consumer or bot password that you create for the bot should
have these grants:

* Basic rights (`basic`)
* High-volume editing (`highvolume`)
* Create, edit, and move pages (`createeditmovepage`)

## Running the bot

The `usage-bot` script does all the work of the bot.  It takes all the
usual command-line arguments for a Pywikibot script.  It also has
options that choose which source to use.  These are defined in
`usage_bot/__init__.py`.

## Running on Toolforge

The main version of the bot runs on
[Wikimedia Toolforge](https://wikitech.wikimedia.org/wiki/Portal:Toolforge).
To run the bot there once you have a tool account:

* Check out the bot code under the tool account in a directory called `usage-bot`.
* Provide a suitable `user-config.py` in that directory.
* Run `toolforge-jobs load usage-bot/jobs.yaml` to install the cron jobs.
