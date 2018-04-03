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
cookie = 'bd_token=tRqfm0plD8N20kjtTMpPZs kliVzg2stYokk/U8RDD5dJua73QX75QiQL0I/BkqLxRIvN7rAfw4; bd_uid=D29180091A62A1CFA6A25BBEFC2B67D5; bd_cpid=10002; bd_gid=4305831314; litera_h5_prev_page=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; QC006=da0c96237b6b460dc27a67d824393c18; sourceFromType=baidu; QC005=1af75b059564a9e5cda46d3b588bbc4f; QC154=true; __dfp=a018d246d3b57f4b008e4079924b66927ac826fb9f103baf6e67ae199f019b679d@1519559471525@1516967471525; QC153=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; litera_h5_reffer=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; litera_h5_OrderInCurrentPage=667; cookie_readingProgress=%7B%2218l2h1252p%22%3A%2218l2al6dbf%22%2C%2218l2gyeu1d%22%3A%2218l3ad45lv%22%2C%2218l2h10ca5%22%3A%2218l2b79v8z%22%7D'
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

        if self.book_title == '' and self.tag == 'div' and _attr(self.attrs, 'class') == 'c-name' and data != '':
            self.book_title = data

        if self.tag == 'span' and _attr(self.attrs, 'class') == 'c-name-gap' and data != '':
            self.chapter_title = data

        if self.tag == 'p' and _attr(self.attrs, 'class') == 'c-contentB' and data != '':
            self.chapter_content = self.chapter_content + '\n    ' + data

content_string = ''
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

    content_string += parser.chapter_title
    content_string += parser.chapter_content
    content_string += '\n\n'
    print unicode(parser.chapter_title, 'utf-8')
    i += 1

print unicode(parser.book_title, 'utf-8')

# write into file
fo = open(unicode(parser.book_title, 'utf-8') + '.txt', 'w')
fo.write(content_string)
fo.close()

