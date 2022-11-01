from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from progressbar import ProgressBar
import time
import os
import os.path
from os import system
import re

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
    for _ in pbar(range(n)):
        time.sleep(1)

def main():
    if os.path.exists('course.txt') == True:
        os.remove("course.txt")
    if os.path.exists('links.txt') == True:
        os.remove("links.txt")
    driver = startChrome()
    system('clear')
    print("Please log in using your account and then press enter to continue.")
    print('')
    goToEducativeMainPage(driver)
    input("")
    print('Validating if you are logged in. Please wait...')
    print('')
    myProgressBar(15)
    print('')
    acceptedURLs = ["https://www.educative.io/learn", "https://www.educative.io/explore", "https://www.educative.io/learning-plans", "https://www.educative.io/projects", "https://www.educative.io/paths", "https://www.educative.io/assessments", "https://www.educative.io/onboarding/dashboard", "https://www.educative.io/onboarding/plans", "https://www.educative.io/onboarding/drafts", "https://www.educative.io/onboarding/modules", "https://www.educative.io/onboarding/assigned-plans", "https://www.educative.io/teach", "https://www.educative.io/create-answer", "https://www.educative.io/paths-dashboard", "https://www.educative.io/assessments-dashboard", "https://www.educative.io/learning-plans-dashboard/questionnaire", "https://www.educative.io/learning-plans-dashboard/modules"]
    if driver.current_url not in acceptedURLs:
        system('clear')
        print("We detected you are not logged in yet! Please login and then try again.")
        driver.quit()
    else:
        system('clear')
        print('Press 1 to extract content from all lessons of the course (quiz, project, mini-project, and assessment lessons will be skipped)')
        print('')
        print('press 2 to extract lessons within a range (quiz, project, mini-project, and assessment lessons will be skipped)')
        print('')
        while True:
            choice = input("Enter your choice: ")
            if choice.isdigit() == False:
                print('Invalid choice! Enter again.')
                print('')
            else:
                if int(choice) not in [1, 2]:
                    print('Invalid choice! Enter again.')
                    print('')
                else:
                    break
        if int(choice) == 1:
            system('clear')
            print("Please enter URL of any lesson of the course you want to scrape. Make sure the URL is of the **PUBLISHED** version of the course and not the page editor.")
            print("For example: https://www.educative.io/courses/react-beginner-to-advanced/JY1xJkJgrqg")
            print('')
            while True:
                firstURL = input("Enter URL here: ")
                regex = re.compile('^https://www.educative.io/courses/')
                if re.match(regex, firstURL):
                    if len(firstURL.split("//")[1].split("/")) != 4:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        break
                else:
                    print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                    print('')
            linksExtracted = False
            try:
                system('clear')
                print('Extracting course lesson links. Please wait...')
                print('')
                driver.get(firstURL)
                myProgressBar(8)
                print('')
                extractLessonLinks(driver)
                linksExtracted = True
            except:
                system('clear')
                print('Some error occured while fetching course lesson links. Please try later. Content scrapping failed.')
                driver.quit()
            if linksExtracted == True:
                resp = getLinksFromFile()
                if resp[0] == False:
                    system('clear')
                    print('Links.txt file is empty. Please make sure there are lesson links inside the file. Content scrapping failed.')
                    driver.quit()
                else:
                    links = resp[1]
                    os.remove("links.txt")
                    count = 0
                    try:
                        system('clear')
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
                        system('clear')
                        print('All done. Content scrapped from a total of ', count, ' lessons.')
                        print('Open the course.txt file to see the results.')
                        driver.quit()
                    except:
                        system('clear')
                        print('Sorry! Something went wrong. Please try again later.')
                        driver.quit()
        else:
            system('clear')
            print("Please enter the URL of the lesson from where you want to start content scrapping.")
            print("Make sure the URL is of the **PUBLISHED** version of the course and not the page editor.")
            print("For example: https://www.educative.io/courses/react-beginner-to-advanced/JY1xJkJgrqg")
            print('')
            firstURL = None
            while True:
                firstURL = input("Enter URL here: ")
                regex = re.compile('^https://www.educative.io/courses/')
                if re.match(regex, firstURL):
                    if len(firstURL.split("//")[1].split("/")) != 4:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        break
                else:
                    print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                    print('')

            system('clear')

            print("Please enter the URL of the lesson from where you want to stop content scrapping.")
            print("Note that this lesson will be included in content scrapping")
            print("Make sure the URL is of the **PUBLISHED** version of the course and not the page editor.")
            print("For example: https://www.educative.io/courses/react-beginner-to-advanced/JPD8EKAxAqg")
            print('')
            secondURL = None
            while True:
                secondURL = input("Enter URL here: ")
                regex = re.compile('^https://www.educative.io/courses/')
                if re.match(regex, secondURL):
                    if len(secondURL.split("//")[1].split("/")) != 4:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        if secondURL.split("//")[1].split("/")[2] != firstURL.split("//")[1].split("/")[2]:
                            print("URL does not seem to be from the same course as the URL entered previously. Please enter again.")
                            print('')
                        else:
                            break
                else:
                    print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                    print('')

            print('')
            linksExtracted = False
            try:
                system('clear')
                print('Checking order of both URLs. Checking if second URL comes after the first one or not.')
                print('')
                driver.get(firstURL)
                myProgressBar(8)
                print('')
                extractLessonLinks(driver)
                linksExtracted = True
            except:
                system('clear')
                print('Some error occured while fetching course lesson links. Please try later. Content scrapping failed.')
                driver.quit()

            if linksExtracted == True:
                resp = getLinksFromFile()
                if resp[0] == False:
                    system('clear')
                    print('Links.txt file is empty. Please make sure there are lesson links inside the file. Content scrapping failed.')
                    driver.quit()
                else:
                    links = resp[1]
                    os.remove("links.txt")
                    # checking order of both URLs
                    pos1 = None
                    pos2 = None
                    for i in range(len(links)):
                        if links[i] == firstURL:
                            pos1 = i
                        if links[i] == secondURL:
                            pos2 = i
                    if pos2 < pos1:
                        system('clear')
                        print('Order of both URLs entered is not correct. Make sure the second URL is of the lesson that comes **AFTER** the first URL.')
                        print('Try again later')
                        driver.quit()
                    else:
                        count = 0
                        links = links[pos1:(pos2+1)]
                        try:
                            system('clear')
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
                            system('clear')
                            print('All done. Content scrapped from a total of ', count, ' lessons.')
                            print('Open the course.txt file to see the results.')
                            driver.quit()
                        except:
                            system('clear')
                            print('Sorry! Something went wrong. Please try again later.')
                            driver.quit()

main()
