from selenium import webdriver
import time
import pandas as pd
import math

# 웹 드라이버 실행
driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe')
driver2 = webdriver.Chrome('./chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(time_to_wait=5)
driver2.implicitly_wait(time_to_wait=5)

url = "https://www.tripadvisor.com/Attractions-g187070-Activities-a_allAttractions.true-France.html"
driver.get(url)

France = pd.DataFrame()

attractions = driver.find_elements_by_css_selector('header > div > div > a:nth-child(1)')

for attraction in attractions:
    print("Count:", len(France))
    attraction_url = attraction.get_attribute('href')
    driver2.get(attraction_url)
    time.sleep(3)

    attraction_name = driver2.find_elements_by_css_selector('h1')[1].text  # 관광지명
    rating = driver2.find_elements_by_css_selector('div.WlYyy.cPsXC.fksET.cMKSg')[0].text  # 전체 평점

    # DataFrame 저장
    attraction = {'attraction':attraction_name, 'score':rating}
    France = France.append(attraction, ignore_index=True)  
        
    review_count = int(driver2.find_element_by_css_selector('div.cIUfa.Ci').text.split()[-1].replace(',', ''))
    
    # 리뷰 수에 따른 페이지 범위 설정
    for i in range(math.floor(review_count / 10)):
        # 리뷰 가져오기
        reviews = driver2.find_elements_by_css_selector('div.bPhtn > div')
        for review in reviews[:-1]:
            try:   
                rating = review.find_element_by_css_selector('div:nth-child(3) > svg').get_attribute('title').split()[0]  # 개인 평점
                title = review.find_element_by_css_selector('div.WlYyy.cPsXC.bLFSo.cspKb.dTqpp').text  # 리뷰 제목
                content = review.find_element_by_css_selector('div.duhwe._T.bOlcm').text  # 리뷰 내용
                trip_date = review.find_element_by_class_name('fEDvV').text.split(' • ')[0]  # 여행 날짜

                # DataFrame 저장
                attraction = {'attraction':attraction_name, 'score':rating, 'title':title, 'review':content, 'trip_date':trip_date}
                France = France.append(attraction, ignore_index=True)
            except Exception as ex:
                print('ERROR!', ex)
                pass
        
        # 최대 1000개까지만 가져옴
        if i == 99:
            break

        # 다음 페이지로 이동
        next_page = driver2.find_element_by_css_selector('div.cCnaz > div > a').get_attribute('href')
        driver2.get(next_page)
        time.sleep(3)