#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 31/3/17
# @Author  : Huaizheng ZHANG
# @Site    : zhanghuaizheng.com
# @File    : QA_searcher.py

import sys
import lucene
import easygui

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


    def doc_search(self, field, keywords, numHits):
        if field != 'All':
            analyzer = StandardAnalyzer()
            parser = QueryParser(field, analyzer)
            query = parser.parse(keywords)

            # self.lReader.getDocCount("title");

            try:
                collector = TopScoreDocCollector.create(numHits)
                self.lSearcher.search(query, collector)
                hits = collector.topDocs().scoreDocs

            except RuntimeError:
                print "Score docoment run fail"
            self.hits = hits
            self.field = field
            return hits
        else:
            analyzer = WhitespaceAnalyzer()
            parser = MultiFieldQueryParser(['Title', 'Body'], analyzer)
            query = MultiFieldQueryParser.parse(parser, keywords)


            # self.lReader.getDocCount("title");

            try:
                collector = TopScoreDocCollector.create(numHits)
                self.lSearcher.search(query, collector)
                hits = collector.topDocs().scoreDocs

            except RuntimeError:
                print "Score docoment run fail"
            self.hits = hits
            self.field = field
            return hits


            self.hits = hits
            self.field = field
            return hits

    def print_result(self):
        j = 1

        for i in self.hits:
            print "\nResult " + str(j) + "\tDocID: " + str(i.doc) + "\t Score: " + str(i.score)
            try:
                if self.field == 'All':
                    print "Tile: " + self.lReader.document(i.doc).get("Title")
                    print "Body: " + self.lReader.document(i.doc).get("Body")
                if self.field == 'Title':
                    print "Tile: " + self.lReader.document(i.doc).get("Title")
                if self.field == 'Body':
                    print "Body: " + self.lReader.document(i.doc).get("Body")

            except RuntimeError:
                print "Search fail"
            j = j + 1
            print j

    def close(self):
        try:
            if (self.lReader != None):
                self.lReader.close()
        except RuntimeError:
            print "Close reader fail"

if __name__ == '__main__':
    lucene.initVM()
    search_keywords = easygui.enterbox(msg='Please input your question: ', title='6223 search engine', strip=True)
    choice = easygui.choicebox('Which field do you want to choose: ', '6223 search engine', ['All','Title','Body'])
    num = easygui.integerbox(msg='How many results do you want to show: ', title='6223 search engine', default=20)
    searcher = QAsearcher('../QAindexer')
    hits = searcher.doc_search(choice, search_keywords, int(num))
    print "I want to search: " + search_keywords
    searcher.print_result()