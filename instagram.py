from bs4 import BeautifulSoup
from time import sleep
import selenium.webdriver as webdriver
import urllib.parse
import pandas_csv

search = input("검색어입력:" )
searching = str(search)
search = urllib.parse.quote(search)
url = 'https://www.instagram.com/explore/tags/'+searching+'/'
driver = webdriver.Chrome('/Users/jaeb/Downloads/chromedriver')

driver.get(url)
sleep(3)

SCROLL_PAUSE_TIME = 1.2

reallink = []

while True:
    pageString = driver.page_source
    bs = BeautifulSoup(pageString, 'lxml')

# 게시물 정보
    for link1 in bs.find_all(name='div', attrs={"class":"Nnq7C weEfm"}):
        title = link1.select('a')[0]
        real = title.attrs['href']
        reallink.append(real)
        title = link1.select('a')[1]
        real = title.attrs['href']
        reallink.append(real)

# 페이지 스크롤
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        else:
            last_height = new_height
            continue

# print(reallink)

hashtag2 = []

reallinknum = len(reallink)
print("total: " + str(reallinknum))

#반복문 시작
try:
    for i in range(0, 20):
        hashtag2.append([])
        req = 'https://www.instagram.com/p'+reallink[i]
        driver.get(req)
        webpage = driver.page_source
        print('webPage: ', webpage)
        soup = BeautifulSoup(webpage, 'html.parser')
        print('soup: ', soup)
        soup1 = str(soup.find_all(attrs={'class': 'e1e1d'}))
        print('soup1:', soup1)
        user_id = soup1.split('href="/')[1].split('/">')[0]
        print(user_id)
        soup1 = str(soup.find_all(attrs={'class':'Nm9Fw'}))
        subValue = 'span'
        if(soup1 == "[]"): # 좋아요가 n개일 경우 코드가 다 다름
            likes = '0'
        elif(soup1.find(subValue) == -1):
            likes = soup1.split('좋아요 ')[1].split('개')[0]
        elif(soup1.find(subValue) != -1):
            likes = soup1.split('<span>')[1].split('</span>')[0]

        soup1 = str(soup.find_all(attrs={'class' : 'xil3i'}))
        if(soup1 == "[]"):
            hashtags = '해쉬태그없음'
            insert_data = {
                "search":searching,
                "usesr_id":user_id,
                "좋아요":likes,
                "hashtags":hashtags
            }
            pandas_csv.to_csv(insert_data)
        else:
            soup2 = soup1.split(',')
            soup2num = len(soup2)
            for j in range(0, soup2num):
                hashtags = soup2[j].split('#')[1].split('</a>')[0]
                print(hashtags)
                insert_data = {
                    "search":searching,
                    "user_id":user_id,
                    "좋아요":likes,
                    "hashtags":hashtags
                }
                pandas_csv.to_csv(insert_data)

except Exception as e:
    print("cause: ", e)
    print("에러: " + str(i+1)+"개의 데이터를 저장합니다.")
    pandas_csv.to_csv(insert_data)

