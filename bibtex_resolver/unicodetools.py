import unicodedata
import itertools
from bibtexparser.latexenc import string_to_latex
from bibtexparser.customization import (unicode_to_latex,
    unicode_to_crappy_latex1, unicode_to_crappy_latex2)

latex_to_unicode = dict((b,a) for a, b in itertools.chain(
    unicode_to_latex, unicode_to_crappy_latex1, unicode_to_crappy_latex2))


def normalize_latex(str):
    str = str.replace("{a}", "a")
    str = str.replace("{e}", "e")
    str = str.replace("{i}", "i")
    str = str.replace("{o}", "o")
    str = str.replace("{u}", "u")
    str = str.replace("{n}", "n")

    u = latex2str(str)
    u = unicodedata.normalize('NFC', u)
    out = string_to_latex(u)
    return out


def latex2str(str, charmap=None):
    if '{' not in str:
        return str

    chars = []
    i = 0
    while i < len(str):
        char = str[i]
        if char == '{':
            r = str.find('}', i)+1
            while str.count('{', i, r) > str.count('}', i, r):
                r = str.find('}', r)+1

            u = latex_to_unicode.get(str[i:r])
            if u is None:
                u = latex_to_unicode.get(str[i+1:r-1])
            char = charmap(u) if charmap is not None else u
            if char is None:
                print(str[i:r], u, '\\^{\\i}' in latex_to_unicode)
                raise ValueError()
            i = r
        else:
            i += 1
        chars.append(char)
    return ''.join(chars)
