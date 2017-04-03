#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/4/17
# @Author  : Huaizheng ZHANG
# @Site    : zhanghuaizheng.com
# @File    : DL_trend_indexer.py
import os
import lucene
from datetime import datetime
import xml.etree.cElementTree as ET
import re

from java.nio.file import Paths;
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import FSDirectory

lucene.initVM()
class DLindexer(object):

    INDEX_FILED_TITLE = "Title"
    INDEX_FILED_BODY = "Body"
    INDEX_FILED_TAGS = "Tags"
    INDEX_FILED_DATE = "Date"


    def __init__(self, dir, data_file):
        self.dir = dir
        self.data_file = data_file
        index_dir = FSDirectory.open(Paths.get(self.dir))
        analyzer = StandardAnalyzer()
        writer_config = IndexWriterConfig(analyzer)
        writer_config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.writer = IndexWriter(index_dir, writer_config)

    def get_document(self, title, body, tags, date):
        doc = Document()
        doc.add(TextField(self.INDEX_FILED_TITLE, title, Field.Store.YES))
        doc.add(TextField(self.INDEX_FILED_BODY, body, Field.Store.YES))
        doc.add(TextField(self.INDEX_FILED_TAGS, tags, Field.Store.YES))
        doc.add(TextField(self.INDEX_FILED_DATE, date, Field.Store.YES))
        return doc

    def index_DLs(self):
        start_time = datetime.now()
        print "Start to index " + self.data_file + " @ " + str(start_time)
        count = 0
        for event, elem in ET.iterparse(self.data_file):
            print datetime.now()
            if event == 'end':
                if elem.get('Title'):
                    title = elem.get('Title')
                else:
                    title = ''
                if elem.get('Body'):
                    body = elem.get('Body')
                    body = re.sub(r'</?\w+[^>]*>', '', body)
                else:
                    body = ''

                if elem.get('Tags'):
                    tags = elem.get('Tags')
                else:
                    tags = ''

                if elem.get('CreationDate'):
                    date = elem.get('CreationDate')[0:7]

                if date[5:7] == self.dir[-2:] and date[0:4] == '2016':
                    print self.dir
                    doc = self.get_document(title.encode("utf-8"), body.encode("utf-8"), tags.encode("utf-8"), date.encode("utf-8"))
                    self.writer.addDocument(doc)
                    print count
                    count = count + 1

            elem.clear()
        self.writer.close()
        print "Indexing " + self.data_file + " complete @ " + str(datetime.now())
        print "Indexing time is " + str(datetime.now() - start_time)

if __name__ == '__main__':
    lucene.initVM()
    if len(os.listdir('../DLindexer')) > 0:
        print 'You have finished indexing'
    else:
        for i in ['01','02','03','04','05','06','07','08','09','10','11','12']:
            index = DLindexer('../DLindexer/' + i, '../Posts.xml')
            index.index_DLs()
