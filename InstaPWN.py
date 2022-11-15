# importing libraries
import asyncio
import json
import lxml
import os
import pandas as pd
import shutil
import re
import requests
import urllib
from bs4 import BeautifulSoup
from Colors import colors
from googlesearch import search
from pyppeteer import launch    

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
    response = requests.get(URL.format(username))
    # converting the text
    soup = BeautifulSoup(response.text, 'html.parser')
    # photo = soup.find_all('img', alt=True)
    # print(photo)
    # photo_url = photo[0].get('content')
    tags = {tag.name for tag in soup.find_all()}
    class_list = set()

    # iterate all tags
    for tag in tags:
    
        # find all element of tag
        for i in soup.find_all( tag ):
    
            # if tag has attribute of class
            if i.has_attr('img'):
    
                if len( i['img'] ) != 0:
                    class_list.add(" ".join( i['img']))
    
    print( class_list )
    
    
    
    
    
    

    
    
    
    
    
    
async def get_html(username):
    # browser = await launch({"headless": False, "args": ["--start-maximized"]})
    browser = await launch()
    page = await browser.newPage()
    await page.goto(URL.format(username), {'waitUntil' : ['load', 'domcontentloaded', 'networkidle0']})
    html = await page.content()
    await browser.close()
    return html
