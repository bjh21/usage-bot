import pywikibot.comms.http as http
import re
from urllib.parse import urlencode, urljoin

class from_taginfo(dict):
    def __init__(self, baseurl="https://taginfo.openstreetmap.org"):
        self.baseurl = baseurl
        self.editsummary = self.get_editsummary()
        self.from_key("wikimedia_commons")
        # self.from_key("image", allowurls=True)
    def from_key(self, key, allowurls=False):
        r = http.fetch(urljoin(self.baseurl, "api/4/key/values"),
                       params={'key': key})
        r.raise_for_status()
        j = r.json()
        for v in j["data"]:
            title = v["value"]
            if allowurls:
                # image=* might be either a Commons page title or a URL
                m = re.match("^https?://commons.wikimedia.org/wiki/"
                             "(File:[^#?]*)",
                             title, re.IGNORECASE)
                if m:
                    title = m[1]
            if re.match("^File:", title, re.IGNORECASE):
                params = urlencode(dict(key=key, value=v['value']))
                tiurl = urljoin(self.baseurl, "tags/?" + params)
                if title in self:
                    self[title] += "<br/>"
                else:
                    self[title] = ""
                self[title] += (f"[{tiurl} {key}={v['value']}]")
    def get_editsummary(self):
        r = http.fetch(urljoin(self.baseurl, "api/4/site/info"))
        r.raise_for_status()
        site_info = r.json()
        r = http.fetch(urljoin(self.baseurl, "api/4/site/sources"))
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

