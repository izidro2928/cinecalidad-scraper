from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image

options = Options()

ua = UserAgent()
fake_ua = ua.random

options.add_argument(f"user-agent={fake_ua}")


def cinecalidad_crawler():
    driver = webdriver.Chrome("C:/Program Files/chromedriver_win32/chromedriver.exe", options=options)
    driver.get('https://cinecalidad.ac/')

    while True:
        page_links = driver.find_elements_by_xpath('//*[@id="content_inside"]/div/a')
        movie_links = []

        for movie_link in page_links:
            movie_links.append(movie_link.get_attribute('href'))

        for link in movie_links:
            driver.get(link)

            try:
                title = driver.find_element_by_xpath('//*[@id="main_container"]/div[4]/h1').text
                print(title)

                poster = driver.find_element_by_xpath(
                    '//*[@id="main_container"]/div[4]/table/tbody/tr/td[1]/img').get_attribute('src')
                print(poster)
                poster_path = poster.split("/")[-1]
                poster_name = poster_path.split(".")[-2]

                # Image Process
                image_url = poster
                image_content = requests.get(image_url).content
                image_file = io.BytesIO(image_content)
                image = Image.open(image_file).convert('RGB')
                file_path = 'images/' + poster_name + '.jpg'
                with open(file_path, 'wb') as f:
                    image.save(f, "JPEG", quality=85)
                # End Image Process

                overview = driver.find_element_by_xpath(
                    '//*[@id="main_container"]/div[4]/table/tbody/tr/td[2]/div[1]/p').text
                print(overview)

                votes = driver.find_element_by_xpath("//div[@id='imdb-box']").text
                res = votes.split()
                imdb = res[3]
                print(imdb)

                genre = driver.find_element_by_xpath("//strong[text()='Género:']/following-sibling::span/a[1]").text
                print(genre)

                online1 = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[1]/li')
                online1.click()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="tviframe"]')))
                video1 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tviframe"]'))).get_attribute('src')
                print(video1)
                driver.switch_to.default_content()
                driver.find_element_by_xpath('//*[@id="cambiar_servidor"]').click()

                online2 = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[2]/li')
                online2.click()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="tviframe"]')))
                video2 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tviframe"]'))).get_attribute('src')
                print(video2)
                driver.switch_to.default_content()
                driver.find_element_by_xpath('//*[@id="cambiar_servidor"]').click()

                online3 = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[3]/li')
                online3.click()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="tviframe"]')))
                video3 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tviframe"]'))).get_attribute('src')
                print(video3)
                driver.switch_to.default_content()
                driver.find_element_by_xpath('//*[@id="cambiar_servidor"]').click()

                online4 = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[4]/li')
                online4.click()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="tviframe"]')))
                video4 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tviframe"]'))).get_attribute('src')
                print(video4)
                driver.switch_to.default_content()
                driver.find_element_by_xpath('//*[@id="cambiar_servidor"]').click()

                online5 = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[5]/li')
                online5.click()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="tviframe"]')))
                video5 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tviframe"]'))).get_attribute('src')
                print(video5)
                driver.switch_to.default_content()
                driver.find_element_by_xpath('//*[@id="cambiar_servidor"]').click()

                online6 = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[6]/li')
                online6.click()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="tviframe"]')))
                video6 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tviframe"]'))).get_attribute('src')
                print(video6)
                driver.switch_to.default_content()
                driver.find_element_by_xpath('//*[@id="cambiar_servidor"]').click()
                driver.back()

                online7 = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[7]/li')
                online7.click()
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="tviframe"]')))
                video7 = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tviframe"]'))).get_attribute('src')
                print(video7)
                driver.switch_to.default_content()
                driver.find_element_by_xpath('//*[@id="cambiar_servidor"]').click()

                trailer = driver.find_element_by_xpath('//*[@id="panel_online"]/ul/a[last()]').get_attribute('data-src')
                print(trailer)
            except Exception:
                pass
        try:
            pagination = driver.find_element_by_class_name('nextpostslink')
            print(pagination.get_attribute('href'))
            pagination.click()
        except Exception:
            print("There was an error!")
            driver.quit()


cinecalidad_crawler()
