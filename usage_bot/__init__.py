import pywikibot

from usage_bot.instantcommons import from_instantcommons
from usage_bot.osm import from_taginfo, from_overpass
from usage_bot.util import canonicalise_name

def filter_files(files):
    # Filter out alleged filenames with impossible characters
    for title in list(files.keys()):
        if '|' in title:
            del files[title]

def from_args(args):
    if '-osm' in args:
        files = from_taginfo()
    elif '-osmwiki' in args:
        files = from_instantcommons(pywikibot.Site("osm:en"),
                                    iwprefix="osmwiki")
    elif '-wikitech' in args:
        files = from_instantcommons(pywikibot.Site("wikitech:en"),
                                    iwprefix="wikitech")
    filter_files(files)
    return files
