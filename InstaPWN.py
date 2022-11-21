# importing libraries

import os
import pandas as pd
import shutil
import requests
import urllib
from bs4 import BeautifulSoup
from Colors import colors
from googlesearch import search
from selenium import webdriver


from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
    
opts = webdriver.ChromeOptions()

opts.headless = True
opts.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)

URL = 'https://www.instagram.com/{}/?hl=en'


def delete_cache():
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get('chrome://settings/clearBrowserData') # for old chromedriver versions use cleardriverData
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 3 + Keys.DOWN * 3) # send right combination
    actions.perform()
    actions = ActionChains(driver) 
    actions.send_keys(Keys.TAB * 4 + Keys.ENTER) # confirm
    actions.perform()
    driver.close() # close this tab
    driver.switch_to.window(driver.window_handles[0]) # switch back






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
    
    #gets all image urls
    driver.get(URL.format(username))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    new_html = str(soup)
    results = list(find_all(new_html, 'https://instagram'))



    i = 0
    post_ids=[]
    new_urls=[]
    
    for posts_url in results:
        filter1 = replace_all_bad_chars_in_url(new_html[posts_url: posts_url + 361])
        filter2 = filter1.split('"')[0]
        filter3 = filter2.split(' ')[0]
        filter4 = str(filter3[54:96])
        
        new_urls.append(filter3)#get photo url

        post_ids.append(filter4)#get photo id
        
    post_id_filter = []
    [post_id_filter.append(x) for x in post_ids if x not in post_id_filter]

    post_ids = post_id_filter
    
    
    
    
    sorted_urls = [[]]*len(post_ids)
    
    print(sorted_urls)
    print(len(new_urls))
    
    n = 0
    for i in range(len(post_ids)-1):
        for url in new_urls:
            if post_ids[i] in url:
                sorted_urls[i].append(url)

        # n+=1

    for i in sorted_urls:
        print(i)
        print('\n')
                
                
    
    
    # parent_dir = 'pwned_users'
    # user_dir = username

    # if not os.path.exists(parent_dir):
    #     os.mkdir(parent_dir)
    
    # num = 0
    # for url in sorted_urls:
    #     # print(url)
    #     # print('\n')
    #     if not os.path.exists(parent_dir + f'\{username}'):
    #         os.mkdir(parent_dir + f'\{username}')
        
    #     for photoUrl in url:
    #         img_file = username + str(num) + '.png'
    #         urllib.request.urlretrieve(photoUrl, img_file)
    #         shutil.move(img_file, parent_dir + f'\{username}')
    #         num+=1