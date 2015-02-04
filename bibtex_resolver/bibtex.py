import re
from unidecode import unidecode
from bibtexparser.customization import author, editor

from .unicodetools import normalize_latex, latex2str
from .stopwords import stopwords
from .abbrevs import JournalAbbreviator

abbreviate = JournalAbbreviator().abbreviate


def id_from_authoryear(record):
    try:
        first_author = author({'author': record['author']})['author'][0]
    except KeyError:
        first_author = editor({'editor': record['editor']})['editor'][0]['name']

    surname = re.split('\s|,', first_author)[0]
    surname = latex2str(surname, lambda u: unidecode(u) if u is not None else '').lower()
    surname = surname.replace('-', '')

    # extract the first words from the title
    title = re.split('\s', record['title'])
    first = next(e.lower() for e in title if e.lower() not in stopwords)
    first = latex2str(first, lambda u: unidecode(u) if u is not None else '').lower()
    if '-' in first:
        first = first.split('-')[0]

    new_id = '%s%s%s' % (surname, record['year'], first)
    record['id'] = new_id
    return record


def customizations(record):
    if 'author' in record:
        record['author'] = normalize_latex(record['author'])
    if 'editor' in record:
        record['editor'] = normalize_latex(record['editor'])
    record = id_from_authoryear(record)
    if 'journal' in record:
        record['journal'] = abbreviate(record['journal'])
    return record
