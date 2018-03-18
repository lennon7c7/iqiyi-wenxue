#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import urllib2
from HTMLParser import HTMLParser

url = 'https://wenxue.iqiyi.com/book/reader-18l2gyeu1d-18l3c9mtdv.html'
book_id = url.split('-')[-2]
chapter_id = url.split('-')[-1].split('.')[0]
url_template = 'https://wenxue.iqiyi.com/book/reader-%s-%s.html?fr=207680739' % (book_id, '%s')

user_agent = 'User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 8_0_2 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A366 Safari/600.1.4)'
values = {}
headers = { 'User-Agent' : user_agent, 'Cookie' : 'bd_token=tRqfm0plD8N20kjtTMpPZs kliVzg2stYokk/U8RDD5dJua73QX75QiQL0I/BkqLxRIvN7rAfw4; bd_uid=D29180091A62A1CFA6A25BBEFC2B67D5; bd_cpid=10002; bd_gid=4305831314; litera_h5_prev_page=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; QC006=da0c96237b6b460dc27a67d824393c18; sourceFromType=baidu; QC005=1af75b059564a9e5cda46d3b588bbc4f; QC154=true; __dfp=a018d246d3b57f4b008e4079924b66927ac826fb9f103baf6e67ae199f019b679d@1519559471525@1516967471525; QC153=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; litera_h5_reffer=http%3A%2F%2Fwenxue.iqiyi.com%2Fbook%2Fdetail-18l2h10ca5.html; litera_h5_OrderInCurrentPage=667; cookie_readingProgress=%7B%2218l2h1252p%22%3A%2218l2al6dbf%22%2C%2218l2gyeu1d%22%3A%2218l3ad45lv%22%2C%2218l2h10ca5%22%3A%2218l2b79v8z%22%7D'}

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag = ''
        self.attrs = []
        self.title1 = ''
        self.content1 = '    '
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
            #print "Encountered some data  :", data

        pass

    def handle_data(self, data):
        def _attr(attrlist, attrname):
            for each in attrlist:
                if attrname == each[0]:
                    return each[1]
            return None


        if self.tag == 'span' and _attr(self.attrs, 'class') == 'c-name-gap' and data.strip() != '':
            self.title1 = data.strip()
            #print "Encountered some data  :", data


        if self.tag == 'p' and _attr(self.attrs, 'class') == 'c-contentB' and data.strip() != '':
            self.content1 = self.content1 + '\n    ' + data.strip()

        #print "Encountered some data  :", data
        pass

# 打开一个文件
fo = open("all.txt", "w")
fo.write('')
fo = open("all.txt", "a+")

while (chapter_id != ''):
    url_new = url_template % (chapter_id)
    the_page = urllib2.urlopen(urllib2.Request(url_new, {}, headers)).read()
    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(the_page)
    chapter_id = parser.next_chapter_id

    fo.write(parser.title1)
    fo.write(parser.content1)
    fo.write('\n\n')

    print parser.title1
    #print parser.content1
    #print parser.next_chapter_id

print 'done'

# 关闭打开的文件
fo.close()

