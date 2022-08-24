"""
This family file was auto-generated by generate_family_file.py script.

Configuration parameters:
  url = https://docs.wikimedia.cz/wiki/
  name = wmczdocs

Please do not commit this to the Git repository!
"""
from pywikibot import family


class Family(family.Family):  # noqa: D101

    name = 'wmczdocs'
    langs = {
        'cs': 'docs.wikimedia.cz',
    }

    def scriptpath(self, code):
        return {
            'cs': '/mw',
        }[code]

    def protocol(self, code):
        return {
            'cs': 'https',
        }[code]
