#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding=utf-8
import os
import urllib2
from HTMLParser import HTMLParser

url = raw_input('input url here: ')
if url == '':
    url = 'https://wenxue.iqiyi.com/book/reader-18l2gzwvjt-18l3mg6v2r.html'
    print 'default: ', url
book_id = url.split('-')[-2]
chapter_id = url.split('-')[-1].split('.')[0]
url_template = 'https://wenxue.iqiyi.com/book/reader-%s-%s.html?fr=207680739' % (book_id, '%s')

chapter_title_prefix = raw_input('input chapter title prefix here: ')
if chapter_title_prefix == '':
    #chapter_title_prefix = 'chapter %s - '
    chapter_title_prefix = '第%s章 - '
    print 'default: ', unicode(chapter_title_prefix, 'utf-8')

user_agent = 'User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4)'
cookie = 'sourcePage=aladdin'
headers = { 'User-Agent' : user_agent, 'Cookie' : cookie}

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag = ''
        self.attrs = []
        self.book_title = ''
        self.chapter_title = ''
        self.chapter_content = '    '
        self.next_chapter_id = ''

    def handle_starttag(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs

        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
            return None

        if self.tag == 'a' and _attr(self.attrs, 'changechapterid'):
            self.next_chapter_id = _attr(self.attrs, 'changechapterid')

    def handle_data(self, data):
        data = data.strip()
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
            return None

        if self.book_title == '' and self.tag == 'span' and _attr(self.attrs, 'class') == 'reader-page' and data != '':
            self.book_title = data

        if self.tag == 'span' and _attr(self.attrs, 'class') == 'c-name-gap' and data != '':
            self.chapter_title = data

        if self.tag == 'p' and _attr(self.attrs, 'class') == 'c-contentB' and data != '':
            self.chapter_content = self.chapter_content + '\n    ' + data

i = 1
while (chapter_id != ''):
    url_new = url_template % (chapter_id)
    the_page = urllib2.urlopen(urllib2.Request(url_new, {}, headers)).read()
    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(the_page)
    chapter_id = parser.next_chapter_id

    if chapter_title_prefix != '':
        parser.chapter_title = (chapter_title_prefix % (i)) + parser.chapter_title

    print unicode(parser.chapter_title, 'utf-8')
    if parser.book_title != '':
        fo = open(unicode(parser.book_title, 'utf-8') + '.txt', 'a+')
    else:
        fo = open(book_id + '.txt', 'a+')
    fo.write(parser.chapter_title)
    fo.write(parser.chapter_content)
    fo.write('\n\n')
    fo.close()
    i += 1

print unicode(parser.book_title, 'utf-8')
