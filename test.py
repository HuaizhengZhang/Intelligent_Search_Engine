#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 31/3/17
# @Author  : Huaizheng ZHANG
# @Site    : zhanghuaizheng.com
# @File    : test.py

import xml.etree.cElementTree as ET

tree = ET.ElementTree(file = '../test/Posts.xml')
# for elem in tree.findall('row'):
#     title = elem.get('Title')
#     body = elem.get('Body')
#
#     print

count = 0
for event, elem in ET.iterparse('../test/Posts.xml'):
    if event == 'end':
        if elem.get('Title'):

            title = elem.get('Title')
        else:
            title = 'haha'
        if elem.get('Body'):
            body = elem.get('Body')
        else:
            body = 'wowo'
        count = count + 1
        print title, body
    elem.clear() # discard the element

print count
# from collections import Counter
# from xml.etree.ElementTree import parse
# from xml.etree.ElementTree import iterparse
#
#
# def parse_and_remove(filename, path):
#     path_parts = path.split('/')
#     doc = iterparse(filename, ('start', 'end'))
#     # Skip the root element
#     next(doc)
#
#     tag_stack = []
#     elem_stack = []
#     for event, elem in doc:
#         if event == 'start':
#             tag_stack.append(elem.tag)
#             elem_stack.append(elem)
#         elif event == 'end':
#             if tag_stack == path_parts:
#                 yield elem
#                 elem_stack[-2].remove(elem)
#             try:
#                 tag_stack.pop()
#                 elem_stack.pop()
#             except IndexError:
#                 pass
#
# potholes_by_zip = Counter()
#
# data = parse_and_remove('../test/Posts.xml', 'row')
# for pothole in data:
#     potholes_by_zip[pothole.findtext('title')] += 1
# for zipcode, num in potholes_by_zip.most_common():
#     print(zipcode, num)
