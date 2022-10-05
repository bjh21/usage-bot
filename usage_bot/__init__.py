import pywikibot

from usage_bot.instantcommons import from_instantcommons
from usage_bot.osm import from_taginfo, from_overpass
from usage_bot.util import canonicalise_name, summary_revision
from usage_bot.wikibase import from_wikibase

def filter_files(files):
    # Filter out alleged filenames with impossible characters
    for title in list(files.keys()):
        if '|' in title:
            del files[title]

def from_args(args):
    # Process global arguments in case we've using a MediaWiki target.
    args = pywikibot.handle_args(args)

    if '-osm' in args:
        files = from_taginfo()
    elif '-osmwiki' in args:
        files = from_instantcommons(pywikibot.Site("osm:en"),
                                    iwprefix="osmwiki")
    elif '-wikitech' in args:
        files = from_instantcommons(pywikibot.Site("wikitech:en"),
                                    iwprefix="wikitech")
    elif '-wmat' in args:
        files = from_instantcommons(pywikibot.Site("wmat:de"),
                                    iwprefix="wmat")
    elif '-wmau' in args:
        files = from_instantcommons(pywikibot.Site("wmau:en"),
                                    iwprefix="wmau")
    elif '-wmczold' in args:
        files = from_instantcommons(pywikibot.Site("wmczold:cs"),
                                    iwprefix="wmcz_old")
    elif '-wmczdocs' in args:
        files = from_instantcommons(pywikibot.Site("wmczdocs:cs"),
                                    iwprefix="wmcz_docs")
    elif '-wmau' in args:
        files = from_instantcommons(pywikibot.Site("wmau:en"),
                                    iwprefix="wmau")
    elif '-wmdc' in args:
        files = from_instantcommons(pywikibot.Site("wmdc:en"),
                                    iwprefix="wmdc")
    elif '-wmhu' in args:
        files = from_instantcommons(pywikibot.Site("wmhu:hu"),
                                    iwprefix="wmhu")
    elif '-wmuk' in args:
        files = from_instantcommons(pywikibot.Site("wmuk:en"),
                                    iwprefix="wmuk")
    elif '-regiowiki' in args:
        files = from_instantcommons(pywikibot.Site("regiowiki:de"),
                                    iwprefix="regiowiki")
    elif '-osmwikibase' in args:
        # Empty iwprefix assumes page will go on OSM Wiki
        files = from_wikibase(pywikibot.Site("osm:en"), iwprefix="")
    filter_files(files)
    return files
