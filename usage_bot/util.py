import re
from subprocess import run, CalledProcessError, PIPE
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
            
def summary_revision():
    # Return a suitable suffix for an edit summary indicating which
    # code revision we're running.
    try:
        return " | " + run(['git', 'describe', '--always', '--dirty'],
                          check=True, encoding='utf-8', stdout=PIPE).stdout
    except CalledProcessError:
        return ""
