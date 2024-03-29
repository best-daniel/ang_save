import argparse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import getpass

# ID: #otp > div:nth-child(1) > div > input.input_id
# PWD: #otp > div:nth-child(1) > div > input.input_pw
URL_MAIN = "https://www.clien.net/service/"
URL_LOGIN = "https://www.clien.net/service/auth/login"
URL_MYARTICLE = "https://www.clien.net/service/mypage/myArticle?&type=articles"
URL_SEARCHING = "https://www.clien.net/service/search/group/community?sk=id&sv={USER_ID}&po={PAGE_NUM}"
PAGE_WAITING_DELAY = 5

def waiting_page(browser=None, elem_type=By.ID, elem_by_id=None):
    is_success = False
    try:
        myElem = WebDriverWait(browser, PAGE_WAITING_DELAY).until(EC.presence_of_element_located((elem_type, elem_by_id)))
        is_success = True
    except TimeoutException:
        is_success = False
        print("[Warning] Waiting too much time. Try later.")

    return is_success


def input_user_name_pwd():
    user_name = input("Username:")
    passwd = getpass.getpass("Password:")

    return user_name, passwd

def open_browser_handle():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("disable-gpu")

    return webdriver.Chrome(options=options)

def page_login(driver, username, password):
    # ID: #otp > div:nth-child(1) > div > input.input_id
    # PWD: #otp > div:nth-child(1) > div > input.input_pw
    css_id = "#userId"
    css_pwd = "#otp > div:nth-child(1) > div > div.signin-section > input.signin_pw"
    elem = driver.find_element(By.CSS_SELECTOR, css_id)
    if elem is not None:
        elem.send_keys(username)

        elem = driver.find_element(By.CSS_SELECTOR, css_pwd)
        if elem is not None:
            elem.send_keys(password)
            elem.send_keys(Keys.ENTER)

    # Waiting until page is changed
    if waiting_page(browser=driver, elem_type=By.ID, elem_by_id="myinfoForm"):
        return True

    return False


def clean_cookie(driver):

    # Main page xpath
    # Cookie: /html/body/div[6]/div[2]/div[1]/div[1]/button
    # Security: //*[@id="security_modal"]/div[1]/div[1]/button

    # Searching xpath
    # /html/body/div[6]/div[2]/div[1]/div[1]/button
    # //*[@id="security_modal"]/div[1]/div[1]/button


    # Cookie
    if waiting_page(browser=driver, elem_type=By.CLASS_NAME, elem_by_id="fc-dialog-container"):
        try:
            elem = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[1]/div[1]/button')
            if elem is not None:
                elem.click()
                print("[INFO] Click cookie / ads button")
        except Exception as e:
            pass

    if waiting_page(browser=driver, elem_type=By.CLASS_NAME, elem_by_id="modal_security_content"):
        try:
            elem = driver.find_element(By.XPATH, '//*[@id="security_modal"]/div[1]/div[1]/button')
            if elem is not None:
                elem.click()
                print("[INFO] Click - Password security")
        except Exception as e:
            pass

    return True


def parse_input():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--delay', dest='page_delay', action='store',
                        default=5, type=int,
                        help='Max. Page waiting time..(default: 5 seconds)')
    parser.add_argument('--file', dest='filename', action='store',
                        default="backup.txt",
                        help='Save url list')
    return parser


def _main():
    parser = parse_input()
    args = parser.parse_args()

    global PAGE_WAITING_DELAY
    PAGE_WAITING_DELAY = int(args.page_delay)

    # Input user ID/PWD
    user_id, password = input_user_name_pwd()
    if len(user_id) <= 3 or len(password) <=3:
        print("[ERROR] Incorrect User ID or Password")
        return -1

    # Browser handle
    driver = open_browser_handle()
    if driver is None:
        return -1

    # Move page
    driver.get(URL_LOGIN)
    # Login page
    # Waiting page login
    if not waiting_page(browser=driver, elem_type=By.ID, elem_by_id="loginForm"):
        print("[WARNING] Cannot find login form")
        driver.close()
        return -1

    if not page_login(driver, user_id, password):
        print("[WARNING] Timeout")
        driver.close()
        return -1

    # Cookie / Password security
    clean_cookie(driver)

    fFile = open(args.filename, "w")

    page_num = 0
    max_page = 1
    while page_num < max_page:
        # Move my article
        PAGE_URL = URL_SEARCHING.format(USER_ID=user_id, PAGE_NUM=page_num)
        driver.get(PAGE_URL)
        print("[INFO] Searching URL: ", PAGE_URL)
        if not waiting_page(browser=driver, elem_type=By.CLASS_NAME, elem_by_id="list_content"):
            print("[WARNING] Timeout: searching by ID")
            break

        # Total page num
        # Once at page start
        if (page_num%10) == 0:
            try:
                elem = driver.find_element(By.CLASS_NAME, "board-nav-area")
                if elem is not None:
                    all_child = elem.find_elements(By.CSS_SELECTOR, '*')
                    max_page += len(all_child)
            except:
                print("[WARNING] Cannot find result")
                break

        print("[INFO] Page  %d/%d" % (page_num, max_page))

        """
        elem = driver.find_element(By.CLASS_NAME, "board-nav-area")
        if elem is not None:
            all_child = elem.find_elements(By.CSS_SELECTOR, '*')
            max_page = len(all_child)
        else:
            break
        """
        """
        if driver.find_element(By.CLASS_NAME, "board-nav-next") is None:
            has_next_page = False
        """

        # list_content: //*[@id="div_content"]/div[6]
        # or item list: #div_content > div.list_content > div:nth-child
        elem = driver.find_element(By.CSS_SELECTOR, "#div_content > div.list_content")
        if elem is None:
            break

        all_child = elem.find_elements(By.CSS_SELECTOR, '*')

        save_url_list = []
        for elem_item in all_child:
            # list_subject
            #
            class_name = elem_item.get_attribute("class")
            if class_name == "list_subject":
                href_info = elem_item.get_attribute("href")
                if href_info is not None:
                    save_url_list.append(href_info)
                    print("[INFO] Page: %d, URL: %s" % (page_num, elem_item.get_attribute("href")))

        fFile.write("\n".join(save_url_list)+"\n")

        page_num += 1
        if page_num == 5:
            break

    fFile.close()
    driver.close()
    return 0


if __name__ == "__main__":
    exit(_main())