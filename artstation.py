from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
import re
import time
import json

# driver = webdriver.Chrome()
driver = webdriver.Remote("http://localhost:4446/wd/hub", desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
page = 0
all_link = []
get_down_link = []
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36'}
#while page <= 3:
# 打开第一页的trending页面，while page可设定打开几页
url = 'https://www.artstation.com/projects.json?page=0&sorting=trending'#%d%page
req = urllib.request.Request(url,headers= headers)
webpage = urllib.request.urlopen(req).read()
picks = json.loads(webpage)

author_page = picks['data']
# ['permalink']
# trending页面获取作者链接
for author_get_link in author_page:
        # print(author_get_link['permalink'])
    all_link.append(author_get_link['permalink'])
    #page += 1 配合while page增加页面
num_for_all_link = str(len(all_link))
print('Get author number is %s'%num_for_all_link)
#作者链接里获取下载地址
for j in all_link:
    driver.get(j)
    soup_1 = BeautifulSoup(driver.page_source,'lxml')
    soup_img = soup_1.find_all('div',class_='artwork-image')

    for a in soup_img:
        find_url = a.find('img')
        get_url = find_url.get('ng-src')
        get_down_link.append(get_url)
#        print(get_url)
#        不显示获取的下载链接
    time.sleep(5)
num_for_get_down_link = str(len(get_down_link))
print('Get %s Pictures links'%num_for_get_down_link)
file_name = []#获得需要的文件名
for down in get_down_link:
    # print(down)
    down = re.findall(r'[a-zA-z]*://cdn\w.artstation.com/p/assets/images/images/+\d+/\d+/\d+/large/+(.*.jpg)+.*',down)
    print('********************************')
    if down:
        # print(down[0])
        file_name.append(down[0])
# print(file_name)
time.sleep(5)
    #下载
n = 1
for f_name,d_link in zip(file_name,get_down_link):
    print('\r'+'Downloading %s now'%f_name,end='')
    #\r清除当前行,end=''不换行print
    print('\r'+'Progress %s/%s'%(n,num_for_get_down_link),end='')
    data = urllib.request.Request(d_link,headers= headers)
    pic= urllib.request.urlopen(data).read()
    file = open('c:/artstation/%s'%f_name,'wb')
    file.write(pic)
    file.close()
    n += 1
    time.sleep(1)




# pic_down_link(all_link)
