import urllib.request,urllib.error
import datetime
import re
import os.path
from selenium import webdriver
import time

big_path=r'C:\Users\lenovo\Desktop\xvideos\\'


def save_file(this_download_url,title):
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    time1=datetime.datetime.now()
    video_name = title
    path = os.path.join(big_path,video_name)
    print (str(time1)[:-7])
    if (os.path.isfile(path)):
        file_size=os.path.getsize(path)/1024/1024
        print ("File %s(%sMb)already exists " %(path,str(file_size)))
        return 1
    else:
        print ("Downloading %s"%(path))
        print("下载地址为://%s"%(this_download_url))
        f = urllib.request.urlopen(this_download_url)
        data = f.read()
        print ("path:%s"%(path))
        with open(path, "wb") as code:
            print ("loading")
            code.write(data)
        time2=datetime.datetime.now()
        print (str(time2)[:-7])
        print ("%s Done."%(path))
        use_time=time2-time1
        print ("Time used: %s"%(str(use_time)[:-7]))
        file_size=os.path.getsize(path)/1024/1024
        print ("File size: %s MB, Speed: %sMB/s"%( str(file_size),str(file_size/(use_time.total_seconds()))[:4]))

def download_the_av(url):
    req = urllib.request.Request(url)
    content = urllib.request.urlopen(req).read()
    content = content.decode('utf-8')
#    小于一百默认失败
    while len(content)<100:
        print("try again...")
        content = urllib.request.urlopen(req).read()
        content = content.decode('utf-8')
    print( "All length:%s" %(str(len(content))))
    titleRe = "setVideoTitle\(\'(.+?)\'\);"
    lowUrlRe = "setVideoUrlLow\(\'(.+?)\'\);"
    patternTitle = re.compile(titleRe)

    patternLowUrl = re.compile(lowUrlRe)
    to_find = content
    
    matchTitle = patternTitle.search(to_find)
    matchLowUrl = patternLowUrl.search(to_find)
    if matchTitle:
        title = matchTitle.group(1)+".mp4"
        print (title)

    if matchLowUrl:
        lowUrl = matchLowUrl.group(1)
        print (lowUrl)
    if len(lowUrl)>0:
        save_file(lowUrl,title)


pages=set()
def getUrls(start_url):
    browser = webdriver.Chrome()
    browser.get(start_url)
    # 通过css选择器查找
    urls = browser.find_elements_by_css_selector('.thumb a')
    
    global pages
    
    for x in urls:
        url = x.get_attribute('href')
        if url not in pages:
    #        新页面
            print(url)
            pages.add(url)
        else:
            print("已经下载过")
    time.sleep(5)
    browser.quit()
    
    

#-----------------------入口-------------------------------
getUrls("https://www.xvideos.com/video10079107/baby_")    
#print(pages)
for page_url in pages:
    getUrls(page_url)
    if(len(pages)>40):
        print("---------------------------------------开始下载-----------------------------------")
        break

for url in pages:
    download_the_av(url)