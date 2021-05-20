#!/usr/bin/env python
# coding: utf-8

# In[4]:


# 라이브러리 선언
from selenium import webdriver    # 셀레니움
import pandas as pd
import time
import requests 
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

# 드라이버 옵션 설정
options = webdriver.ChromeOptions()  
options.add_argument("window-size=1920x1080")

# 드라이버 위치 설정
driverLoc = "./addon/chromedriver/chromedriver.exe"
driver = webdriver.Chrome(driverLoc, options=options)
options.add_argument("window-size=1920x1080")

# 브라우저 팝업 (벅스뮤직)
targetUrl = "https://music.bugs.co.kr/"
driver.get(targetUrl)
time.sleep(3)

# 차트탭 클릭하여 이동
xpathChart = '//*[@id="gnbBody"]/div/div[1]/nav/ul/li[1]/a'
chartBtn = driver.find_element_by_xpath(xpathChart)
chartBtn.click()
time.sleep(3)    # 정보를 잘 못가져와서 3초기다리게 함.

# 현재 있는 페이지 정보 가져오기.
finalUrl = driver.current_url
pgSource = driver.page_source

# 헤더 변경 나는 크롤러가 아니라 매킨토시 mac으로 접근하고 있으니 차단하지 말아줘~ 라는 느낌임
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:71.0) Gecko/20100101 Firefox/71.0'}

# URL 접속
resp = requests.get(url=finalUrl, headers = headers)
if resp.status_code == 200:
    resp.encoding = "utf-8"
    html = resp.text
    htmlObj = BeautifulSoup(html, "html.parser")
else:
    print("다시 URL 확인해봐~")

# 정보 가져오기
# 순위
rankDivTags = htmlObj.find_all("div", class_="ranking")
# 제목
titlePTags = htmlObj.find_all("p", class_='title')
# 가수
artistPTags = htmlObj.find_all("p", class_='artist')

# 리스트 생성
rankList = []
titleList = []
artistList = []

for i in range (len(rankDivTags)):
    rank = rankDivTags[i].find("strong").text
    title = titlePTags[i].find("a").text
    artist = artistPTags[i].find("a").text
    
    rankList.append(rank)
    titleList.append(title)
    artistList.append(artist)

bugsChart = pd.DataFrame( zip(rankList, titleList, artistList), columns=["순위", "제목", "가수"])
bugsChart = bugsChart.set_index("순위")
# bugsChart.to_csv("../dataset/bugsChart.csv", encoding="utf-8", index=False)  # utf-8로 인코딩해도 엑셀에서 한글이 깨집니다. (메모장은 됨) 교수님께 질문!
bugsChart


# In[ ]:




