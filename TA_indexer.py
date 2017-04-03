#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/4/17
# @Author  : Huaizheng ZHANG
# @Site    : zhanghuaizheng.com
# @File    : TA_indexer.py


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
class TAindexer(object):

    INDEX_FILED_TITLE = "Title"
    INDEX_FILED_POSTID = "PostTypeId"
    INDEX_FILED_AC = "AnswerCount"


    def __init__(self, dir, data_file):
        self.dir = dir
        self.data_file = data_file
        index_dir = FSDirectory.open(Paths.get(self.dir))
        analyzer = StandardAnalyzer()
        writer_config = IndexWriterConfig(analyzer)
        writer_config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        self.writer = IndexWriter(index_dir, writer_config)

    def get_document(self, title, post_id, ac):
        doc = Document()
        doc.add(TextField(self.INDEX_FILED_TITLE, title, Field.Store.YES))
        doc.add(TextField(self.INDEX_FILED_POSTID, post_id, Field.Store.YES))
        doc.add(TextField(self.INDEX_FILED_AC, ac, Field.Store.YES))
        return doc

    def index_TAs(self):
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
                if elem.get('PostTypeId'):
                    post_id = elem.get('PostTypeId')
                else:
                    post_id = ''

                if elem.get('AnswerCount'):
                    answer_count = elem.get('AnswerCount')
                else:
                    answer_count = ''
                print post_id
                print answer_count
                if str(post_id) == '1':
                    print self.dir
                    doc = self.get_document(title.encode("utf-8"), post_id.encode("utf-8"), answer_count.encode("utf-8"))
                    self.writer.addDocument(doc)
                    print count
                    count = count + 1

            elem.clear()
        self.writer.close()
        print "Indexing " + self.data_file + " complete @ " + str(datetime.now())
        print "Indexing time is " + str(datetime.now() - start_time)

if __name__ == '__main__':
    lucene.initVM()
    if len(os.listdir('../TAindexer')) > 0:
        print 'You have finished indexing'
    else:
        index = TAindexer('../TAindexer', '../Posts.xml')
        index.index_TAs()