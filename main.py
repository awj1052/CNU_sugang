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
            while 1:
                WebService.sugang(driver)

            driver.close()
        except:
           print(get_current_time(), 'restart')
           time.sleep(5) 
    
