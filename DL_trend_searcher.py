#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2/4/17
# @Author  : Huaizheng ZHANG
# @Site    : zhanghuaizheng.com
# @File    : DL_trend_searcher.py

import lucene
import easygui
import numpy as np
import matplotlib.pyplot as plt
from java.nio.file import Paths
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser, MultiFieldQueryParser
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader, IndexReader, Term
from org.apache.lucene.search import IndexSearcher, Query, ScoreDoc, TopScoreDocCollector
from org.apache.lucene.store import FSDirectory


class DLsearcher(object):
    def __init__(self, dir):
        self.dir = dir
        self.lReader = DirectoryReader.open(FSDirectory.open(Paths.get(self.dir)))
        self.lSearcher = IndexSearcher(self.lReader)

    # def get_collection_size(self):
    #     return self.lReader.numDocs()


    def doc_search(self, keywords):
        term1 = self.lReader.totalTermFreq(Term('Title', keywords))
        term2 = self.lReader.totalTermFreq(Term('Body', keywords))
        term3 = self.lReader.totalTermFreq(Term('Tags', keywords))
        term = term1 + term2 + term3

        self.term = term
        # print term
        return term


    def close(self):
        try:
            if (self.lReader != None):
                self.lReader.close()
        except RuntimeError:
            print "Close reader fail"


if __name__ == '__main__':
    lucene.initVM()
    labels = easygui.multchoicebox('Please select one or more DL framwork', '6223 DL framwork trend', ['tensorflow','caffe','mxnet','torch','theano'])
    if len(labels) == 0:
        print 'Please choose one at least'
    else:

        x_total = []
        y_total = []
        start_month = easygui.integerbox(msg='Please choose the first monthe ', title='6223 DL framwork trend', default=1)
        end_month = easygui.integerbox(msg='Please choose the last monthe ', title='6223 DL framwork trend', default=12)
        if int(end_month) -  int(start_month) < 1 or int(start_month) > 12 or int(end_month) > 12:
            print "Please import correct month"
        else:
            for i in range(int(start_month), int(end_month)+1):
                if len(str(i)) == 1:
                    month = '0' + str(i)
                else:
                    month = str(i)
                x_total.append(month)
                searcher = DLsearcher('../DLindexer/' + month)
                for j in labels:
                    month_total = searcher.doc_search(j)
                    y_total.append([j, int(month_total), month])
    y_total = np.array(y_total)
    for i in labels:
        y = []
        for j in range(len(y_total)) :
            # print y_total[j,0]
            if y_total[j,0] == i:
                y.append(y_total[j,1])
        # print y
        plt.plot(x_total, y, label=i)
    plt.legend()
    plt.show()
