import os
import time
import urllib3
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

if __name__ == "__main__":
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }
    print("input start and end:\n")
    a,b = (int(i) for i in (input().split()))
    urllib3.disable_warnings()
    options = webdriver.ChromeOptions()
    options.binary_location = r"E:\chrome-win\chrome.exe"
    driver = webdriver.Chrome(options=options,executable_path=r"E:\chrome-win\driver\chromedriver.exe")
    driver.implicitly_wait(2)
    url_root = "https://www.???/"
    driver.refresh()
    driver.maximize_window()
    time.sleep(2)
    post = a
    while(post<b):
        try:
            html_url_1 = url_root + 'r15/' + post.__str__() + '.html'
            html_url_2 = url_root + 'r18/' + post.__str__() + '.html'
            post += 1
            driver.get(html_url_1)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            isNull = soup.find_all('img', class_="nocontent")
            if len(isNull) == 0:
                html_url = html_url_1
            else:
                driver.get(html_url_2)
                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                isNull = soup.find_all('img', class_="nocontent")
                if len(isNull) == 0:
                    html_url = html_url_2
                else:
                    continue
            driver.get(html_url)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            url_list = soup.find_all('img', class_="post-item-img lazy")
            if len(url_list) == 0:
                continue
            print(len(url_list))
            title = url_list[0].get('title')[:-4].replace(' ', '_')
            print(title)
            if not os.path.exists('./img/' + title):
                os.mkdir('./img/' + title)
            for i in range(0, len(url_list)):
                url_list[i] = url_list[i].get('data-original')
            print(url_list)
            for url in url_list:
                print(f"download {url}")
                try:
                    response = requests.get(url,proxies=proxies,verify=False,timeout=60)
                    print(response)
                    filename = url.split('/')[-1]
                    with open('./img/' + title + '/' + '%s' % filename, "wb") as f:
                        f.write(response.content)
                except Exception as e:
                    print("Exception:", e)
                    continue
            time.sleep(0.5)
        except Exception as e:
            print("Exception:",e)
            continue