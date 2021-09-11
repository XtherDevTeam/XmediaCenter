#!/bin/python3
import os
import zipfile
import sys
import json

from lxml import etree
from bs4 import BeautifulStoneSoup

RECOVER_PARSER = etree.XMLParser(recover=True, no_network=True)
NAMESPACES = {
    'dc': 'http://purl.org/dc/elements/1.1/',
}


class EpubObject(object):
    u"""
    需要主动调用open方法才能获得相应的属性
    """
    _FILE = '%s'

    def __init__(self, book_id=None):
        if book_id:
            self.open(book_id)

    def fromstring(self, raw, parser=RECOVER_PARSER):
        return etree.fromstring(raw, parser=parser)

    def read_doc_props(self, raw):
        u"""

        :param raw: raw string of xml
        :return:
        """
        root = self.fromstring(raw)
        try:
            self.title = root.xpath('//dc:title', namespaces={'dc': NAMESPACES['dc']})[0].text
        except:
            self.title = ''
        try:
            self.author = root.xpath('//dc:creator', namespaces={'dc': NAMESPACES['dc']})[0].text
        except:
            self.author = ''

    def open(self, book_id=None):
        if book_id:
            self.book_id = book_id
        if not self.book_id:
            raise Exception('Book id not set')

        self.f = zipfile.ZipFile(self._FILE % self.book_id, 'r')
        soup = BeautifulStoneSoup(self.f.read('META-INF/container.xml'))

        oebps = soup.findAll('rootfile')[0]['full-path']
        folder = oebps.rfind(os.sep)
        self.oebps_folder = '' if folder == -1 else oebps[:folder+1]   # 找到oebps的文件夹名称

        oebps_content = self.f.read(oebps)
        self.read_doc_props(oebps_content)

        opf_bs = BeautifulStoneSoup(oebps_content)
        ncx = opf_bs.findAll('item', {'id': 'ncx'})[0]
        ncx = self.oebps_folder + ncx['href']     # 找到ncx的完整路径

        ncx_bs = BeautifulStoneSoup(self.f.read(ncx))
        try:
            self.chapters = [(nav.navlabel.text, nav.content['src']) for
                            nav in ncx_bs.findAll('navmap')[0].findAll('navpoint')]
        except:
            self.chapters = []

def parse(filename:str):
    epub = EpubObject()
    epub.open(filename)
    print(epub.title)
    print(epub.author)
    result = { 'title':epub.title, 'author':epub.author, 'chapters':epub.chapters, 'files':{} }
    for i in epub.f.filelist:
        result['files'][i.filename] = epub.f.read(i.filename)
    return result
