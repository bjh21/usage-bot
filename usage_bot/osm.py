import pywikibot.comms.http as http
import re
from urllib.parse import urlencode

class from_taginfo(dict):
    def __init__(files):
        files.editsummary = taginfo_editsummary()
        r = http.fetch("https://taginfo.openstreetmap.org/api/4/key/values"
                       "?key=wikimedia_commons")
        r.raise_for_status()
        j = r.json()
        for v in j["data"]:
            if re.match("^File:", v["value"], re.IGNORECASE):
                params = urlencode(dict(key="wikimedia_commons",
                                        value=v["value"]))
                tiurl = "https://taginfo.openstreetmap.org/tags/?" + params
                files[v['value']] = (
                    f"{v['value']}<br/>[{tiurl} ~{v['count']} use(s)]")

def taginfo_editsummary():
    r = http.fetch("https://taginfo.openstreetmap.org/api/4/site/info")
    r.raise_for_status()
    site_info = r.json()
    r = http.fetch("https://taginfo.openstreetmap.org/api/4/site/sources")
    r.raise_for_status()
    site_sources = r.json()
    dbsrc = [src for src in site_sources if src['id'] == 'db'][0]
    return (f"; data via {site_info['name']} [{site_info['url']}]; "
            f"correct as of {dbsrc['data_until']} UTC")

oplq = """
[out:json];
// gather results
(
  node["wikimedia_commons"~"(^|;)File:",i];
  way["wikimedia_commons"~"(^|;)^File:",i];
  relation["wikimedia_commons"~"(^|;)File:",i];
);
// print results
out tags qt;
"""

def from_overpass():
    r = http.fetch("https://overpass-api.de/api/interpreter",
                   params={'data': oplq})
    r.raise_for_status()
    j = r.json()
    files = {}

    for e in j["elements"]:
        wc = e.get("tags", {}).get("wikimedia_commons")
        if wc != None:
            osm_type = e["type"]
            osm_id = e["id"]
            files[wc] = (f"[https://www.openstreetmap.org/{osm_type}/{osm_id} "
                         f"{osm_type} {osm_id}]")
    return files

