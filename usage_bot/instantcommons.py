import pywikibot.data.api as api
import pywikibot

class from_instantcommons(dict):
    def __init__(self, site, iwprefix=None):
        # Logically, we could use a PageGenerator here, but we only want a
        # couple of values and want to minimise load on the target.
        parameters = dict(
            generator='allfileusages', gafunique=True,
            prop='imageinfo', iiprop='')
        if iwprefix == None:
            parameters['prop'] += '|info'
            parameters['inprop'] = 'url'
        g = api.QueryGenerator(site=site, parameters=parameters)
        for f in g:
            if f['imagerepository'] == 'wikimediacommons':
                if iwprefix == None:
                    self[f['title']] = f"[{f['fullurl']} {f['title']}]"
                else:
                    # pywikibot.Link theoretically supports generating
                    # interwiki links between arbitrary Sites, but in
                    # practice it's not reliable.  For instance for a
                    # link from Commons to Wikitech it generates
                    # [[wikitech:en:File:Example.png]] which actually
                    # ends us up at English Wikipedia.  So we just
                    # allow the caller to specify an interwiki prefix,
                    # which isn't very much additional hassle and is
                    # much simpler than working it out properly from
                    # the interwiki map.
                    self[f['title']] = f"[[{iwprefix}:{f['title']}]]"
