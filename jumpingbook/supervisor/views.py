#-*- coding:utf-8 -*-#
import json
from braces.views import SuperuserRequiredMixin
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View


# SuperuserRequiredMixin,
import requests
from core.models import Book, Category


class ScrapKyoboBookView(View):

    template_name = "supervisor/scrapkyobobook.html"

    def get(self, request, *args, **kwargs):

        return render(request,
                      self.template_name,
                      {} )

    def post(self, request, *args, **kwargs):

        category_code = request.POST.get('category-code')
        category_name = request.POST.get('category-name')

        category, created = Category.objects.get_or_create(name=category_name)

        for targetPage in range(1,5):
            payload = {'linkClass': category_code, 'mallGb': 'KOR', 'targetPage': str(targetPage)}
            r = requests.post("http://www.kyobobook.co.kr/category/recCategoryBookKorList.laf", data=payload)

            soup = BeautifulSoup(r.text)

            book_list = soup.find(id="detailList").find('table').find_all('tr')
            for book_item in book_list:
                image_url = book_item.select('.book_image img')[0]['src'].encode('utf-8')
                title = book_item.select('.book_title dt a strong')[0].string.strip().encode('utf-8')
                book_info = str(book_item.select('.book_title dd')[0])
                author = book_info[book_info.find('저자')+10:book_info.find('<span', book_info.find('저자')+10)-2].strip()
                publisher = book_info[book_info.find('출판사')+14:book_info.find('<!--', book_info.find('출판사')+14)].strip()
                published_date = book_info[ book_info.find('</span>',book_info.find('<!-- 출판일 -->')+12)+9:book_info.find('<!--', book_info.find('출판일')+12)].strip()

                # print title.encode('utf-8') + "/" + author + "/" + publisher + "/" + published_date
                book = Book(name=title,image_url=image_url, category=category, author=author, publisher=publisher, published_date=published_date.replace(".","-"))
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
