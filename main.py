import WebService
import time


# 과목번호 아래와 같이 수정
# target_code = [
#     "1214-2003-01",
#     "1214-2004-01",
# ]

target_code = [
    "1214-2003-01"
]

# 예비 수강신청 아이템 개수 10보다 클 때만 수정
BASKET = 10

# 수정 끝

# complete[-1]을 사용하기 위함
BASKET += 1
complete = [0]*BASKET

def get_current_time():
    return WebService.get_current_time()

if __name__ == "__main__":
    while 1:
        try:
            driver = WebService.get_driver()

            print(get_current_time(), "init")
            WebService.init(driver)

            flag = True
            while 1:
                flag = WebService.sugang(driver, complete)
                flag = WebService.sugang_code(driver, target_code) and flag
                
                if flag:
                    break

            driver.close()
            if flag:
                print(get_current_time(), "수강신청 완료")
                break
        except:
            print(get_current_time(), 'restart')
            time.sleep(5) 
    
