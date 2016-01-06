import requests
from bs4 import BeautifulSoup as bs
import re
from mutagen.mp3 import MP3
from urllib import urlretrieve
import json
import math
import itertools


def scrape_page(base_url):
        page = requests.get(base_url)
        soup = bs(page.text, 'lxml')
        links = soup.find('table', 'archives').find_all('a')
        for link in links:
            title_link = 'http://www.dailywav.com'+link['href']
            title_page = requests.get(title_link)
            title_soup = bs(title_page.text, 'lxml')
            files_links = title_soup.find('div', 'view-content').find_all('a')
            for files_link in files_links:
                movie_link = 'http://www.dailywav.com'+files_link['href']
                movie_name = files_link.text.strip()
                movie_page = requests.get(movie_link)
                movie_soup = bs(movie_page.text, 'lxml')
                image_url = ''
                try:
                    image_url = movie_soup.find('div', 'coverArt2').find('img')['src']
                except:
                    try:
                        image_url = movie_soup.find('div', 'content quotes').find('img')['src']
                    except:
                        pass

                nodes = movie_soup.find_all('div', 'node-content-wrapper')
                for node in nodes:
                    file_url = node.find('div', 'content quotes').find('a')['href']
                    transcript = node.find('div', 'content quotes').find('p').text.strip()
                    file_type = file_url.split('.')[-1]
                    categories = 'Shows'
                    # try:
                    #     filename, headers = urlretrieve(link)
                    #     audio = MP3(filename)
                    #     if audio.info.length < 1:
                    #         length = int(math.ceil(audio.info.length))
                    #     else:
                    #         length = int(round(audio.info.length))
                    #     duration = length
                    # except:
                    #     duration = ''
                    print movie_link, movie_name, transcript,  file_type, file_url, categories, image_url
                    yield movie_link, movie_name, transcript,  file_type, file_url, categories, image_url

                next_link = ''
                try:
                    next_link = movie_soup.find('li', 'pager-next').find('a')
                except:
                    pass
                if next_link:
                    movie_page = requests.get('http://www.dailywav.com'+next_link)
                    movie_soup = bs(movie_page.text, 'lxml')
                    continue
                else:
                    break



def scrape():
   with open('data7.json', 'w') as outfile:
        sounds = {}
        lists = []
        base_url = 'http://www.dailywav.com/archives/shows/'
        s = scrape_page(base_url)
        for l in s:
            json_dic = {}
            json_dic['sourceUrl']=l[0]
            json_dic['movie name']=l[1]
            json_dic['transcript']=l[2]
            json_dic['fileType']=l[3]
            json_dic['fileUrl']=l[4]
            # json_dic['duration']=l[6]
            json_dic['categories']=l[5]
            json_dic['imageUrl']=l[5]
            print json_dic['movie name']
            lists.append(json_dic)
        sounds['sounds'] = lists
        json.dump(sounds, outfile, indent = 4)



if __name__ == '__main__':
    scrape()
