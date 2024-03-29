import pywikibot.data.api as api
import pywikibot.bot as bot
import pywikibot

class NoRepoError(Exception):
    pass

class from_instantcommons(dict):
    def __init__(self, site, iwprefix=None):
        # Find out how this wiki refers to Commons.
        r = api.Request(site, parameters=dict(action='query',
                                              meta='filerepoinfo',
                                              friprop='name|server'))
        commons_ids = [repo['name'] for repo in r.submit()['query']['repos']
                       if repo.get('server') == '//commons.wikimedia.org']
        if len(commons_ids) == 0:
            raise(NoRepoError("No repository found with "
                              "server=//commons.wikimedia.org"))
        bot.log(f"Commons repo id(s): {commons_ids}")
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
            if f['imagerepository'] in commons_ids:
                # Other wikis might have their own namespace prefix in
                # place of "File:", but those won't work on Commons.
                # Assume that everything up to the first colon is the
                # namespace prefix.
                commons_title = f['title'].split(':', 1)[1]
                # We could stick "File:" on the front for Commons, but
                # <gallery> works perfectly well without it and that
                # saves 5 KB per gallery.  At least, until someone
                # uploads a file to Commons whose name begins "File:",
                # but a search suggests that this has only ever
                # happened once.
                if iwprefix == None:
                    self[commons_title] = f"[{f['fullurl']} {f['title']}]"
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
                    self[commons_title] = f"[[{iwprefix}:{f['title']}]]"
