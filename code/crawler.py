from selenium import webdriver
import time
import pandas as pd
import json
import pymongo
from tqdm.notebook import tqdm

# 웹 드라이버 실행
driver = webdriver.Chrome('./chromedriver_win32/chromedriver.exe')
driver2 = webdriver.Chrome('./chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(time_to_wait=5)
driver2.implicitly_wait(time_to_wait=5)


# # MongoDB 연결
client = pymongo.MongoClient("mongodb+srv://dbUser:0000@cluster0.89n32.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client['review_data']
col = db['tripadvisor']

# country url
with open("countryURL.json", "r") as f:
    urls = json.load(f)

for country, url in tqdm(urls.items(), desc="Country"):
    driver.get(url)

    # df = pd.DataFrame()

    # attractions list
    attractions = driver.find_elements_by_css_selector('header > div > div > a:nth-child(1)')
    attraction_count = 1  # attraction 개수

    for attraction in attractions:
        attraction_url = attraction.get_attribute('href')
        driver2.get(attraction_url)
        time.sleep(3)

        attraction_name = driver2.find_elements_by_css_selector('h1')[1].text  # 관광지명

        # # 전체 평점
        # rating = driver2.find_elements_by_css_selector('div.WlYyy.cPsXC.fksET.cMKSg')[0].text  
        # data = {'country':country, 'attraction':attraction_name, 'score':rating}
        # df = df.append(data, ignore_index=True)  

        review_count = 0  # 리뷰 개수
        flag = False

        while True:
            # 리뷰 가져오기
            reviews = driver2.find_elements_by_css_selector('div.bPhtn > div')
            
            if len(reviews) == 0:
                attraction_count -= 1
                break              
            
            for review in reviews[:-1]:
                try:
                    writing_date = review.find_element_by_class_name('WlYyy.diXIH.cspKb.bQCoY')  # 작성 날짜
                    
                    # 작성 날짜가 2021년인 것만 추출
                    if writing_date.text.split()[-1] == '2021':  
                        score = review.find_element_by_css_selector('div:nth-child(3) > svg').get_attribute('title').split()[0]  # 개인 평점
                        #title = review.find_element_by_css_selector('div.WlYyy.cPsXC.bLFSo.cspKb.dTqpp').text  # 리뷰 제목
                        content = review.find_element_by_css_selector('div.duhwe._T.bOlcm').text  # 리뷰 내용
                        trip_date = review.find_element_by_class_name('fEDvV').text.split(' • ')[0]  # 여행 날짜'

                        # 여행 날짜가 2021년이 아니면 제외
                        if trip_date.split()[-1] != '2021':  
                            continue

                        # MongoDB에 저장
                        data = {'country':country, 'attraction':attraction_name, 'score':float(score), 'review':content, 'trip_date':trip_date}
                        # df = df.append(data, ignore_index=True)
                        # df = df[['country', 'attraction', 'score', 'review', 'trip_date']]
                        col.insert_one(data)
                        review_count += 1
                        
                        print(f'\rAttraction{attraction_count} Review Count:', review_count, end='')
                        #col.insert_one(data)
                        #pbar.update(1)
                    else:
                        flag = True
                        break
                except Exception as ex:
                    #print('ERROR!', ex)
                    pass
            if flag:
                break    

            # 다음 페이지로 이동
            try:
                next_page = driver2.find_element_by_css_selector('div.cCnaz > div > a').get_attribute('href')
                driver2.get(next_page)
                time.sleep(3)  
            except:
                pass
        
        
        # attaction 10개 가져오면 종료
        attraction_count += 1
        if attraction_count == 11:
            break

    # df.to_csv(f'./data/{country}.csv', index=False)