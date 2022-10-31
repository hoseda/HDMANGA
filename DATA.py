# in this page we gather all info about any manga an return them to another py file.


import requests
from bs4 import BeautifulSoup

MURL = 'https://manga-usa.com'
URL = 'https://manga-usa.com/manga/'


def page_response(url):
    res = requests.get(url)
    
    if res.ok:
        return True
    
    else:
        False

def get_page_html(Murl):
    Mpage = requests.get(Murl)
    Mpage_soup = BeautifulSoup(Mpage.content,'lxml')
    return Mpage_soup


def get_number_of_lastpage(page):
    last_page = page.find('ul',{'class':'pagination'}).select_one(':nth-last-child(2)').text
    return last_page.strip()
   

def get_number_of_items(page):
    div_list = page.find('div',{'class':'card-body'})
    div_num = div_list.find_all('div',{'class':'series-detail'})
    return len(div_num)
  

def get_name_and_link_of_items(page):
    items_name_and_link = []
    div_list = page.find('div',{'class':'card-body'})
    div_items = div_list.find_all('div',{'class':'series-detail'})
    
    for item in div_items:
        item_name = item.find('p',{'class':'item-title'}).text
        item_link = URL + item_name.replace(' ','-')
        items_name_and_link.append([item_name , item_link])

    return items_name_and_link


def get_summery_and_name_of_item(page):
    item_page = page.find('div',{'class':'card-body'})
    item_summery = item_page.find('p').text
    item_name = item_page.find('h1').text
    return [item_name , item_summery]


def get_chapter_and_link_of_theme(page):
    chapter_name_and_link = []
    chapters_item = page.find_all('div',{'class':'col-chapter'})
    
    for chapter in chapters_item:
        chapter_link = MURL + chapter.find('a').get('href')
        chapter_name = chapter.find('h5').find_all(text = True ,recursive = False)[0].replace('\n','')
        chapter_name_and_link.append([chapter_name , chapter_link])
    
    return chapter_name_and_link[::-1]


def get_images_link(page):
    images_link = []
    image_list = page.find_all('img',{'class':'lozad'}) 
    
    for image in image_list:
        images_link.append([image.get('alt') , image.get('data-src')])

    return images_link
    

# def extract_info(manga_name , number_of_chapter , summery , page_link):
#     info = {
#               'manga_name' : manga_name,
#               'number_of_chapter' : number_of_chapter,  
#               'summery' : summery,
#               'page_link' : page_link,
#             }
    
#     return info

