from itertools import chain
import json
import pywikibot.data.api as api
import pywikibot

from usage_bot.util import canonicalise_name

# This is currently specific to the Wikibase instance on the
# OpenStreetMap Wiki.

class from_wikibase(dict):
    def __init__(self, site, iwprefix=None):
        # To find values of a particular property, we search for links
        # to it from items (namespace 120), which is how uses of it appear.
        parameters = dict(
            generator='backlinks', gblnamespace=120,
            gblfilterredir='nonredirects',
            prop='revisions', rvprop='content', rvslots="main")
        if iwprefix == None:
            parameters['prop'] += '|info'
            parameters['inprop'] = 'url'
        g_p28 = api.QueryGenerator(site=site, parameters=parameters |
                                   dict(gbltitle="Property:P28"))
        g_p39 = api.QueryGenerator(site=site, parameters=parameters |
                                   dict(gbltitle="Property:P39"))
        for f in chain(g_p28, g_p39):
            slot = f['revisions'][0]['slots']['main']
            if (slot['contentmodel'] != 'wikibase-item' or
                slot['contentformat'] != 'application/json'):
                continue
            item = json.loads(slot['*'])
            # Only search top-level claims for now.
            for claim in (item['claims'].get('P28', []) +
                          item['claims'].get('P39', [])):
                if claim['mainsnak']['snaktype'] != 'value': continue
                title = claim['mainsnak']['datavalue']['value']
                title = canonicalise_name(title)
                if title in self:
                    self[title] += "<br/>"
                else:
                    self[title] = f"{title}<br/>"
                if iwprefix == None:
                    self[title] += f"[{f['fullurl']} {f['title']}]"
                else:
                    self[title] += f"[[{iwprefix}:{f['title']}]]"

