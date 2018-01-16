import codecs
import json
import operator
import re
import string

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from data_cache.models import DNNKeyword


def get_keywords(html):

    # Note: 
    # 
    # \u2022 is bullet
    # \u2010 is hyphen
    # \u201c left double quotation mark
    # \u201d right double quotation mark
    # \u2018 left single quotation mark
    # \u2019 right single quotation mark
    # \u2013 en dash
    # \u2014 em dash
    # \u2019 apostrophel

    # \u25a1 white square
    # \u037e greek question mark
    # \u2011 non-breaking hyphen
    # \u2026 horiontal ellipsis
    # &#xbf inverted question mark
    # &#xbb '>>'
    # &#xb7 bullet point
    # &#xad soft hyphen
    # &#xad chapter character - '§''
    #
    # \xbf
    #

    replacements = { 
        '\n': '', '\r': '', '\t': '', '\xa0': '', '\u2022': '', '\u201c': '', '\u201d': '', '\u2018': '', '\u2019': '', '\u2014': '', '\u25a1': '', '\u037e': '', '\u2011': '', '\u2026': '', '&#xbf;': '', '&#xad': '',
        '&nbsp;': ' ', '|': ' ', '\u2010': ' ', '\u2013': ' ', '&#xbb': ' ', '&#xad': ' ', ':': ' ', '/': ' ', '.': ' ', '-': ' ', '(': ' ', ')': ' ',
        '\u2019': '\'',
        '&amp;': '&', 'amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
    }

    tmp = html
    for bad, good in replacements.items():
        tmp = tmp.replace(bad, good)

    for pos in range(0, len(tmp)):
        val = tmp[pos]
        if ord(val) > 128:
            tmp = tmp.replace(val, ' ')

    keywords = [ keyword for keyword in tmp.split(' ') if keyword ]
    keywords = [ keyword.strip(string.punctuation).lower() for keyword in keywords if keyword ]
    keywords = [ keyword for keyword in keywords if keyword ]

    keyword_objects = [ DNNKeyword(keyword=keyword) for keyword in keywords ]

    # for keyword in keywords:
    #     if len(keyword) >= 128:
    #         pdb.set_trace()


    # if "officeadministrationcorrespondenceoffice" in keywords:
    #     pdb.set_trace()


    return keywords, keyword_objects

class Command(BaseCommand):
    help = """
        This command loads all dnn keywords into a database, e.g.,
        python manage.py load_dnn_keywords LoosyHtml.txt"""

    def add_arguments(self, parser):
        """
        Build command-line args.
        """
        parser.add_argument('input_file', type=str, help='File to load keywords from')

    def handle(self, *args, **options):

        DNNKeyword.objects.all().delete()

        filename = options['input_file']

        keywords_all = []
        keywords_map = {}
        page_cnt = 0

        with open(filename, newline='', encoding="utf8") as input_file:

            content = input_file.read()
            content_json = json.loads(content)

            for page in content_json:

                page_content = page['result']
                page_content_json = json.loads(page_content)

                html = page_content_json['lossyHTML']

                keywords, keyword_objects = get_keywords(html)

                DNNKeyword.objects.bulk_create(keyword_objects)

                keywords_all.extend(keywords)

                for keyword in keywords:

                    if not keywords_map.get(keyword):
                        keywords_map[keyword] = 0

                    keywords_map[keyword] = keywords_map[keyword] + 1

                page_cnt = page_cnt + 1

        keywords_sorted = sorted(keywords_map.items(), key=operator.itemgetter(1))


        
