#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
from bs4 import BeautifulSoup
import psycopg2
import sys
import requests


# http://m.kyobobook.com/searchLinkClass?productType=KOR&linkClass=01&comboBoxId=%25EB%258F%2584%25EC%2584%259C_%25EC%2586%258C%25EC%2584%25A4Combo&period=WEEK&invokeEvent=true
categorys = [{
    'baseLinkClassName': u'소설',
    'baseLinkClass': '01',
    'items':[
        {
            'name': u'청소년소설',
            'linkClass': '0118'
        }
    ]
}]

conn = None
cursor = None

def _get_db_connection():
    global conn, cursor
    #Define our connection string
    conn_string = "host='jumpingbookdbinstance.chxobddaq8ce.ap-northeast-1.rds.amazonaws.com' dbname='jumpingbook' user='root' password='parkjuram90'"

    # print the connection string we will use to connect
    print "Connecting to database\n	->%s" % (conn_string)

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

def _start_scrapping():
    global conn, cursor

    for category in categorys:
        query_string = "insert into core_category(name, link_class) select '%s', '%s' where not exists ( select id from core_category where name = '%s' );"\
        % (category['baseLinkClassName'], category['baseLinkClass'], category['baseLinkClassName'])

        cursor.execute(query_string)
        # conn.commit()

        query_string = "SELECT id FROM core_category WHERE name = '%s'" % (category['baseLinkClassName'])
        cursor.execute(query_string)
        category_id = cursor.fetchone()[0]

        for subcategory in category['items']:
            query_string = "insert into core_subcategory(name, link_class, category_id) select '%s', '%s', '%s' where not exists ( select id from core_subcategory where name='%s' );" \
                           % (subcategory['name'], subcategory['linkClass'], category_id, subcategory['name'])

            cursor.execute(query_string)
            # conn.commit()

            query_string = "SELECT id FROM core_subcategory WHERE name = '%s'" % (subcategory['name'])
            cursor.execute(query_string)
            subcategory_id = cursor.fetchone()[0]
            offset = "1"

            while True:

                print "offset : "+ offset
                book_list_url = "http://m.kyobobook.com/search/byCategory/KOR/%s/SALE_QTY?orderClick=mC8&size=10&offset=%s&tabId=&linkClass=%s" \
                %(subcategory['linkClass'], offset, subcategory['linkClass'])

                print book_list_url

                r = requests.get(book_list_url)
                book_list_json = r.json()
                offset = str(int(offset) + 1)
                for item in book_list_json['items']:
                    title = item['title']
                    image_url = item['imageUrl']
                    image_url = image_url.replace("medium","xlarge").replace("/m","/x")
                    author = item['authorName']
                    publisher = item['publisherName']
                    barcode = item['barcode']
                    # published_date = item['publishingDay']
                    published_date = "20150622"

                    query_string = "insert into core_book(title, barcode, image_url, author, publisher, published_date, category_id) select '%s', '%s', '%s', '%s', '%s', '%s', '%s' where not exists ( select id from core_book where title = '%s' and author = '%s' );" \
                               % (title, barcode, image_url, author, publisher, published_date, subcategory_id, title, author)


                    # print query_string
                    cursor.execute(query_string)

                if book_list_json['more'] == False:
                    break


    conn.commit()



    #
    # category_code = "010101"
    # category_name = u"고전소설"
    # category_id = "2"
    #
    #
    # for targetPage in range(5,6):
    #     payload = {'linkClass': category_code, 'mallGb': 'KOR', 'targetPage': str(targetPage)}
    #     r = requests.post("http://www.kyobobook.co.kr/category/recCategoryBookKorList.laf", data=payload)
    #
    #     soup = BeautifulSoup(r.text)
    #
    #     book_list = soup.find(id="detailList").find('table').find_all('tr')
    #
    #     print len(book_list)
    #
    #     for book_item in book_list:
    #         image_url = book_item.select('.book_image img')[0]['src'].encode('utf-8')
    #         title = book_item.select('.book_title dt a strong')[0].string.strip().encode('utf-8')
    #         book_info = str(book_item.select('.book_title dd')[0])
    #         author = book_info[book_info.find('저자')+10:book_info.find('<span', book_info.find('저자')+10)-2].strip()
    #         publisher = book_info[book_info.find('출판사')+14:book_info.find('<!--', book_info.find('출판사')+14)].strip()
    #         published_date = book_info[ book_info.find('</span>',book_info.find('<!-- 출판일 -->')+12)+9:book_info.find('<!--', book_info.find('출판일')+12)].strip()
    #
    #         # print title + "/" + author + "/" + publisher + "/" + published_date
    #         query_string = "insert into core_book(name, image_url, author, publisher, published_date, category_id) select '%s', '%s', '%s', '%s', '%s', '%s' where not exists ( select id from core_book where name = '%s' and author = '%s' );" \
    #                        % (title, image_url, author, publisher, published_date, category_id, title, author)
    #
    #         print query_string
    #         cursor.execute(query_string)
    #
    #     if len(book_list) != 20:
    #         break
    # conn.commit()

if __name__=="__main__":
    _get_db_connection()
    _start_scrapping()