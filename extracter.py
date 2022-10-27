from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from progressbar import ProgressBar
import time
import os
import os.path

def startChrome():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1000, 1000)
    return driver

def goToEducativeMainPage(driver):
    driver.get("https://www.educative.io/")

def getPTags(driver):
    contents = driver.find_elements(By.TAG_NAME, "p")
    file_object = open('course.txt', 'a')
    exclude = ["COURSE ASSESSMENT", "MINI PROJECT", "COURSE PROJECT"]
    for content in contents:
        if content.text in exclude:
            continue
        else:
            file_object.write(content.text + "\n")
    file_object.close()

def getH1Tags(driver):
    contents = driver.find_elements(By.TAG_NAME, "h1")
    file_object = open('course.txt', 'a')
    for content in contents:
        file_object.write("Lesson Title: " + content.text + "\n")
    file_object.close()

def getliTags(driver):
    contents = driver.find_elements(By.TAG_NAME, "li")
    file_object = open('course.txt', 'a')
    for content in contents:
        file_object.write(content.text + "\n")
    file_object.write("\n")
    file_object.close()

def getLinksFromFile():
    linksList = []
    filesize = os.path.getsize("links.txt")
    if filesize == 0:
        return (False, linksList)
    else:
        file_object = open('links.txt', 'r')
        links = file_object.readlines()
        for link in links:
            linksList.append(link.strip())
        file_object.close()
        return (True, linksList)

def extractLessonLinks(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, "div[class='flex w-full']>a")
    file_object = open('links.txt', 'a')
    for element in elements:
        link = element.get_attribute("href")
        file_object.write(link + "\n")
    file_object.close()

def myProgressBar(n):
    pbar = ProgressBar()
    for i in pbar(range(n)):
        time.sleep(1)

def main():
    print('Program started. Please wait...')
    print('')
    if os.path.exists('course.txt') == True:
        os.remove("course.txt")
    if os.path.exists('links.txt') == True:
        os.remove("links.txt")
    myProgressBar(3)
    print('')
    driver = startChrome()
    goToEducativeMainPage(driver)
    print('')
    input("Please log in using your account and then press enter to continue.")
    print('')
    print('Processing. Please wait...')
    print('')
    myProgressBar(8)
    print('')
    acceptedURLs = ["https://www.educative.io/learn", "https://www.educative.io/explore", "https://www.educative.io/learning-plans", "https://www.educative.io/projects", "https://www.educative.io/paths", "https://www.educative.io/assessments", "https://www.educative.io/onboarding/dashboard", "https://www.educative.io/onboarding/plans", "https://www.educative.io/onboarding/drafts", "https://www.educative.io/onboarding/modules"]
    if driver.current_url not in acceptedURLs:
        print("We detected you are not logged in yet! Please login and then try again.")
        driver.quit()
    else:
        print("Please enter URL of the **FIRST** lesson of the course you want to scrape. Make sure the link is of the **PUBLISHED** version of the course and not the page editor.")
        print("For example: https://www.educative.io/courses/react-beginner-to-advanced/JY1xJkJgrqg")
        print('')
        firstURL = input("Enter URL here: ")
        print('')
        linksExtracted = False
        try:
            driver.get(firstURL)
            myProgressBar(5)
            print('')
            print('Extracting course lesson links. Please wait...')
            print('')
            extractLessonLinks(driver)
            linksExtracted = True
        except:
            print('Some error occured while fetching course lesson links. Please try later. Content scrapping failed.')
            driver.quit()
        if linksExtracted == True:
            resp = getLinksFromFile()
            if resp[0] == False:
                print('Links.txt file is empty. Please make sure there are lesson links inside the file. Content scrapping failed.')
                driver.quit()
            else:
                links = resp[1]
                count = 0
                try:
                    print('Content scrapping started. Please be patient.')
                    print('You can open the course.txt file in any editor to monitor its contents side by side.')
                    print('')
                    for link in links:
                        driver.get(link)
                        myProgressBar(5)
                        getH1Tags(driver)
                        getPTags(driver)
                        getliTags(driver)
                        print('Lesson: ', link, ' content added to course.txt file. Total lessons done = ', count + 1)
                        print('')
                        count = count + 1
                    print('')
                    print('All done. Content scrapped from a total of ', count, ' lessons.')
                    driver.quit()
                except:
                    print('Sorry! Something went wrong. Please try again later.')
                    driver.quit()

main()
