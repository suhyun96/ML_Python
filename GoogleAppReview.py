# -*- coding: utf-8 -*-

from selenium import webdriver
import time
import pyautogui as pya
import datetime 
import pandas as pd
import keyboard

#장치가 제대로 사용 못하는 오류를 막기 위해
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

#수집하려는 url 
url="https://play.google.com/store/apps/details?id=com.truefriend.neosmarta&showAllReviews=true"
driverPath = "./chromedriver.exe" # Chrome Driver path 
driver.get(url) 

#리뷰 전체 보기 위해 클릭 
tmp = driver.find_element_by_xpath("//*[text() = '리뷰 모두 보기']")
tmp.click()

# 로딩 위해 기다리고 해당 팝업창 활성화 위해 클릭 1번 
time.sleep(1)
#제목쪽 클릭도 안 됨 
pya.click(1002,667)
# print(pya.position()) 해당 함수로 마우스 위치 확인하기 


# 스크롤 끝까지 내리기 위한 함수 
# 일정 시간동안 무한 스크롤 
def scroll_down(second):
    # 시작시간과 끝나는 시간 계산
    start = datetime.datetime.now()
    end = start + datetime.timedelta(seconds=second)

    i=0
    
    while True:

        #긴급 탈출용 
        if keyboard.is_pressed('ctrl'):
            break # while문 탈출

        i=i+1
        pya.press('space', presses=5)
        # 로딩 위해 1번씩 쉬어가자         
        if(i%10==0):
            time.sleep(0.7)
            print("쉬어갑니다")
        
        pya.click()
        print(i)
        if datetime.datetime.now() > end:
            break

# 시간 넣어주기 
scroll_down(100)


#### 문장 처리 ##### 

# 리뷰 내용 
reviews = driver.find_elements_by_xpath("//div[@class='h3YV2d']")
# 시간 날짜
dates = driver.find_elements_by_xpath("//span[@class='bp9Aid']")
# 좋아요 수 -> 이건 보류 없는 경우가 있어서 배열 범위 벗어남 
likes = driver.find_elements_by_xpath("//div[@class='AJTPZc']")

stars = driver.find_elements_by_xpath("//div[@class='Jx4nYe']/div[@role='img']")

res_dict = [] 
for i in range(len(reviews)): 
    res_dict.append({ 
        'DATE' : dates[i].text, 
        'STAR' : stars[i].get_attribute('aria-label'), 
        #'LIKE' : likes[i].text, 이게 도움이 되는게 있고 안 되는게 있어서 빼야 할듯.. 
        'REVIEW' : reviews[i].text }) 
res_df = pd.DataFrame(res_dict) 
res_df.to_csv('./Crawling_data5.csv', index=False, encoding='utf-8-sig')










