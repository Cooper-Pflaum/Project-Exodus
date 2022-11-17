# importing libraries
import os
import shutil
import time
import requests
import urllib
from bs4 import BeautifulSoup
from Colors import colors
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
URL = 'https://www.instagram.com/{}/?hl=en'

# instantiate a chrome options object so you can set the size and headless preference

# driver = uc.Chrome()

def getTopResults(name, last_name = '', num_results=20, command = ''):
    if last_name != '':
        query_name = name + ' ' + last_name
    else:
        query_name = name
    query = query_name.replace(' ', '+')
    query += '+instagram'
    pwned_users = []
    results = search(query, int(num_results))

    for url in results:
        user = ''
        prefix = 'https://www.instagram.com/'
        suffix = '/?hl=en'
        # print(url)
        if prefix in url:
            removed_prefix = url.replace(prefix,'')
            user = removed_prefix.replace(suffix,'')
            # print(colors.green + 'New URL: ' + url + colors.reset)
        if '/' in user:
            user = user.replace('/','')
        if user != ''   :
            pwned_users.append(user)
   
    if last_name != '':
        print(colors.grey + f'Top results for {name}' + f' { last_name}:')
    else:
        print(colors.grey + f'Top results for {name}:')
        
    if len(pwned_users) == 0:
        print(colors.red + 'No Results found')
    new_pwned = []
    new_pwned = [new_pwned.append(x) for x in pwned_users if x not in new_pwned]
    for usr in pwned_users:
        if(command == '-scan'):
            print(colors.yellow + '    ' + usr + colors.reset)
            getUsernameInfo(usr)
        else:
            print(colors.green + '    ' + usr + colors.reset)

def getUsernameInfo(username):
     
    # getting the request from url
    response = requests.get(URL.format(username))
    if response.ok:
        # converting the text
        s = BeautifulSoup(response.text, 'html.parser')
        
        # finding meta info
        meta = s.find('meta', property ='og:description')
        if meta != None:
            text = meta.attrs['content']
            
            
            # splitting the content
            # then taking the first part
            text = text.split('-')[0]
            
            # again splitting the content
            text = text.split(' ')
            # return parse_data(meta.attrs['content'])
            
            print(colors.green + colors.italics + '      Followers: ' + text[0] + '\n      Following: ' + text[2] + '\n      Posts: ' + text[4] + colors.reset)
        else:
            print(colors.red + 'Unable to get instagram account name. Please make sure its valid and try again')
    else:
        print(colors.red + colors.italics + 'Error 429       Please try again later')

def getPhoto(username, command):
    # getting the request from url
    response = requests.get(URL.format(username))
    # converting the text
    soup = BeautifulSoup(response.text, 'html.parser')
    photo = soup.find_all('meta', attrs={'property': 'og:image'})
    photo_url = photo[0].get('content')
    
    parent_dir = 'pwned_users'
    user_dir = username

    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    
    if command == '-png':
        
            
        if not os.path.exists(parent_dir + f'\{username}'):
            os.mkdir(parent_dir + f'\{username}')
            
        if os.path.exists(parent_dir + f'\{username}\{username}.png'):
            os.remove(parent_dir + f'\{username}\{username}.png')
            
            
        img_file = username + '.png'
        urllib.request.urlretrieve(photo_url, img_file)
        shutil.move(img_file, parent_dir + f'\{username}')
        
        
    if command == '-jpg':

            
        if not os.path.exists(parent_dir + f'\{username}'):
            os.mkdir(parent_dir + f'\{username}')
            
        if os.path.exists(parent_dir + f'\{username}\{username}.jpg'):
            os.remove(parent_dir + f'\{username}\{username}.jpg')
           
            
        img_file = username + '.jpg'
        urllib.request.urlretrieve(photo_url, img_file)
        shutil.move(img_file, parent_dir + f'\{username}')
    if command == '-d':
        if os.path.exists(parent_dir + f'\{username}'):
            shutil.rmtree(parent_dir + f'\{username}')
        print(colors.green + 'Successfully downloaded to folder: pwned_users')

def getMedia(username):
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches


    def replace_all_bad_chars_in_url(url):
        return url.replace('&amp;', '&')
    
    opts = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    opts.add_argument(user_agent)

    opts.headless = False

    driver = webdriver.Chrome('./chromedriver.exe', options=opts)
 
    driver.get(f'https://www.instagram.com/{username}/?hl=en')
    
    # converting the text
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    # all_html = soup.text()
    # print(soup.prettify)
    page_html = str(soup)
    print(page_html)
    
    index = list(find_all(page_html, 'https://instagram')) # [0, 5, 10, 15]
    print(index)
    i=0
    for post_url in index:
        # shutil.move(img_file, parent_dir + f'\{username}')
        filter1 = replace_all_bad_chars_in_url(page_html[post_url: post_url + 361])
        filter2 = filter1.split('"')[0]
        filter3 = filter2.split(' ')[0]
        photo_url = filter3
        print(photo_url)
        
        
        img_file = username + str(i) + '.png'
        urllib.request.urlretrieve(photo_url, img_file)
            
        i+=1
    # print ("\n".join(set(tag['src'] for tag in tags)))
    