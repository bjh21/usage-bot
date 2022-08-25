import re
from urllib.parse import unquote

def canonicalise_name(name):
    # Produce the canonical form of a name for use in galleries and as
    # a key.  Galleries don't need the namespace prefix, so we strip
    # it off.
    name = unquote(name).replace("_", " ")
    name = re.sub(r"^File:\s*", "", name, flags=re.IGNORECASE)
    # XXX Should upcase the first character, but I need to check
    # precisely how MediaWiki does that.
    return name
            
