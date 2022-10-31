# this is the main file and we control every things here and let client choice and show him the result.


import inspect
import os
import sys
import time
from textwrap import TextWrapper

import pyfiglet
from colorama import Back, Fore, init

import DATA
import MAKER

init()

def screen_cleaner():
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        os.system("clear")


def figlet():
    fglet = pyfiglet.Figlet('doom',width= 200)
    print(Fore.CYAN + fglet.renderText('HMANGA'))

def banner():
    screen_cleaner()
    figlet()
    
    item_1 = Fore.LIGHTYELLOW_EX + '   [1] All Manga\n'
    item_2 = Fore.LIGHTYELLOW_EX + '  [2] Search Manga\n'
    item_3 = Fore.LIGHTRED_EX + '  [0] Exit\n' + Fore.RESET +  Fore.RESET
        
    print(item_1 , item_2 , item_3)
    chosing_banner()

def chosing_banner():
    while True:
        entry = str(input(Fore.LIGHTGREEN_EX + 'Choose one item : ' + Fore.RESET)).strip()
        
        if entry == 0 or entry == '0':
            print(Fore.LIGHTWHITE_EX + '\nGoodBye...!\n')
            quit()
            
        elif entry == 1 or entry == '1':
            all_manga()
            break
        
        elif entry == 2 or entry == '2':
            search_manga()
            break
            
        else:
            print(Fore.LIGHTRED_EX + 'you enter somethings wrong!!!' + Fore.RESET)
            continue

def back(input):
    if input == 0 or input == '0':
        banner()
    
    else:
        pass


def search_manga():
    screen_cleaner()
    figlet()
    print(Fore.LIGHTBLUE_EX + ' PLEASE PAY ATTENTION '.center(71 ,'*'))
    print('\n')
    print(Fore.LIGHTWHITE_EX +  ' enter all name of manga '.capitalize().center(71 , ' '))
    print('\n')
    
    while True:
        print( Fore.LIGHTRED_EX + '  [0] Back' + Fore.RESET)
        name = str(input(Fore.LIGHTYELLOW_EX + "  Enter name of manga : " + Fore.RESET))
        url = DATA.URL + name.replace(' ' , '-')
        
        back(name)
        
        response = DATA.page_response(url)
        
        if  name != '' and response:
            process_info(url)
            break
        
        else:
            print('\n===> \n    there are no manga with this name , maybe you enter name wrong.\n')
            continue
 
 
def all_manga(pg = 1):
    pg = pg    
    all_url = f'https://manga-usa.com/manga?page={pg}'
    page = DATA.get_page_html(all_url)
    l_pg = int(DATA.get_number_of_lastpage(page))    
    number_of_items = DATA.get_number_of_items(page)
    name_link_of_items = DATA.get_name_and_link_of_items(page)
      
    all_manga_chooser([number_of_items , name_link_of_items , l_pg , pg]) 
   
            
def process_info(url):
    caller = inspect.stack()[1][3]
    page = DATA.get_page_html(url)
    
    if caller == 'search_manga':
        info = DATA.get_summery_and_name_of_item(page)
        chapters = DATA.get_chapter_and_link_of_theme(page)
        show_manga([caller , info , chapters])
    
    else:
        info = DATA.get_summery_and_name_of_item(page)
        chapters = DATA.get_chapter_and_link_of_theme(page)
        show_manga([caller , info , chapters])


def all_manga_chooser(info):
    screen_cleaner()
    figlet()
    print(Fore.LIGHTRED_EX + '> All Manga <'.center(120 , '=' ) + Fore.RESET , end = '\n\n')
    print(Fore.WHITE +  f'Current page : {info[3]}' + Fore.RESET, end = ' \n')
    print()
        
    for item in range(1 , info[0]+1):
        obj = Fore.LIGHTYELLOW_EX + f'    ==> [{item}] {info[1][item-1][0]}' + Fore.RESET
        print(obj)
        
    while True:
        if int(info[3]) == 1:
            print(Fore.MAGENTA + '\n[N] Next Page' + Fore.RESET)
            print(Fore.LIGHTRED_EX + '[0] Back' + Fore.RESET)

        elif int(info[3]) == 27:
            print(Fore.MAGENTA + '[P] Previous Page' + Fore.RESET)
            print(Fore.LIGHTRED_EX + '[0] Back' + Fore.RESET)

        else:
            print(Fore.MAGENTA + '\n[N] Next Page' + Fore.RESET)
            print(Fore.MAGENTA + '[P] Previous Page' + Fore.RESET)
            print(Fore.LIGHTRED_EX + '[0] Back' + Fore.RESET)
            
        entry = str(input(Fore.LIGHTGREEN_EX + 'Enter Number of Item : ' + Fore.RESET))

        if str(entry) == '0':
            back(entry)
            break
            
        elif entry.lower() == 'n':
            all_manga(int(info[3] + 1))
            break
                
        elif entry.lower() == 'p':
            all_manga(int(info[3] - 1))
            break
            
        elif int(entry) in range(1 , int(info[0]) + 1):
            Url = info[1][int(entry) - 1][1]
            process_info(Url)
            break
            
        else:
            print(Fore.LIGHTRED_EX + 'you enter something wrong' + Fore.RESET)
            break



def show_manga(info):
    screen_cleaner()
    figlet()
    print(Fore.LIGHTWHITE_EX + '\n Manga Name : '+Fore.LIGHTYELLOW_EX + f'{info[1][0]}' + Fore.RESET) 
    print(Fore.WHITE + "\n Summery : \n" + Fore.RESET)
        
    wrapper = TextWrapper(width = 150)
    word_list = wrapper.wrap(info[1][1])
        
    for word in word_list:
        print(Fore.LIGHTBLUE_EX + word + Fore.RESET)
        
    print(Back.LIGHTRED_EX + '<+++>'.center(130 , '^') + Back.RESET)
    print(Fore.LIGHTWHITE_EX+ '\n Chapters : \n' + Fore.RESET)
    item = 1
    for chapter in info[2]:
        print(Fore.LIGHTYELLOW_EX + '    ==> ' +f'[{item}] ' + chapter[0] + Fore.RESET)
        item += 1

    choose_chapter(info)
        
        

def choose_chapter(info):
    chapters = info[2]
    num_chapters = len(chapters)
    while True:
        print(Fore.LIGHTRED_EX + '\n[0] Back' + Fore.RESET)
        chapter = str(input(Fore.LIGHTGREEN_EX + "Choose a Chapter : " + Fore.RESET)).strip()
        
        if chapter == 0 or chapter == '0':
            back(chapter)
            break
        
        elif int(chapter) in range(1 , num_chapters+1):
            print(Fore.CYAN + 'Downloading .... \n' + Fore.RESET)
            downloader(info[1][0] , chapters[int(chapter) -1][0], chapters[int(chapter) -1][1])
            break

        else:
            print(Fore.LIGHTRED_EX + 'You Enter Something Wrong!!!' + Fore.RESET)
            continue


def try_again():
    while True:
        entry = str(input(Fore.LIGHTGREEN_EX + '\nDid you wanna try it again [Yes / No] : ' + Fore.RESET))

        if entry.lower() == 'yes':
            print(Fore.LIGHTWHITE_EX + 'Ok ...' + Fore.RESET)
            time.sleep(0.7)
            banner()
            break
        
        elif entry.lower() == 'no':
            print(Fore.LIGHTWHITE_EX + 'Goodbye ...' + Fore.RESET)
            time.sleep(0.5)
            quit()
            
        else:
            print(Fore.LIGHTRED_EX + "Enter Something Wrong!!" + Fore.RESET)
            continue


def downloader(manga_name , chapter_number , chapter_link):
    MAKER.main_maker()
    MAKER.Manga_folder_maker(manga_name)
    
    images_link = DATA.get_images_link(DATA.get_page_html(chapter_link + '/all'))
    MAKER.image_downloadear(images_link)
    MAKER.pdf_maker(manga_name , chapter_number)
    
    try_again()
        
banner()
