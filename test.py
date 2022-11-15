import json
import requests
import urllib.request
from bs4 import BeautifulSoup


def get_url(user_):
    url = f'https://www.instagram.com/{user_}/'
    response = requests.get(url)
    print(response.json())
    cont = BeautifulSoup(response, 'lxml')
    script = cont.body.script.text
    
    
    aaaaaa = script[21:len(script)-1]
    print(aaaaaa)
    data = json.loads(aaaaaa)
    
    new = json.dumps(data, indent=2, sort_keys=True)
    
    data2 = data['entry_data']
    data3 = str(data2['ProfilePage'])
    data4 = data3.split("'")
    
    
    while True:
        try:
            posi = data4.index('shortcode')+2
            pic_id = data4[posi]
            data4 = data4[posi:]
            url2 = f'https://www.instagram.com/p/{pic_id}/?taken-by={user_}'
            print(f'Downloading img: {pic_id}')
            download_image(url2)
        except:
            break
    

def download_image(url):
    response = requests.get(url).text
    cont = BeautifulSoup(response, 'lxml')
    head = cont.head
    filt1 = cont.find_all('meta')
    filt2 = str(filt1).split('"')
    url3 = filt2[37]
    download_final(url3)
    
def download_final(url):
    urllib.request.urlretrieve(url, 'test.png')
    
    
get_url('project__exodus')