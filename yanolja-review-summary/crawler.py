import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver

URL = 'https://nol.yanolja.com/reviews/domestic/10054600'

def crawl_yanolja_reviews():
    review_list = []
    driver = webdriver.Chrome()
    driver.get(URL)

    time.sleep(3)

    scroll_count = 10
    for i in range(scroll_count):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    review_containers = soup.select('div.css-166s55a')

    for container in review_containers:
        review_text = container.find('p', class_='content-text').text.strip()
        full_stars = container.select('path[fill="currentColor"]:not([fill-rule])')
        star_cnt = len(full_stars)
        date = container.select_one('p.css-6lreu3').text.strip()

        review_dict = {
            'review' : review_text,
            'stars' : star_cnt,
            'date' : date
        }

        review_list.append(review_dict)

    with open('./res/reviews.json','w', encoding='utf-8') as f:
        json.dump(review_list,f,indent=4,ensure_ascii=False)

if __name__ == '__main__':
    crawl_yanolja_reviews()