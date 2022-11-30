"""
     _.-^^---....,,--       
 _--                  --_  
<                        >)
|                         | 
 \._                   _./  
    ```--. . , ; .--'''       
          | |   |             
       .-=||  | |=-.   
       `-=#$%&%$#=-'   
          | ;  :|     
 _____.,-#%&$@%#&#~,._____
"""
#This is the death of me


# getting all of them imports to make the code do its thing

import faceRecognize
import faceEncode
import os
import shutil
import requests
import tkinter
import urllib
from bs4 import BeautifulSoup
from Colors import colors
from datetime import datetime
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from tkinter import filedialog




    

def init():
    #---GENERATES A HIDDEN BROWSER THAT ALLOWS ME TO PULL ALL OF THE IMAGES OFF OF A PAGE. MUY IMPORTANTE!!!---#
    

    opts = webdriver.ChromeOptions()
    opts.headless = True
    opts.add_experimental_option('excludeSwitches', ['enable-logging'])


    global driver 
    driver = webdriver.Chrome('./chromedriver.exe', chrome_options=opts)
    delete_cache()

    #used for finding the webapage with the needed username    
    global link    
    link = 'https://www.instagram.com/{}/?hl=en'

    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

def delete_cache():
    #idk why this works but it allows me to bypass the login redirect so it stays
    #used to delete cache and cookies so you wont get flagged as often
    #however it does make it slow to start
    
    
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
            getStats(usr)
        else:
            print(colors.green + '    ' + usr + colors.reset)

def getStats(username):
     
    # getting the request from url
    response = requests.get(link.format(username))
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

            
            print(colors.green + colors.italics + '      Followers: ' + text[0] + '\n      Following: ' + text[2] + '\n      Posts: ' + text[4] + colors.reset)
        else:
            print(colors.red + 'Unable to get instagram account name. Please make sure its valid and try again')
    else:
        print(colors.red + colors.italics + 'Error 429       Please try again later')

def getPhoto(username):
    #finds all substrings in a string and returns their locations
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches
     
    #Used to make the originally pulled urls work again for downloading
    def replace_all_bad_chars_in_url(url):
        return url.replace('&amp;', '&')
    
    #generates the webpage while hidden and gets html/javascript code
    response = requests.get(link.format(username)) #used to get the proper error messages
    if driver.current_url != link.format(username):
        driver.get(link.format(username))
    
    #checks for good response code
    if response.status_code == 200:
        #parses the html for the later functions
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        new_html = str(soup)
        results = list(find_all(new_html, 'https://instagram'))
        


        
        #makes pwned_users and subsequent user directory folders
        parent_dir = 'pwned_users'
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)
        if not os.path.exists(parent_dir + f'\{username}'):
                os.mkdir(parent_dir + f'\{username}')



        post_ids=[]

        urls=[]
        #-------------------------GET POST IDS-------------------------#
        for post in results: 
            #all of the needed filters to get the needed content
            filter1 = replace_all_bad_chars_in_url(new_html[post: post + 361])
            filter2 = filter1.split('"')[0]
            filter3 = filter2.split(' ')[0]
            filter4 = str(filter3[54:100])
            
            
            #sets both of those to their proper filters
            photo_url = filter3
            photo_id = filter4
            
            
            urls.append(photo_url)      #photo url
            post_ids.append(photo_id)   #photo id
            
            
        #declares the needed size for the sorted array (no space goes unused)
        post_ids = list(dict.fromkeys(post_ids))
        sorted_urls = [[] for j in range(len(post_ids))]
        highest_res_urls = []

        #sorts all of the photos
        for i in range(len(post_ids)):
            for url in urls:
                if post_ids[i] in url:
                    sorted_urls[i].append(url)


        #chooses highest resoluion from each photo
        for i in range(len(sorted_urls)):
            for url in sorted_urls[i]:
                if '1024x1024' in url:
                    highest_res_urls.append(url)
                elif '640x640' in url:
                    highest_res_urls.append(url)
                elif '480x480' in url:
                    highest_res_urls.append(url)
                elif '320x320' in url:
                    highest_res_urls.append(url)
                elif '240x240' in url:
                    highest_res_urls.append(url)
                elif '150x150' in url:
                    highest_res_urls.append(url)
                else:
                    highest_res_urls.append(url)
                break

        
        #-------------------------DOWNLOAD HIGHEST-RES PHOTO FROM URL AND SETS FILE NAME AS USERNAME-------------------------#
        # if len(highest_res_urls) != 0
        # highest_res_urls.pop(0) #Removes profile picture from downloaded images (seperate function for that)
        if len(highest_res_urls) > 1: 

            profile_pic = highest_res_urls[0]

            if os.path.exists(parent_dir + f'\{username}\{username}.png'):
                os.remove(parent_dir + f'\{username}\{username}.png')
                
                
            img_file = username + '.png'
            urllib.request.urlretrieve(profile_pic, img_file)
            shutil.move(img_file, parent_dir + f'\{username}')
            print(colors.green + f'Successfully found profile picture of {username}' + colors.reset)

    #Checks for bad status code and gives proper error statement
    elif response.status_code == 429:
        print(colors.red + 'Error 429: Too many requests. Please try again a little later')    
    elif response.status_code == 404:
        print(colors.red + 'Error 404: Username does not exist')    
    elif response.status_code == 500:
        print(colors.red + 'Instagram server error')

def getPosts(username, attempt=1):
    #finds all substrings in a string and returns their locations
    def find_all(a_str, sub):
        start = 0
        while True:
            start = a_str.find(sub, start)
            if start == -1: return
            yield start
            start += len(sub) # use start += 1 to find overlapping matches
     
    #Used to make the originally pulled urls work again for downloading
    def replace_all_bad_chars_in_url(url):
        return url.replace('&amp;', '&')
    
    #generates the webpage while hidden and gets html/javascript code
    response = requests.get(link.format(username)) #used to get the proper error messages
    
    if driver.current_url != link.format(username):
        driver.get(link.format(username))
    
    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    #checks for good response code
    if response.status_code == 200:
        
        
        #parses the html for the later functions
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        new_html = str(soup)
        results = list(find_all(new_html, 'https://instagram'))
        

        
        #makes pwned_users and subsequent user directory folders
        parent_dir = 'pwned_users'
        if not os.path.exists(parent_dir):
            os.mkdir(parent_dir)
        if not os.path.exists(parent_dir + f'\{username}'):
                os.mkdir(parent_dir + f'\{username}')



        post_ids=[]

        urls=[]
#-------------------------GET POST IDS-------------------------#
        for post in results: 
            #all of the needed filters to get the needed content
            filter1 = replace_all_bad_chars_in_url(new_html[post: post + 361])
            filter2 = filter1.split('"')[0]
            filter3 = filter2.split(' ')[0]
            filter4 = str(filter3[54:100])
            
            
            #sets both of those to their proper filters
            photo_url = filter3
            photo_id = filter4
            
            
            urls.append(photo_url)      #photo url
            post_ids.append(photo_id)   #photo id
            
            
        #declares the needed size for the sorted array (no space goes unused)
        post_ids = list(dict.fromkeys(post_ids))
        sorted_urls = [[] for j in range(len(post_ids))]
        highest_res_urls = []

        #sorts all of the photos
        for i in range(len(post_ids)):
            for url in urls:
                if post_ids[i] in url:
                    sorted_urls[i].append(url)


        #chooses highest resoluion from each photo
        for i in range(len(sorted_urls)):
            for url in sorted_urls[i]:
                if '1024x1024' in url:
                    highest_res_urls.append(url)
                elif '640x640' in url:
                    highest_res_urls.append(url)
                elif '480x480' in url:
                    highest_res_urls.append(url)
                elif '320x320' in url:
                    highest_res_urls.append(url)
                elif '240x240' in url:
                    highest_res_urls.append(url)
                elif '150x150' in url:
                    highest_res_urls.append(url)
                else:
                    highest_res_urls.append(url)
                break

        
        #-------------------------DOWNLOAD HIGHEST-RES PHOTO FROM URL AND SETS CURRENT TIME AS THE NAME-------------------------#
        # if len(highest_res_urls) != 0
        if len(highest_res_urls) > 1: 
            highest_res_urls.pop(0) #Removes profile picture from downloaded images (seperate function for that)
            for photo_url in highest_res_urls:
                time = str(datetime.now().time())
                
                time = time.replace(':', '-')
                time = time.replace('.', '-')
                
                img_file = username + str(time) + '.png'
                urllib.request.urlretrieve(photo_url, img_file)
                shutil.move(img_file, parent_dir + f'\{username}')
            num_of_posts = len(highest_res_urls)
            print(colors.green + f'Successfully found {num_of_posts} posts from {username}' + colors.reset)
        else:
            if 'https://www.instagram.com/accounts/login/?next=' in driver.current_url and attempt < 5:
                print(colors.red + f'Redirected to login screen. Trying again (Attempt {attempt}/5)')
                attempt+=1
                getPosts(username, attempt)
                
            # else:
            #     print(colors.red + 'Private Account' + colors.reset)
    #Checks for bad status code and gives proper error statement
    elif response.status_code == 429:
        print(colors.red + 'Error 429: Too many requests. Please try again a little later' + colors.reset)    
    elif response.status_code == 404:
        print(colors.red + 'Error 404: Username does not exist' + colors.reset)    
    elif response.status_code == 500:
        print(colors.red + 'Instagram server error' + colors.reset)
    
def comparePhotosAndPosts(username):
    print(colors.grey + 'Please select image containing the face that you would like to compare:' + colors.reset)
    file = filedialog.askopenfile()
    
    parent_dir = 'pwned_users'
    username_dir = f'{parent_dir}\{username}'
    
    if file: 
        faceEncode.encodeFace(file.name, username)
    
    # file2 = filedialog.askopenfile()
    
    faceRecognize.findFace(username_dir)
    
def deleteTargetData(username):
    parent_dir = 'pwned_users'
    
    if os.path.exists(parent_dir + f'\{username}'):
            shutil.rmtree(parent_dir + f'\{username}')
            print(colors.red + f'Successfully deleted {username}')

def deleteAllTargetsInfo():
    parent_dir = r'pwned_users\\'
    
    all_user_dirs = os.listdir(parent_dir)
    
    for directory in all_user_dirs:
        shutil.rmtree(parent_dir + directory)
    
    print(colors.red + f'Successfully deleted all targets')