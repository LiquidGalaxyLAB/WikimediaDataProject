import hashlib
import logging
import os
import re
from xml.dom import minidom
import xml.etree.cElementTree as ET
import six
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

uri_scheme = 'https'
api_uri = 'wikipedia.org/w/api.php'

_uri = 'wikipedia.org/wiki/'
file_name = "olympic_games_tmp_file.xml"

# common sub sections to exclude from output
UNWANTED_SECTIONS = (
    'External links and resources',
    'External links',
    'Navigation menu',
    'See also',
    'References',
    'Further reading',
    'Contents',
    'Official',
    'Other',
    'Notes',
)

#https://en.wikipedia.org/w/api.php?action=query&format=xml&titles=albesa&prop=revisions&rvprop=content

class WikiApi(object):

    def __init__(self, options=None):
        if options is None:
            options = {}

        self.options = options
        if 'locale' not in options:
            self.options['locale'] = 'en'
        self.caching_enabled = True if options.get('cache') is True else False
        self.cache_dir = options.get('cache_dir') or '/tmp/wikiapicache'

    def getIndex_substring(self,string,resp):
        index = 0

        if string in resp:
           c = string[0]

           for ch in resp:
               if ch == c:
                  if resp[index:index+len(string)] == string:
                     return index

               index += 1

        return -1

    def replace(self, results):
        results = results.decode()

        results = results.replace("&lt;","<")
        results = results.replace("&gt;",">")
        results = results.replace("&amp;","&",)
        results = results.replace("&quot;","\"")

        return results

    def find(self, terms):

        search_params = {
        'action': 'parse',
        'format': 'xml',
        'page': terms
        }

        url = "{scheme}://{locale_sub}.{hostname_path}".format(
        scheme = uri_scheme,
        locale_sub = self.options['locale'],
        hostname_path = api_uri
        )
        print (url)
        resp = self.get(url, search_params)
        logger.debug('find "%s" response: %s', terms, resp)

        return resp

    def dbpedia(self, city_name):

        uri_scheme = 'http'
        api_uri = 'dbpedia.org/data/'+city_name+'.xml'
        search_params = {}

        url = "{scheme}://{hostname_path}".format(
        scheme = uri_scheme,
        hostname_path = api_uri
        )
        print ("dbpedia")
        resp = self.get(url, search_params).decode("utf-8") #bytes to string

        return resp

    def scraping_infobox(self, result_xml):
        wiki = WikiApi()
        hash_data = {}
        index_i = wiki.getIndex_substring(("infobox").encode('utf-8'),result_xml)
        index_f = wiki.getIndex_substring(("vertical-navbox").encode('utf-8'),result_xml)
        result_xml = wiki.replace(result_xml[index_i:index_f])
        with open(file_name,'w') as f:
            f.write(result_xml)
        file = open(file_name, 'r')
        key = ""
        value = ""
        for line in file.readlines():
            if "<th" in line:
                parts = line.split('\">')
                key = parts[len(parts)-1].split("</")[0]
            if "<td>" in line:
                value = line.split(">")[1].split("<")[0]
                if "<td><a" in line:
                    parts = line.split('\">')
                    value = parts[len(parts)-1].split("</")[0]
                if "<" not in value:
                    hash_data[key] = value
            elif "<td" in line:
                parts = line.split('\">')
                value = parts[len(parts)-(len(parts)//2)].split("</")[0]
                if "<" not in value:
                    hash_data[key] = value

        return hash_data

    def get_atributes_dbpedia_city(self, resp, attr):
        wiki = WikiApi()
        if attr == "latitude":
            lat_index_i = wiki.getIndex_substring("<geo:lat",resp)
            lat_index_f = wiki.getIndex_substring("</geo:lat>",resp)
            latitude = resp[lat_index_i:lat_index_f].split(">")[1]
            return latitude
        elif attr == "longitude":
            long_index_i = wiki.getIndex_substring("<geo:long",resp)
            long_index_f = wiki.getIndex_substring("</geo:long>",resp)
            longitude = resp[long_index_i:long_index_f].split(">")[1]
            return longitude
        elif attr == "population":
            popu_index_i = wiki.getIndex_substring("<dbo:populationTotal",resp)
            popu_index_f = wiki.getIndex_substring("</dbo:populationTotal>",resp)
            population = resp[popu_index_i:popu_index_f].split(">")[1]
            return population
        elif attr == "area":
            area_index_i = wiki.getIndex_substring("<dbo:areaTotal",resp)
            area_index_f = wiki.getIndex_substring("</dbo:areaTotal>",resp)
            area = resp[area_index_i:area_index_f].split(">")[1]
            print (float(area))
            return float(area)/1000000.0
        elif attr == "image":
            image_index_i = wiki.getIndex_substring("<foaf:depiction",resp)
            image_index_f = wiki.getIndex_substring("<foaf:isPrimary",resp)
            print (image_index_i," ",image_index_f)
            image = resp[image_index_i:image_index_f]
            return image

    def get(self, url, params={}):
        if self.caching_enabled:
            cached_item_path = self._get_cache_item_path(
                url=url,
                params=params
            )

            cached_resp = self._get_cached_response(cached_item_path)

            if cached_resp:
                return cached_resp

        resp = requests.get(url, params=params)
        resp_content = resp.content

        if self.caching_enabled:
            self._cache_response(cached_item_path, resp_content)

        return resp_content
