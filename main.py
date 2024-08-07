import WebService
import time

if __name__ == "__main__":
    while 1:
        try:
            driver = WebService.get_driver()

            print("init")
            WebService.init(driver)
            while 1:
                WebService.sugang(driver)

            driver.close()
        except:
           print('restart')
           time.sleep(5) 
    
