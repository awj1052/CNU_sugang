from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import time

import account

def zf(s):
    return str(s).zfill(2)

def get_current_time():
    now = time.localtime()
    return f"[{now.tm_year}.{zf(now.tm_mon)}.{zf(now.tm_mday)} {zf(now.tm_hour)}:{zf(now.tm_min)}:{zf(now.tm_sec)}]"

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
    print(get_current_time(), 'login')
    time.sleep(5)
    driver.find_element(By.LINK_TEXT, '수강신청 화면으로 이동').click() # 수강신청 화면 이동
    print(get_current_time(), 'move page')
    time.sleep(5)

def sugang(driver):

    buttons = driver.find_elements(By.LINK_TEXT, '확정하기')
    if len(buttons) == 1:
        return True
    for index, value in enumerate(buttons):
        if index == 0: continue
        value.click()
        time.sleep(0.8)

        alert_text = '대기열'
        try:
            alert = Alert(driver)
            alert_text = alert.text
            alert.accept()
        except:
            print(get_current_time(), 'alert not found')
            time.sleep(10)

        time.sleep(0.4)        

        if not '인원이 초과' in alert_text: # message
            xpath = f'/html/body/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[5]/div/div/div[20]/div/div/div/div/div[3]/div/div[2]/div/div[1]/div/div/div[{index+1}]/div[4]/div/div/div'
            element = driver.find_element(By.XPATH, xpath)
            print(get_current_time(), alert_text, element.text)
    return False
