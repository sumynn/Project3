from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# 웹 드라이버 실행
driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe')

url = "https://www.tripadvisor.com/Attractions-g187070-Activities-a_allAttractions.true-France.html"
driver.get(url)

driver.implicitly_wait(time_to_wait=5)

France = pd.DataFrame()

for i in range(29):
    driver.find_elements_by_css_selector('header > div > div > a:nth-child(1)')[i].click()
    time.sleep(5)
    driver.switch_to_window(driver.window_handles[1])

    attraction_name = driver.find_elements_by_css_selector('h1')[1].text  # 관광지명
    rating = driver.find_elements_by_css_selector('div.WlYyy.cPsXC.fksET.cMKSg')[0].text  # 전체 평점

    # DataFrame 저장
    attraction = {'attraction':attraction_name, 'score':rating}
    France = France.append(attraction, ignore_index=True)  

    for i in range(100):
        try:              
            # 리뷰 가져오기
            reviews = driver.find_elements_by_css_selector('div.bPhtn > div')
            for review in reviews[:-1]:
                rating = review.find_element_by_css_selector('div:nth-child(3) > svg').get_attribute('title').split()[0]  # 개인 평점
                title = review.find_element_by_css_selector('div.WlYyy.cPsXC.bLFSo.cspKb.dTqpp').text  # 리뷰 제목
                content = review.find_elements_by_css_selector('div.duhwe._T.bOlcm')[0].text  # 리뷰 내용
                trip_date = review.find_element_by_class_name('fEDvV').text.split('•')[0].strip()  # 여행 날짜

                # DataFrame 저장
                attraction = {'attraction':attraction_name, 'score':rating, 'title':title, 'review':content, 'trip_date':trip_date}
                France = France.append(attraction, ignore_index=True)

            # 다음 페이지로 이동
            driver.find_element_by_xpath('//*[@id="tab-data-qa-reviews-0"]/div/div[5]/div[11]/div[1]/div/div[1]/div[2]/div/a').send_keys(Keys.ENTER)
            time.sleep(5)
        except:
            continue

    driver.close()
    driver.switch_to_window(driver.window_handles[0])