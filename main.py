import WebService
import time

def get_current_time():
    return WebService.get_current_time()

if __name__ == "__main__":
    while 1:
        try:
            driver = WebService.get_driver()

            print(get_current_time(), "init")
            WebService.init(driver)

            flag = False
            while 1:
                flag = WebService.sugang(driver)
                if flag:
                    break

            driver.close()
            if flag:
                print(get_current_time(), "수강신청 완료")
                break
        except:
            print(get_current_time(), 'restart')
            time.sleep(5) 
    
