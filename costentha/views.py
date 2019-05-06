from django.shortcuts import render
from django.http import HttpResponse
# Used by 'getCity' view
import urllib.request
from bs4 import BeautifulSoup

import json

# Create your views here.


def getCity(request):
    ''' Scrapes a webpage and returns unique cities in the state of Andhra Pradesh  '''

    page = urllib.request.urlopen("http://www.manarythubazar.com/Andhra")
    soup = BeautifulSoup(page, features="html.parser")
    all_a = soup.find_all('a')  # Finding all <a> tags in the page
    text = [item.getText() for item in all_a]
    all_a = [str(item) for item in all_a]

    # Looking for '/andhra' in list items and if found,
    # converting them into lowercase and looking them up in master list.
    # If not found, giving them an entry

    master_area = []

    for item in all_a:
        temp = item.lower()
        if '/andhra' in temp:
            text_to_add = text[all_a.index(item)]
            if text_to_add not in master_area:
                master_area.append(text_to_add)

    # Status: Successful

    return render(request, 'home.html', {'cities': master_area})


def findArea(request):
    ''' Scrapes webpage with a certain 'city_name' and return areas. '''
    if request.method == 'GET':
        city_name = request.GET['city_name']
        state_name = request.GET['state_name']
        target_text = ('/'+state_name+'/'+city_name).lower()

        # For keywords like 'east godavari' url should be 'east%20godavari'
        # The rest are just fine
        city_name = city_name.replace(' ', '%20') 

        area_page = urllib.request.urlopen('http://www.manarythubazar.com/'+state_name+'/'+city_name+'/')

        soup = BeautifulSoup(area_page, features="html.parser")
        all_a = soup.find_all('a')
        text = [item.getText() for item in all_a]
        all_a = [str(item) for item in all_a]

        master_area = []

        for item in all_a:
            temp = item.lower()
            if target_text in temp:
                text_to_add = text[all_a.index(item)]
                if text_to_add not in master_area:
                    master_area.append(text_to_add)

        data = json.dumps({'areas': master_area})

        return HttpResponse(data)  
    else:
        return HttpResponse("Request method is not a GET")

def findPrice(request):

    if request.method == 'GET':
        state_name = request.GET['state_name']
        city_name = request.GET['city_name']
        area_name = request.GET['area_name']

        city_name, area_name = city_name.replace(' ', '%20'), area_name.replace(' ', '%20')
        area_name = area_name.replace('.', '@@')

        print(city_name, area_name)

        end_page = 'http://www.manarythubazar.com/'+state_name+'/'+city_name+'/'+area_name+'/'
        print(end_page)
        end_page = urllib.request.urlopen(end_page)
        end_soup = BeautifulSoup(end_page)
        all_td = end_soup.find_all('td')
        length_all_td = len(all_td)
        a,b = 1,3
        veg_name, veg_price = [], []

        while length_all_td - b > 4:
            veg_name.append(all_td[a].getText()) 
            veg_price.append(all_td[b].getText())
            a = a+4
            b = b+4
        print(veg_name, veg_price)

        data = json.dumps({'veg_name': veg_name, 'veg_price': veg_price})

        return HttpResponse(data)