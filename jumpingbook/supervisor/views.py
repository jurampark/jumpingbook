#-*- coding:utf-8 -*-#
import json
from braces.views import SuperuserRequiredMixin
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View


# SuperuserRequiredMixin,
import requests
from recommend.models import Book, Category


class ScrapKyoboBookView(View):

    template_name = "supervisor/scrapkyobobook.html"

    def get(self, request, *args, **kwargs):

        return render(request,
                      self.template_name,
                      {} )

    def post(self, request, *args, **kwargs):

        category = Category.objects.get(name='한국소설')

        for targetPage in range(1,5):
            payload = {'linkClass': '0101', 'mallGb': 'KOR', 'targetPage': str(targetPage)}
            r = requests.post("http://www.kyobobook.co.kr/category/recCategoryBookKorList.laf", data=payload)

            soup = BeautifulSoup(r.text)

            book_list = soup.find(id="detailList").find('table').find_all('tr')
            for book_item in book_list:
                title = book_item.select('.book_title dt a strong')[0].string.strip()
                book_info = str(book_item.select('.book_title dd')[0])
                author = book_info[book_info.find('저자')+10:book_info.find('<span', book_info.find('저자')+10)-2].strip()
                publisher = book_info[book_info.find('출판사')+14:book_info.find('<!--', book_info.find('출판사')+14)].strip()
                published_date = book_info[ book_info.find('</span>',book_info.find('<!-- 출판일 -->')+12)+9:book_info.find('<!--', book_info.find('출판일')+12)].strip()

                print title.encode('utf-8') + "/" + author + "/" + publisher + "/" + published_date
                book = Book(name=title.encode('utf-8'), category=category, author=author, publisher=publisher, published_date=published_date.replace(".","-"))
                book.save()

        response_data = {
            'testkey': u'data from server'
        }

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    #     ids = request.POST.get('ids')
    #     ids = ids.split("@")
    #     values = request.POST.get('values')
    #     values = values.split("@")
    #
    #     for i in range(len(ids)):
    #         id = ids[i]
    #         value = values[i]
    #         UserSurvey.objects.filter(id=id).update(result_file_name=str(value))
    #
    #     return redirect("supervisor:analysis")
