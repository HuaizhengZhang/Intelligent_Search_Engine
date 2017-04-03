System:
Ubuntu 14.04
Python 2.7
JDK 1.8

The third lib you need:

ant: http://www-us.apache.org/dist//ant/source/apache-ant-1.10.1-src.zip (sudo apt-get install ant)
pylucene: http://www-eu.apache.org/dist/lucene/pylucene/pylucene-6.4.1-src.tar.gz
jcc: svn co http://svn.apache.org/repos/asf/lucene/pylucene/trunk/jcc jcc

xml.etree.cElementTree: https://docs.python.org/2/library/xml.etree.elementtree.html
easygui: http://easygui.sourceforge.net/ (sudo pip install easygui)
matplotlib: http://matplotlib.org/ (sudo pip install matplotlib)
numpy: http://www.numpy.org/ (sudo pip install numpy)


How to run:

Open terminal and creat a dir, then copy this dir and Post.xml document to your dir

1. About search engine:
    a. index your Post.xml document by using 'python QA_indexer.py'
    b. run 'python QA_searcher.py' and choose your choice according to GUI noticing
    c. you can watch output here

2. Deep Learning trend app
    a. index your Post.xml document by using 'python DL_trend_indexer.py'
    b. run 'python DL_trend_searcher.py' and choose your choice according to GUI noticing
    c. you can watch output here

3. The top 10 question
    a. index your Post.xml document by using 'python TA_indexer.py'
    b. run 'python TA_searcher.py' and choose your choice according to GUI noticing
    c. you can watch output here