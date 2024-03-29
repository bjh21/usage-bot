"""
This family file was auto-generated by generate_family_file.py script.

Configuration parameters:
  url = https://wikimedia.org.au/wiki/
  name = wmau

Please do not commit this to the Git repository!
"""
from pywikibot import family


class Family(family.Family):  # noqa: D101

    name = 'wmau'
    langs = {
        'en': 'wikimedia.org.au',
    }

    def scriptpath(self, code):
        return {
            'en': '/w',
        }[code]

    def protocol(self, code):
        return {
            'en': 'https',
        }[code]
