import re
from subprocess import run, CalledProcessError, PIPE
from urllib.parse import unquote

def canonicalise_name(name):
    # Produce the canonical form of a name for use in galleries and as
    # a key.  Broadly equivalent to part of the splitTitleString
    # function in MediaWiki.
    name = unquote(name)
    # Strip bidi overrides.
    name = re.sub(r"[\u200E\u200F\u202A-\u202E]+", "", name)
    # Normalise spaces.
    name = re.sub(r"[ _\xA0\u1680\u180E\u2000-\u200A\u2028\u2029\u202F"
                  r"\u205F\u3000]+", " ", name)
    name = name.strip(" ")
    # Galleries don't need the namespace prefix, so we strip it off.
    name = re.sub(r"^File: *", "", name, flags=re.IGNORECASE)
    if len(name) > 0:
        # This is not the proper way to capitalise a string, since it
        # messes up characters with a titlecase form.  It seems to
        # match what MediaWiki does, though.
        name = name[0].upper() + name[1:]
    return name
            
def summary_revision():
    # Return a suitable suffix for an edit summary indicating which
    # code revision we're running.
    try:
        return " | " + run(['git', 'describe', '--always', '--dirty'],
                          check=True, encoding='utf-8', stdout=PIPE).stdout
    except CalledProcessError:
        return ""
