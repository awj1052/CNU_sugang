from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
import time

import account

# 클릭 후 alert 띄울 때까지 기다리는 시간
CLICK_AFTER_INTERVAL = 0.8

# alert 닫고 기다리는 시간
WAIT_INTERVAL = 0.4

# 대기열 등 오류 났을 때 기다리는 시간
QUEUE_INTERVAL = 5

# init 시 페이지 이동을 기다리는 시간
PAGELOAD_INTERVAL = 5

# alert에 단어가 포함되지 않으면 로그 메세지 print
# EXCLUDED_WORD = '인원이 초과' # DEFAULT
EXCLUDED_WORD = '인원이 초과' # DEFAULT

# 수정 끝

def zf(s):
    return str(s).zfill(2)

def get_current_time():
    now = time.localtime()
    return f"[{now.tm_year}.{zf(now.tm_mon)}.{zf(now.tm_mday)} {zf(now.tm_hour)}:{zf(now.tm_min)}:{zf(now.tm_sec)}]"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    #chrome_options.add_argument("--headless")
    #chrome_service = webdriver.ChromeService('/usr/lib/chromium-browser/chromedriver')
    driver = webdriver.Chrome(options=chrome_options)#, service=chrome_service)
    return driver

def init(driver):
    driver.get('https://sugang.cnu.ac.kr/login.do')
    driver.find_element(By.XPATH, '//*[@id="USER_ID"]').send_keys(account.ID)
    driver.find_element(By.XPATH, '//*[@id="USER_PWD"]').send_keys(account.PW)
    driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div/div/div[1]/div/button').click() # 로그인
    print(get_current_time(), 'login')
    time.sleep(PAGELOAD_INTERVAL)
    driver.find_element(By.LINK_TEXT, '수강신청 화면으로 이동').click() # 수강신청 화면 이동
    print(get_current_time(), 'move page')
    time.sleep(PAGELOAD_INTERVAL)

def sugang_code(driver, codes):
    if len(codes) == 0: 
        return True
    
    complete = []
    for i in range(len(codes)):
        a,b,c = codes[i].split("-")

        A = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[5]/div/div/div[17]/div/div/div[8]/div/div/div[4]/div/div/div[13]/div/input')
        A.clear(); A.send_keys(a)
        
        B = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[5]/div/div/div[17]/div/div/div[8]/div/div/div[4]/div/div/div[15]/div/input')
        B.clear(); B.send_keys(b)
        
        C = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[5]/div/div/div[17]/div/div/div[8]/div/div/div[4]/div/div/div[17]/div/input')
        C.clear(); C.send_keys(c)

        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[5]/div/div/div[17]/div/div/div[8]/div/div/div[4]/div/div/div[18]/a')\
            .click()
        
        time.sleep(CLICK_AFTER_INTERVAL)

        alert_text = check_alert(driver)

        time.sleep(WAIT_INTERVAL)

        if not EXCLUDED_WORD in alert_text: # message
            print(get_current_time(), f'{alert_text} {a}-{b}-{c}')
        if '이미 이수한 과목' in alert_text:
            complete.append(i)
    
    for i in range(len(complete)-1, -1, -1):
        codes.pop(complete[i])
    return False

def sugang(driver, complete):
    buttons = driver.find_elements(By.LINK_TEXT, '확정하기')
    if len(buttons) == 0:
        return True
    
    if complete[-1] != len(buttons):
        complete[-1] = len(buttons)
        for i in range(len(complete)-1):
            complete[i] = 0
    else:
        res = 0
        for i in range(len(complete)-1):
            if complete[i]: res += 1
        if res == complete[-1]: return True

    for index, value in enumerate(buttons):
        if complete[index]: continue
        value.click()
        time.sleep(CLICK_AFTER_INTERVAL)

        alert_text = check_alert(driver)

        time.sleep(WAIT_INTERVAL)        

        if not EXCLUDED_WORD in alert_text: # message
            xpath = f'/html/body/div[1]/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div/div/div/div[1]/div/div/div/div/div[5]/div/div/div[20]/div/div/div/div/div[3]/div/div[2]/div/div[1]/div/div/div[{index+1}]/div[4]/div/div/div'
            element = driver.find_element(By.XPATH, xpath)
            print(get_current_time(), alert_text, element.text)
        if '이미 이수한 과목' in alert_text:
            complete[index] = 1
    return False

def check_alert(driver):
    alert_text = '대기열'
    try:
        alert = Alert(driver)
        alert_text = alert.text
        alert.accept()
    except:
        print(get_current_time(), 'alert not found')
        time.sleep(QUEUE_INTERVAL)
    return alert_text