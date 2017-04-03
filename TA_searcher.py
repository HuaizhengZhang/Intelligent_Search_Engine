#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 3/4/17
# @Author  : Huaizheng ZHANG
# @Site    : zhanghuaizheng.com
# @File    : TA_searcher.py

import lucene
import easygui
import numpy as np
from java.nio.file import Paths
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader, IndexReader
from org.apache.lucene.search import IndexSearcher, Query, ScoreDoc, TopScoreDocCollector
from org.apache.lucene.store import FSDirectory


class QAsearcher(object):
    def __init__(self, dir):
        self.dir = dir
        self.lReader = DirectoryReader.open(FSDirectory.open(Paths.get(self.dir)))
        self.lSearcher = IndexSearcher(self.lReader)

    # def get_collection_size(self):
    #     return self.lReader.numDocs()


    def doc_search(self, keywords):

            analyzer = StandardAnalyzer()
            parser = QueryParser('Title', analyzer)
            query = parser.parse(keywords)

            try:
                collector = TopScoreDocCollector.create(3000)
                self.lSearcher.search(query, collector)
                hits = collector.topDocs().scoreDocs

            except RuntimeError:
                print "Score docoment run fail"
            self.hits = hits
            return hits

    def print_result(self):
        temp = []
        for i in self.hits:
            # print "\nResult " + str(j) + "\tDocID: " + str(i.doc) + "\t Score: " + str(i.score)
            try:
                temp.append([self.lReader.document(i.doc).get("Title"), int(self.lReader.document(i.doc).get("AnswerCount"))])
            except RuntimeError:
                print "Search fail"
        sort = np.array(temp, dtype=object)

        sort1000 = sort[np.argsort(-sort[:, 1])]

        show = 'The top 10 question is \n'
        for i in range(0,10):
            show = show + '\n' + 'The ' + str(i+1) + ' question is: ' + str(sort1000[i,0]) +'\nThe number of answer is ' + str(sort1000[i,1]) + '\n'

        text = '\n'.join(show)
        easygui.textbox(title='6223 Top Question', text=show)




    def close(self):
        try:
            if (self.lReader != None):
                self.lReader.close()
        except RuntimeError:
            print "Close reader fail"

if __name__ == '__main__':
    lucene.initVM()
    search_keywords = easygui.enterbox(msg='Please input your question: ', title='6223 Top Question', strip=True)
    searcher = QAsearcher('../TAindexer')
    hits = searcher.doc_search(search_keywords)
    searcher.print_result()
