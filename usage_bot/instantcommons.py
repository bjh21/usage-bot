import pywikibot.data.api as api
import pywikibot

class from_instantcommons(dict):
    def __init__(self, site):
        # Logically, we could use a PageGenerator here, but we only want a
        # couple of values and want to minimise load on the target.
        g = api.QueryGenerator(site = site, parameters=dict(
            generator='allfileusages', gafunique=True,
            prop='imageinfo|info', iiprop='', inprop='url'))
        for f in g:
            if f['imagerepository'] == 'wikimediacommons':
                self[f['title']] = f"[{f['fullurl']} {f['title']}]"
