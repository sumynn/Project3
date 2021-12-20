# 유럽 국가별 감정 분석을 통한 여행 추천 지수 서비스

> 📅 2021.10.21 - 2021.12.03 (6주)
>
> 👨‍👦‍👦 3인

<br>

## 📑 Index

1. [프로젝트 개요](#-프로젝트-개요)
2. [기술 스택 및 라이브러리](#-기술-스택-및-라이브러리)
3. [프로젝트 수행 내용](#-프로젝트-수행-내용)
4. [담당한 기능](#-담당한-기능)
5. [배운 점](#-배운-점)

<br>

## 📖 프로젝트 개요

여행 플랫폼 Tripadvisor에서 수집한 유럽 국가별 관광 명소에 대한 평점과 리뷰의 자연어 분석을 통해 해당 여행지에 대한 추천 지수를 산출해 유럽 국가로의 여행에 대한 정량적인 정보를 제공해주고자 한다.

<br>

## 🛠 기술 스택 및 라이브러리

- Python3
- AWS
- 데이터 수집
  - Selenium
  - MongoDB
- EDA 및 모델링
  - VADER 감성 분석
- 웹 페이지 구현
  - MySQL
  - Django

<br>

## 📝 프로젝트 수행 내용

1. 데이터 수집
   - 여행지 리뷰
   - 코로나 현황
2. 전처리 및 EDA
   - 자연어 처리, 분석
3. 모델링
   - 긍부정 점수 산출
4. 웹 페이지 구현
   - 추천 지수 시각화

<br>

## 😎 담당한 기능

**데이터 수집**

- `Selenium`을 사용해 Tripadvisor의 여행지 리뷰 크롤링 후 **MongoDB** 적재

  > [Tripadvisor 크롤링 코드](TripadvisorCrawler.ipynb)

  - 리뷰 작성자 id, 개인 평점, 리뷰 제목, 리뷰 내용, 여행 날짜 등 추출

    <br>

- 코로나 현황

  > [코로나 현황 데이터 수집 코드](covid.py)

  - 확진자 현황

    - [API](https://github.com/disease-sh/API)를 사용해 [Worldometer](https://www.worldometers.info/coronavirus/)의 데이터 추출 후 **MySQL** 적재
    - 업데이트 날짜, 누적 확진자, 신규 확진자, 100만명당 확진자 등 추출

  - 백신 접종 현황

    - [OWID GitHub](https://github.com/owid/covid-19-data)에 매일 업데이트 되는 백신 접종 데이터 추출 후 MySQL 적재

    - 업데이트 날짜, 1차 접종자 수, 접종 완료자 수, 1차 접종률, 접종 완료율 등 추출

      <br>

- MySQL DB 백업

  [db_backup.sh](db_backup.sh)

  ```sh
  #!/bin/bash
  DATE=$(date +%Y%m%d%H%M)
  BACKUP_DIR=/home/lab21/project/db_backup/
  mysqldump --login-path=local Covid > $BACKUP_DIR"backup_"$DATE.sql
  
  # 3일이 지난 백업 파일삭제
  find $BACKUP_DIR -ctime +3 -exec rm -f {} \;
  
  echo "DB Backup --- $(date +%Y:%m:%d) $(date +%H:%M:%s)"
  ```

  <br>

- `Crontab`을 사용해 코로나 현황 데이터 매일 1회 자동 업데이트, DB 자동 백업

  ```
  30 09 * * * /usr/bin/python3 /home/lab21/project/covid.py >> /home/lab21/cron.log 2>&1
  30 09 * * * sh /home/lab21/project/db_backup.sh >> /home/lab21/cron.log 2>&1
  ```

<br>

## 👍 느낀 점

- 이전과는 달리 크롤링을 하며 발생하는 에러(ex. 리뷰에 여행 날짜가 없으면 에러 발생)들이 많았다. 크롤링을 자동화하기 위해 이를 모두 try/except 문으로 예외 처리해 줬다. 하지만 단순히 에러를 회피하는 방식이었기 때문에 처리할 수 있는 에러들은 그에 맞는 처리 방식을 사용하는 것이 좋을 것 같다.

<br>

