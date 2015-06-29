#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
from bs4 import BeautifulSoup
import psycopg2
import sys
from psycopg2._psycopg import ProgrammingError
import requests

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

    update_cursor = conn.cursor()

    cursor.execute("SELECT id, image_url FROM core_book where id>=247224;")
    for record in cursor:
        id = str(record[0])
        image_url = record[1]

        print id + "/" + image_url

        request_result = requests.get(image_url)
        if (request_result.status_code == 404):
            image_url = image_url.replace("xlarge","large").replace("/x","/l")
            query_string = 'update core_book set image_url=\'%s\' where id=%s' %( image_url, id )
            print query_string
            update_cursor.execute(query_string)
            conn.commit()



    conn.commit()

if __name__=="__main__":
    _get_db_connection()
    _start_scrapping()