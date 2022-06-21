import pywikibot.data.api as api

def from_instantcommons(site):
    # Logically, we could use a PageGenerator here, but we only want a
    # couple of values and want to minimise load on the target.
    g = api.QueryGenerator(site = site, parameters=dict(
        generator='allfileusages', gafunique=True,
        prop='imageinfo|info', iiprop='', inprop='url'))
    files = {}
    for f in g:
        if f['imagerepository'] == 'wikimediacommons':
            files[f['title']] = (
                f"[{f['fullurl']} {f['title']}]")
    return files
