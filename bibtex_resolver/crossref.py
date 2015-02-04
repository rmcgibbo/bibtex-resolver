import json
import requests
import functools
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter

from .bibtex import customizations

PARSER = BibTexParser()
PARSER.customization = customizations
WRITER = BibTexWriter()


@functools.lru_cache(maxsize=1024)
def retreive_doi(search, rows=3):
    r = requests.get('http://search.crossref.org/dois',
        params={'q': search, 'rows': int(rows)})
    j = r.json()
    return j


@functools.lru_cache(maxsize=32)
def retreive_record(doi):
    r = requests.get('http://api.crossref.org/works/' + doi +  '/transform/application/x-bibtex')
    return r.content.decode('utf-8')


def retreive_bibtex(search):
    lines = []
    for item in retreive_doi(search):
        lines.append(retreive_record(item['doi']))
    db = PARSER.parse('\n'.join(lines))
    return WRITER.write(db)
