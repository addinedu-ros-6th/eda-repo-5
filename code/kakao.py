from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.mouse_button import MouseButton
from selenium.webdriver import ActionChains
import pandas as pd
import pandas as pd
import time

driver = webdriver.Chrome()
driver.get('https://map.kakao.com/')
driver.implicitly_wait(3)

selenium_data = []
def collect_data():
    place_list = driver.find_element(By.ID, "info.search.place.list").find_elements(By.TAG_NAME, "li")
    place_list_len = len(driver.find_element(By.ID, "info.search.place.list").find_elements(By.TAG_NAME, "li"))
    for j in range(place_list_len):
        print(j)
        tmp = []
        ratings_reviews = ratings_reviews = driver.find_element(By.CLASS_NAME, "placelist").find_elements(By.CLASS_NAME, "rating.clickArea")[j].text.split('\n')
        name = driver.find_elements(By.CLASS_NAME, "tit_name")[j].text[2:] #상호
        address = driver.find_elements(By.CLASS_NAME, "addr")[j].text.split('\n')[0] #주소
        category = driver.find_elements(By.CLASS_NAME, "subcategory.clickable")[j].text #카테고리
        gu = driver.find_elements(By.CLASS_NAME, "addr")[0].text.split(' ')[1] #구
        #별점 미제공 식당
        if len(ratings_reviews) == 2:
            ratings = '미제공' #별점
            reviews = ratings_reviews[1][3:] #리뷰
        else:
            ratings = ratings_reviews[0] #별점
            reviews = ratings_reviews[2][3:] #리뷰
        tmp.append(name)
        tmp.append(ratings)
        tmp.append(reviews)
        tmp.append(address)
        tmp.append(category)
        tmp.append(gu)
        selenium_data.append(tmp)

def next_btn(driver):
    no2 = driver.find_element(By.ID,'info.search.page.no2')
    no2.click()
    time.sleep(0.1)
    collect_data()
    #driver.implicitly_wait(3) # 필요할 경우 time.sleep(0.5) 대체(실행시간이 더 빠름)
    no3 = driver.find_element(By.ID,'info.search.page.no3')
    no3.click()
    time.sleep(0.1)
    collect_data()
    no4 = driver.find_element(By.ID,'info.search.page.no4')
    no4.click()
    time.sleep(0.1)
    collect_data()
    no5 = driver.find_element(By.ID,'info.search.page.no5')
    no5.click()
    time.sleep(0.1)
    collect_data()
    no_next = driver.find_element(By.ID,'info.search.page.next')
    no_next.click()
    time.sleep(0.1)

seoul_districts = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']
celenium_data = []
#작동 안 될시 카카오맵 검색창 클릭
#ㅇㅇ구 맛집 검색
for i in seoul_districts:
    restaurant = i + ' 맛집'
    driver.find_element(By.XPATH, """//*[@id="search.keyword.query"]""").click()
    time.sleep(0.3)
    driver.find_element(By.XPATH, """//*[@id="search.keyword.query"]""").click()
    driver.find_element(By.XPATH, """//*[@id="search.keyword.query"]""").send_keys(restaurant)
    driver.find_element(By.XPATH, """//*[@id="search.keyword.submit"]""").send_keys(Keys.ENTER)
    place_list = driver.find_element(By.ID, "info.search.place.list").find_elements(By.TAG_NAME, "li")
    place_list_len = len(driver.find_element(By.ID, "info.search.place.list").find_elements(By.TAG_NAME, "li"))
    tag = driver.find_element(By.ID,'info.search.place.more')
    tag.click()
    driver.find_element(By.ID,'info.search.page.no1').click()
    #식당 정보 수집
    have_btn = True
    while have_btn:
        try:
            next_btn(driver)
        except Exception as e:
            print('검색 완료')
            have_btn = False
            break
    driver.find_element(By.XPATH, """//*[@id="local"]""").click()

driver.close()

df = pd.DataFrame(celenium_data, columns= ['구', '이름', '카테고리', '별점', '리뷰수', '주소'])
