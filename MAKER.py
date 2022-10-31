# in this file we make the .temp folder and download the images and save them in .temp folder after that we make a pdf file from that images.


import os
import shutil
import tqdm
import requests
from PIL import Image

CWD = os.getcwd()

def temp_folder_maker():
    if os.path.isdir('./.temp'):
        pass
    else:
        os.mkdir('.temp')


def HMANGA_folder_maker():
    if os.path.isdir('./HMANGA'):
        pass
    else:
        os.mkdir('HMANGA')


def Manga_folder_maker(manga_name):
    if os.path.isdir(f'./HMANGA/{manga_name}'):
        pass
    else:
        os.mkdir(f'./HMANGA/{manga_name}')


def image_downloadear(images_link):
    try : 
        for image_link in images_link:
            print()
            response = requests.get(image_link[1])
            total_size_in_bytes= int(response.headers.get('content-length', 0))
            block_size = 1024 #1 Kibibyte
            progress_bar = tqdm.tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True,colour='red')
            
            with open(CWD + f'/.temp/{image_link[0]}.jpg','wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                file.write(response.content)
            
            progress_bar.close()
            
    except:
        pass

def pdf_maker(manga_name , chapter):
    Path = './.temp'
    list_of_images = os.listdir(path = Path)
    list_of_images = sorted(list_of_images , key = lambda x: int(os.path.splitext(x)[0]))
    
    ready_images_list = []
    
    for image in list_of_images:
        img = Image.open(Path + f'/{image}')
        im = img.convert('RGB')
        ready_images_list.append(im)
    
    pdf_Path = f'./HMANGA/{manga_name}/{chapter}.pdf'
    ready_images_list[0].save(pdf_Path , save_all = True , append_images = ready_images_list)
    
    print(f'\nYour manga save in {pdf_Path}')
    shutil.rmtree(Path)
    
def main_maker():
    temp_folder_maker()
    HMANGA_folder_maker()
