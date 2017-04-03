#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 30/3/17
# @Author  : Huaizheng ZHANG
# @Site    : zhanghuaizheng.com
# @File    : QA_indexer.py

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
class QAindexer(object):

    INDEX_FILED_TITLE = "Title"
    INDEX_FILED_BODY = "Body"


    def __init__(self, dir, data_file):
        self.dir = dir
        self.data_file = data_file
        index_dir = FSDirectory.open(Paths.get(self.dir))
        analyzer = StandardAnalyzer()
        writer_config = IndexWriterConfig(analyzer)
        writer_config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.writer = IndexWriter(index_dir, writer_config)

    def get_document(self, title, body):
        doc = Document()
        doc.add(TextField(self.INDEX_FILED_TITLE, title, Field.Store.YES))
        doc.add(TextField(self.INDEX_FILED_BODY, body, Field.Store.YES))
        return doc

    def index_QAs(self):
        print "Start to index " + self.data_file + " @ " + str(datetime.now())
        count = 0
        for event, elem in ET.iterparse(self.data_file):
            if event == 'end':
                if elem.get('Title'):
                    title = elem.get('Title')
                    print title
                else:
                    title = ''
                if elem.get('Body'):
                    body = elem.get('Body')

                    body = re.sub(r'</?\w+[^>]*>', '', body)
                    print body
                else:
                    body = ''

                doc = self.get_document(title.encode("utf-8"), body.encode("utf-8"))

                self.writer.addDocument(doc)
                print count
                count = count + 1

            elem.clear()
        self.writer.close()
        print "Indexing " + self.data_file + " complete @ " + str(datetime.now())


if __name__ == '__main__':
    lucene.initVM()
    if len(os.listdir('../QAindexer')) > 0:
        print 'You have finished indexing'
    else:
        index = QAindexer('../QAindexer', '../Posts.xml')
        index.index_QAs()

