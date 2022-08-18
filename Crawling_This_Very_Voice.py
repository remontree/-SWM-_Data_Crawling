import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import pyautogui
import time

chromedriver_autoinstaller.install() 
driver = webdriver.Chrome()

num=1

for i in range(1,68):
    print("Page"+str(i))
    url = "https://m.fss.or.kr:4434/phishingkeeper/board/boardList.do?page={}&bbsId=1436425918273&mId=M045202000000".format(i)
    driver.get(url)
    html = driver.page_source
    html = BeautifulSoup(html,'html.parser')
    for name in html.select("section #board-Content"):
        for li in name.select("ul.board-list li a"):
            sub_url = "https://m.fss.or.kr:4434/phishingkeeper/board/"+li["href"]
            response = urlopen(sub_url)
            response = BeautifulSoup(response,'html.parser')
            file_name  = None
            check = ['\\','/',':',"*","?","\"","<",">","|"]
            for file in response.select("section.board-Title h3"):
                file_name=file.get_text()
                for c in check:
                    if c in file_name:
                        file_name=file_name.replace(c,"")
            print("파일 다운로드 중: "+file_name)
            for name2 in response.select("section.board-Attach"):
                for link in name2.select("ul li audio source"):
                    URL = link["src"]
                    response = requests.get(URL)
                    open(str(num)+"."+file_name+".mp3", "wb").write(response.content)
                    num+=1
                    time.sleep(3)
