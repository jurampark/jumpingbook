#!/usr/bin/python
# -*- coding: utf-8 -*-

import pprint
from bs4 import BeautifulSoup
import psycopg2
import sys
from psycopg2._psycopg import ProgrammingError
import requests


# http://m.kyobobook.com/searchLinkClass?productType=KOR&linkClass=01&comboBoxId=%25EB%258F%2584%25EC%2584%259C_%25EC%2586%258C%25EC%2584%25A4Combo&period=WEEK&invokeEvent=true
categorys = [
# {
#     'baseLinkClassName': u'소설',
#     'baseLinkClass': '01',
#     'items':[
#         # {
#         #     "name": u'청소년소설',
#         #     "linkClass": '0118'
#         # },
#         {
#             "name": u'한국소설',
#             "linkClass": '0101'
#         },
#         {
#             "name": u'영미소설',
#             "linkClass": '0103'
#         },
#         {
#             "name": u'일본소설',
#             "linkClass": '0105'
#         },
#         {
#             "name": u'중국소설',
#             "linkClass": '0107'
#         },
#         {
#             "name": u'기타나라소설',
#             "linkClass": '0113'
#         },
#         {
#             "name": u'라이트 노벨',
#             "linkClass": '0114'
#         },
#         {
#             "name": u'장르소설',
#             "linkClass": '0115'
#         },
#         {
#             "name": u'테마소설',
#             "linkClass": '0117'
#         },
#         {
#             "name": u'세계문학',
#             "linkClass": '0121'
#         },
#         {
#             "name": u'세계고전',
#             "linkClass": '0123'
#         },
#         {
#             "name": u'러시아소설',
#             "linkClass": '0109'
#         },
#         {
#             "name": u'독일소설',
#             "linkClass": '0112'
#         },
#         {
#             "name": u'프랑스소설',
#             "linkClass": '0111'
#         }
#     ]
# },
# {
#     'baseLinkClassName': u'자기계발',
#     'baseLinkClass': '15',
#     'items':[
#         {
#             "name": u'성공/처세',
#             "linkClass": '1501',
#         },
#         {
#             "name": u'자기능력계발',
#             "linkClass": '1503',
#         },
#         {
#             "name": u'비즈니스능력계발',
#             "linkClass": '1505',
#         },
#         {
#             "name": u'인간관계',
#             "linkClass": '1506',
#         },
#         {
#             "name": u'화술/협상',
#             "linkClass": '1507',
#         },
#         {
#             "name": u'청소년자기계발',
#             "linkClass": '1508',
#         },
#         {
#             "name": u'오디오북',
#             "linkClass": '1509',
#         }
#     ]
# },
# {
#     'baseLinkClassName': u'컴퓨터/IT',
#     'baseLinkClass': '33',
#     'items':[
#         {
#             "name": u'IT에세이',
#             "linkClass": '3302',
#         },
#         {
#             "name": u'컴퓨터공학',
#             "linkClass": '3301',
#         },
#         {
#             "name": u'컴퓨터입문/활용',
#             "linkClass": '3303',
#         },
#         {
#             "name": u'전산통계/해석',
#             "linkClass": '3305',
#         },
#         {
#             "name": u'OS',
#             "linkClass": '3307',
#         },
#         {
#             "name": u'네트워크',
#             "linkClass": '3309',
#         },
#         {
#             "name": u'데이터베이스',
#             "linkClass": '3311',
#         },
#         {
#             "name": u'게임',
#             "linkClass": '3313',
#         },
#         {
#             "name": u'프로그래밍/언어',
#             "linkClass": '3315',
#         },
#         {
#             "name": u'OA/사무자동화',
#             "linkClass": '3317',
#         },
#         {
#             "name": u'웹사이트',
#             "linkClass": '3319',
#         },
#         {
#             "name": u'그래픽',
#             "linkClass": '3321',
#         },
#         {
#             "name": u'멀티미디어',
#             "linkClass": '3323',
#         },
#         {
#             "name": u'CAD',
#             "linkClass": '3325',
#         },
#         {
#             "name": u'대학교재',
#             "linkClass": '3329',
#         },
#         {
#             "name": u'모바일프로그래밍',
#             "linkClass": '3316',
#         },
#         {
#             "name": u'보안/해킹',
#             "linkClass": '3310',
#         },
#         {
#             "name": u'개발방법론',
#             "linkClass": '3312',
#         },
#         {
#             "name": u'웹프로그래밍',
#             "linkClass": '3314',
#         }
#     ]
# },
# {
#     'baseLinkClassName': u'경제/경영',
#     'baseLinkClass': '13',
#     'items':[
#         {
#             "name": u'경영일반',
#             "linkClass": '1301',
#         },
#         {
#             "name": u'경영이론',
#             "linkClass": '1303',
#         },
#         {
#             "name": u'경영관리',
#             "linkClass": '1305',
#         },
#         {
#             "name": u'경영전략',
#             "linkClass": '1307',
#         },
#         {
#             "name": u'경제일반',
#             "linkClass": '1309',
#         },
#         {
#             "name": u'경제이론',
#             "linkClass": '1311',
#         },
#         {
#             "name": u'기업경제',
#             "linkClass": '1313',
#         },
#         {
#             "name": u'각국경제',
#             "linkClass": '1315',
#         },
#         {
#             "name": u'기업실무관리',
#             "linkClass": '1317',
#         },
#         {
#             "name": u'마케팅/세일즈',
#             "linkClass": '1319',
#         },
#         {
#             "name": u'유통/창업',
#             "linkClass": '1321',
#         },
#         {
#             "name": u'재테크/금융',
#             "linkClass": '1323',
#         },
#         {
#             "name": u'무역/운송',
#             "linkClass": '1325',
#         },
#         {
#             "name": u'관광/호텔',
#             "linkClass": '1327',
#         },
#         {
#             "name": u'경제/경영문고',
#             "linkClass": '1329',
#         },
#         {
#             "name": u'대학교재',
#             "linkClass": '1331',
#         }
#     ]
# },
{
    'baseLinkClassName': u'인문',
    'baseLinkClass': '05',
    'items':[
        # {
        #     "name": u'독서/글쓰기',
        #     "linkClass": '0525',
        # },
        # {
        #     "name": u'문헌정보학',
        #     "linkClass": '0527',
        # },
        # {
        #     "name": u'역학/사주',
        #     "linkClass": '0529',
        # },
        # {
        #     "name": u'인문교양문고',
        #     "linkClass": '0533',
        # },
        # {
        #     "name": u'인문고전문고',
        #     "linkClass": '0535',
        # },
        # {
        #     "name": u'인문학일반',
        #     "linkClass": '0501',
        # },
        # {
        #     "name": u'심리학',
        #     "linkClass": '0503',
        # },
        # {
        #     "name": u'교육학',
        #     "linkClass": '0505',
        # },
        # {
        #     "name": u'유아교육',
        #     "linkClass": '0507',
        # },
        # {
        #     "name": u'특수교육',
        #     "linkClass": '0509',
        # },
        # {
        #     "name": u'임용고시',
        #     "linkClass": '0511',
        # },
        {
            "name": u'철학',
            "linkClass": '0513',
        },
        {
            "name": u'문학이론',
            "linkClass": '0515',
        },
        {
            "name": u'한국문학론',
            "linkClass": '0517',
        },
        {
            "name": u'영미문학론',
            "linkClass": '0519',
        },
        {
            "name": u'중국문학론',
            "linkClass": '0520',
        },
        {
            "name": u'세계문학론',
            "linkClass": '0521',
        },
        {
            "name": u'언어학',
            "linkClass": '0523',
        },
        {
            "name": u'대학교재',
            "linkClass": '0532',
        }
    ]
},
{
    'baseLinkClassName': u'과학',
    'baseLinkClass': '29',
    'items':[
        {
            "name": u'과학이론',
            "linkClass": '2901',
        },
        {
            "name": u'도감',
            "linkClass": '2903',
        },
        {
            "name": u'교양과학',
            "linkClass": '2905',
        },
        {
            "name": u'수학',
            "linkClass": '2907',
        },
        {
            "name": u'물리학',
            "linkClass": '2909',
        },
        {
            "name": u'화학',
            "linkClass": '2911',
        },
        {
            "name": u'생물학',
            "linkClass": '2913',
        },
        {
            "name": u'지구과학',
            "linkClass": '2915',
        },
        {
            "name": u'천문학',
            "linkClass": '2917',
        },
        {
            "name": u'청소년 교양과학',
            "linkClass": '2918',
        },
        {
            "name": u'과학문고',
            "linkClass": '2919',
        },
        {
            "name": u'초과학',
            "linkClass": '2923',
        },
        {
            "name": u'대학교재',
            "linkClass": '2921',
        }
    ]
},
{
    'baseLinkClassName': u'기술/공학',
    'baseLinkClass': '26',
    'items':[
        {
            "name": u'금속/재료',
            "linkClass": '2611',
        },
        {
            "name": u'공학일반',
            "linkClass": '2609',
        },
        {
            "name": u'생활과학',
            "linkClass": '2619',
        },
        {
            "name": u'의학',
            "linkClass": '2621',
        },
        {
            "name": u'건축/인테리어',
            "linkClass": '2601',
        },
        {
            "name": u'토목/건설',
            "linkClass": '2603',
        },
        {
            "name": u'환경/소방/도시/조경',
            "linkClass": '2605',
        },
        {
            "name": u'자동차/운전',
            "linkClass": '2607',
        },
        {
            "name": u'운전면허',
            "linkClass": '2608',
        },
        {
            "name": u'기계/역학/항공',
            "linkClass": '2613',
        },
        {
            "name": u'전기/전자',
            "linkClass": '2615',
        },
        {
            "name": u'농수산/축산',
            "linkClass": '2617',
        },
        {
            "name": u'대학교재',
            "linkClass": '2623',
        }
    ]
},
{
    'baseLinkClassName': u'요리',
    'baseLinkClass': '08',
    'items':[
        {
            "name": u'요리일반',
            "linkClass": '0801',
        },
        {
            "name": u'테마별요리',
            "linkClass": '0803',
        },
        {
            "name": u'베이킹/간식',
            "linkClass": '0805',
        },
        {
            "name": u'계절요리',
            "linkClass": '0807',
        },
        {
            "name": u'재료별요리',
            "linkClass": '0809',
        },
        {
            "name": u'나라별요리',
            "linkClass": '0811',
        },
        {
            "name": u'전문요리',
            "linkClass": '0815',
        },
        {
            "name": u'와인/커피/음료',
            "linkClass": '0817',
        },
        {
            "name": u'생활요리',
            "linkClass": '0813',
        },
        {
            "name": u'요리수험서',
            "linkClass": '0819',
        },
        {
            "name": u'요리에세이',
            "linkClass": '0802',
        }
    ]
},
{
    'baseLinkClassName': u'건강',
    'baseLinkClass': '09',
    'items':[
        {
            "name": u'건강일반',
            "linkClass": '0901',
        },
        {
            "name": u'뇌건강',
            "linkClass": '0903',
        },
        {
            "name": u'한방치료',
            "linkClass": '0905',
        },
        {
            "name": u'질병치료/예방',
            "linkClass": '0909',
        },
        {
            "name": u'다이어트',
            "linkClass": '0911',
        },
        {
            "name": u'건강문고',
            "linkClass": '0920',
        },
        {
            "name": u'자연건강',
            "linkClass": '0907',
        },
        {
            "name": u'건강식사',
            "linkClass": '0908',
        },
        {
            "name": u'운동/트레이닝',
            "linkClass": '0913',
        },
        {
            "name": u'피부관리/메이크업',
            "linkClass": '0915',
        }
    ]
},
{
    'baseLinkClassName': u'청소년',
    'baseLinkClass': '38',
    'items':[
        {
            "name": u'청소년 교양공학',
            "linkClass": '3835',
        },
        {
            "name": u'청소년 소설',
            "linkClass": '3813',
        },
        {
            "name": u'논술(단행본)',
            "linkClass": '3801',
        },
        {
            "name": u'공부방법',
            "linkClass": '3802',
        },
        {
            "name": u'진로',
            "linkClass": '3803',
        },
        {
            "name": u'명문대진학가이드',
            "linkClass": '3804',
        },
        {
            "name": u'성교육',
            "linkClass": '3805',
        },
        {
            "name": u'청소년 자기계발',
            "linkClass": '3809',
        },
        {
            "name": u'청소년 에세이',
            "linkClass": '3811',
        },
        {
            "name": u'청소년 시',
            "linkClass": '3815',
        },
        {
            "name": u'청소년 고전',
            "linkClass": '3817',
        },
        {
            "name": u'청소년 문학기타',
            "linkClass": '3819',
        },
        {
            "name": u'청소년 철학',
            "linkClass": '3821',
        },
        {
            "name": u'청소년 역사',
            "linkClass": '3823',
        },
        {
            "name": u'청소년 예술',
            "linkClass": '3825',
        },
        {
            "name": u'청소년 인문교양',
            "linkClass": '3827',
        },
        {
            "name": u'청소년 경제',
            "linkClass": '3829',
        },
        {
            "name": u'청소년 정치사회',
            "linkClass": '3831',
        },
        {
            "name": u'청소년 교양과학',
            "linkClass": '3833',
        }
    ]
},
{
    'baseLinkClassName': u'여행',
    'baseLinkClass': '32',
    'items':[
        {
            "name": u'국내여행',
            "linkClass": '3201',
        },
        {
            "name": u'해외여행',
            "linkClass": '3203',
        },
        {
            "name": u'테마여행',
            "linkClass": '3205',
        },
        {
            "name": u'인기지역',
            "linkClass": '3206',
        },
        {
            "name": u'지도',
            "linkClass": '3214',
        },
        {
            "name": u'여행에세이',
            "linkClass": '3204',
        }
    ]
},
{
    'baseLinkClassName': u'취미/실용/스포츠',
    'baseLinkClass': '11',
    'items':[
        {
            "name": u'취미일반',
            "linkClass": '1124',
        },
        {
            "name": u'살림의지혜',
            "linkClass": '1104',
        },
        {
            "name": u'가정원예',
            "linkClass": '1101',
        },
        {
            "name": u'애완동물',
            "linkClass": '1105',
        },
        {
            "name": u'등산/낚시',
            "linkClass": '1107',
        },
        {
            "name": u'바둑',
            "linkClass": '1109',
        },
        {
            "name": u'골프',
            "linkClass": '1111',
        },
        {
            "name": u'무술',
            "linkClass": '1113',
        },
        {
            "name": u'스포츠',
            "linkClass": '1115',
        },
        {
            "name": u'무용',
            "linkClass": '1119',
        },
        {
            "name": u'체육',
            "linkClass": '1121',
        },
        {
            "name": u'취미관련상품',
            "linkClass": '1125',
        },
        {
            "name": u'대학교재',
            "linkClass": '1130',
        },
        {
            "name": u'생활공예/DIY',
            "linkClass": '1103',
        },
        {
            "name": u'레크레이션/게임',
            "linkClass": '1117',
        },
        {
            "name": u'퀴즈/퍼즐/스도쿠',
            "linkClass": '1118',
        },
        {
            "name": u'홈인테리어/수납',
            "linkClass": '1102',
        }
    ]
}
]

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
                    title = title.replace("'", "''")
                    image_url = item['imageUrl']
                    # image_url = image_url.replace("medium","xlarge").replace("/m","/x")
                    author = item['authorName']
                    author = author.replace("'", "''")
                    publisher = item['publisherName']
                    barcode = item['barcode']
                    readerContentGradeAverage = item['readerContentGradeAverage']
                    memberReviewCount = item['memberReviewCount']
                    # published_date = item['publishingDay']
                    published_date = "20151006"

                    query_string = "insert into core_book(title, barcode, image_url, author, publisher, published_date, category_id) select '%s', '%s', '%s', '%s', '%s', '%s', '%s' where not exists ( select id from core_book where title = '%s' and author = '%s' );" \
                               % (title, barcode, image_url, author, publisher, published_date, subcategory_id, title, author)


                    # print query_string
                    try:
                        cursor.execute(query_string)
                    except ProgrammingError as e:
                        print query_string
                        print e

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