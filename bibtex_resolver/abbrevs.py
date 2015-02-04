import json
import os
import difflib
import sys
import functools


class JournalAbbreviator(object):
    def __init__(self):
        with open(os.path.join(os.path.dirname(__file__), 'abbreviations.json')) as f:
            self.table = json.load(f)
        self.abbrevs = [r[0] for r in self.table]
        self.fulltitles = [r[1] for r in self.table]

        self.all = self.abbrevs + self.fulltitles

    @functools.lru_cache(maxsize=1024)
    def abbreviate(self, journal):
        journal2 = journal.replace('{', '').replace('}', '')
        if journal2 not in self.abbrevs:
            matches = difflib.get_close_matches(journal2, self.all, n=1)
            if len(matches) == 0:
                return None
            closest = matches[0]
            if closest in self.fulltitles:
                i = self.fulltitles.index(closest)
                closest = self.abbrevs[i]

            return closest
        return journal
