import WebService

if __name__ == "__main__":

    driver = WebService.get_driver()

    print("init")
    WebService.init(driver)
    while 1:
        WebService.sugang(driver)
    
    driver.close()
