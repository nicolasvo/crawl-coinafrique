# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
from lxml import etree
import json
import requests
import unidecode

import os
import ssl

if not (os.environ.get('PYTHONHTTPSVERIFY', '') or not getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


def process_string(string):
    return unidecode.unidecode(string.encode("latin-1").decode("utf-8")).lower().replace('&', 'et')


def get_tree(url):

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url, headers=hdr)
    response = urlopen(req)
    htmlparser = etree.HTMLParser()
    tree = etree.parse(response, htmlparser)
    return tree

list_country = []

for country in get_tree("http://web.coinafrique.com/").xpath('//ul/a'):
    list_country.append(country.xpath('./@href')[0])

tree_bj = get_tree(list_country[0])

for li in tree_bj.xpath('//ul/li'):
    print(li.xpath('./div[@class="collection-item collapsible-body"]'))

dict_category = {}
for li in tree_bj.xpath('//ul[@data-collapsible="accordion"]/li'):
    if len(li.xpath('.//h1/text()'))>0:
        list_id = []
        list_category = []
        for a in li.xpath('./div[@class="collection-item collapsible-body"]/a'):
            list_id.append(process_string(a.xpath('./@data-category-id')[0]))
            list_category.append(process_string(a.xpath('./@data-category-name')[0]))
        dict_category.update({process_string(li.xpath('.//h1/text()')[0]):
                                  dict(zip(list_id[:-1], list_category[:-1]))})

print(dict_category)