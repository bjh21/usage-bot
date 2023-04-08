import re
from subprocess import run, CalledProcessError, PIPE
from urllib.parse import unquote

# MediaWiki seems to use a casing table from Unicode 8.0.0 or 9.0.0.
# These are the characters that gained a Simple_Uppercase_Mapping
# between Unicode 9.0.0 and Unicode 15.0.0.  For compatibility with
# MediaWiki, we shouldn't up-case these characters at the start of
# filenames.
suppress_casing = {
    "\U00000282", "\U000010D0", "\U000010D1", "\U000010D2", "\U000010D3",
    "\U000010D4", "\U000010D5", "\U000010D6", "\U000010D7", "\U000010D8",
    "\U000010D9", "\U000010DA", "\U000010DB", "\U000010DC", "\U000010DD",
    "\U000010DE", "\U000010DF", "\U000010E0", "\U000010E1", "\U000010E2",
    "\U000010E3", "\U000010E4", "\U000010E5", "\U000010E6", "\U000010E7",
    "\U000010E8", "\U000010E9", "\U000010EA", "\U000010EB", "\U000010EC",
    "\U000010ED", "\U000010EE", "\U000010EF", "\U000010F0", "\U000010F1",
    "\U000010F2", "\U000010F3", "\U000010F4", "\U000010F5", "\U000010F6",
    "\U000010F7", "\U000010F8", "\U000010F9", "\U000010FA", "\U000010FD",
    "\U000010FE", "\U000010FF", "\U00001D8E", "\U00002C5F", "\U0000A794",
    "\U0000A7B9", "\U0000A7BB", "\U0000A7BD", "\U0000A7BF", "\U0000A7C1",
    "\U0000A7C3", "\U0000A7C8", "\U0000A7CA", "\U0000A7D1", "\U0000A7D7",
    "\U0000A7D9", "\U0000A7F6", "\U00010597", "\U00010598", "\U00010599",
    "\U0001059A", "\U0001059B", "\U0001059C", "\U0001059D", "\U0001059E",
    "\U0001059F", "\U000105A0", "\U000105A1", "\U000105A3", "\U000105A4",
    "\U000105A5", "\U000105A6", "\U000105A7", "\U000105A8", "\U000105A9",
    "\U000105AA", "\U000105AB", "\U000105AC", "\U000105AD", "\U000105AE",
    "\U000105AF", "\U000105B0", "\U000105B1", "\U000105B3", "\U000105B4",
    "\U000105B5", "\U000105B6", "\U000105B7", "\U000105B8", "\U000105B9",
    "\U000105BB", "\U000105BC", "\U00016E60", "\U00016E61", "\U00016E62",
    "\U00016E63", "\U00016E64", "\U00016E65", "\U00016E66", "\U00016E67",
    "\U00016E68", "\U00016E69", "\U00016E6A", "\U00016E6B", "\U00016E6C",
    "\U00016E6D", "\U00016E6E", "\U00016E6F", "\U00016E70", "\U00016E71",
    "\U00016E72", "\U00016E73", "\U00016E74", "\U00016E75", "\U00016E76",
    "\U00016E77", "\U00016E78", "\U00016E79", "\U00016E7A", "\U00016E7B",
    "\U00016E7C", "\U00016E7D", "\U00016E7E", "\U00016E7F"}

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
    if len(name) > 0 and name[0] not in suppress_casing:
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
