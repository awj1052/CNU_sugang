from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import time

import account

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_service = webdriver.ChromeService('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(options=chrome_options, service=chrome_service)
    return driver

def init(driver):
    driver.get('https://sugang.cnu.ac.kr/login.do')
    driver.find_element(By.XPATH, '//*[@id="USER_ID"]').send_keys(account.ID)
    driver.find_element(By.XPATH, '//*[@id="USER_PWD"]').send_keys(account.PW)
    driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div[1]/div/button').click() # 로그인
    print('login')
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, '수강신청 화면으로 이동').click() # 수강신청 화면 이동
    print('move page')
    time.sleep(5)

def sugang(driver):

    buttons = driver.find_elements(By.LINK_TEXT, '확정하기')
    if len(buttons) == 1:
        exit()
    for index, value in enumerate(buttons):
        if index == 0: continue
        value.click()
        time.sleep(0.5)

        try:
            alert = Alert(driver)
            alert_text = alert.text
            alert.accept()
        except:
            time.sleep(5)

        time.sleep(0.5)        

        if not '인원이 초과' in alert_text: # message
            xpath = f'/html/body/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[5]/div/div/div[20]/div/div/div/div/div[3]/div/div[2]/div/div[1]/div/div/div[{index+1}]/div[4]/div/div/div'
            element = driver.find_element(By.XPATH, xpath)
            print(alert_text, element.text)
