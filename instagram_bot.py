from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, strftime
from random import randint
import pandas as pd

PATH = "C:\chromedriver.exe"
custom_options = webdriver.ChromeOptions()
prefs = {
  "translate_whitelists": {"fr":"en"},
  "translate":{"enabled":"true"}
}
custom_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(PATH, options=custom_options)
driver.get("https://www.instagram.com/accounts/login/?source=auth_switcher")

try:
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    username.send_keys("mohcine.bouzalim2016@gmail.com")
    password = driver.find_element_by_name("password")
    password.send_keys("mohcine@1997")
    button_login = driver.find_element_by_css_selector("#loginForm > div > div:nth-child(3) > button")
    button_login.click()
    sleep(3)

    notnow1 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root > section > main > div > div > div > div > button"))
    )
    notnow1.click()
    
    while  True:
        try:
            notnow2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div:nth-child(13) > div > div > div > div.mt3GC > button.aOOlW.HoLwm"))
            )
            notnow2.click()
        except:
            break

    hashtag_list = ["travel", "london"]
    prev_user_list = [] #if it's the first time you run it, use this line and comment the two below
    #prev_user_list = pd.read_csv("the_last_csv_file_here").iloc[:,1:2]
    #prev_user_list = list(prev_user_list['0'])

    new_followed = []
    tag = -1
    followed = 0
    likes = 0
    comments = 0

    for hashtag in hashtag_list:
        tag += 1
        driver.get("https://www.instagram.com/explore/tags/"+ hashtag_list[tag] + "/")
        sleep(5)
        first_thumbnail = driver.find_element_by_css_selector("#react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1) > a > div > div.KL4Bh")
        driver.execute_script("arguments[0].click();", first_thumbnail)

        sleep(randint(2,4))

        try:
            for i in range(1,3):
                username = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a").text
                if username not in prev_user_list:
                    if driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button").text == "Follow":
                        driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button").click()
                        new_followed.append(username)
                        followed += 1

                        #likes
                        button_like = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button/div/span")
                        button_like.click()
                        likes += 1
                        sleep(randint(20,25))
                        
                        #comments
                        comm_proba = randint(1,10)
                        if comm_proba > 7:
                            comments += 1
                            driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[2]/button").click()
                            comment_box = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[3]/section[3]/div/form/textarea")
                            if comm_proba < 10 :
                                comment_box.send_keys("Nice")
                                sleep(2)
                            else:
                                comment_box.send_keys("Cool")
                                sleep(2)
                            comment_box.send_keys(Keys.ENTER)
                            sleep(randint(20,25))

                    driver.find_element_by_link_text("Next").click()
                    sleep(randint(20,25))
                    
                else:
                    driver.find_element_by_link_text("Next").click()
                    sleep(randint(20,25))
        except:
            continue
    
    for i in range(0, len(new_followed)):
        prev_user_list.append(new_followed[i])
    
    new_user_df = pd.DataFrame(prev_user_list)
    new_user_df.to_csv('{}_users_followed_list.csv'.format(strftime("%Y%m%d-%H%M%S")))
    print('Liked {} photos.'.format(likes))
    print('Commented {} photos.'.format(comments))
    print('Followed {} new people.'.format(followed))


finally:
    driver.quit()
