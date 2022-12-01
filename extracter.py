from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from progressbar import ProgressBar
import time
import os
import os.path
from os import system
from bs4 import BeautifulSoup
import re
import argparse
import sys

def startChrome():
    options = webdriver.ChromeOptions()
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument("--start-maximized")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1000, 1000)
    return driver

def goToEducativeMainPage(driver):
    driver.get("https://www.educative.io/")

# def getPTags(driver):
#     contents = driver.find_elements(By.TAG_NAME, "p")
#     file_object = open('course.txt', 'a')
#     exclude = ["COURSE ASSESSMENT", "MINI PROJECT", "COURSE PROJECT"]
#     for content in contents:
#         if content.text in exclude:
#             continue
#         elif content.get_attribute("class") == "katex-block ":
#             continue
#         elif content.get_attribute("class") == "katex-block":
#             continue
#         else:
#             file_object.write(content.text + "\n")
#     file_object.close()

def getPTags(driver):
    contents = driver.find_elements(By.TAG_NAME, "p")
    file_object = open('course.txt', 'a')
    exclude = ["COURSE ASSESSMENT", "MINI PROJECT", "COURSE PROJECT"]
    for content in contents:
        if content.text in exclude:
            continue
        elif content.get_attribute("class") == "katex-block ":
            continue
        elif content.get_attribute("class") == "katex-block":
            continue
        else:
            temp = content.get_attribute('innerHTML')
            temp1 = BeautifulSoup(temp, features="html.parser")
            unwanted = temp1.find_all('annotation')
            unwanted2 = temp1.find_all('span',{'class': 'katex-html'})
            unwanted3 = temp1.find_all('span',{'class': 'mspace'})
            unwanted4 = temp1.find_all('mtext')
            for i in unwanted:
                i.extract()
            for i in unwanted2:
                i.extract()
            for i in unwanted3:
                i.extract()
            for i in unwanted4:
                i.extract()
            file_object.write(temp1.text + "\n")
    file_object.close()

def getH1Tags(driver):
    contents = driver.find_elements(By.TAG_NAME, "h1")
    file_object = open('course.txt', 'a')
    for content in contents:
        file_object.write("Lesson Title: " + content.text + "\n")
    file_object.close()

# def getliTags(driver):
#     contents = driver.find_elements(By.TAG_NAME, "li")
#     file_object = open('course.txt', 'a')
#     for content in contents:
#         file_object.write(content.text + "\n")
#     file_object.write("\n")
#     file_object.close()

def getliTags(driver):
    contents = driver.find_elements(By.TAG_NAME, "li")
    file_object = open('course.txt', 'a')
    for content in contents:
        temp = content.get_attribute('innerHTML')
        temp1 = BeautifulSoup(temp, features="html.parser")
        unwanted = temp1.find_all('annotation')
        unwanted2 = temp1.find_all('span',{'class': 'katex-html'})
        unwanted3 = temp1.find_all('span',{'class': 'mspace'})
        unwanted4 = temp1.find_all('mtext')
        for i in unwanted:
            i.extract()
        for i in unwanted2:
            i.extract()
        for i in unwanted3:
            i.extract()
        for i in unwanted4:
            i.extract()
        file_object.write(temp1.text + "\n")
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

def parseFile():
    with open("course.txt", 'r') as inFile, open('temp.txt', 'w') as outFile:
        for line in inFile:
            if line.strip():
                outFile.write(line)
    if os.path.exists('course.txt') == True:
        os.remove("course.txt")
    firstDone = False
    with open('temp.txt','r') as inFile, open('course.txt','w') as outFile:
        for line in inFile:
            line = line.strip()
            if line[0:12] == "Lesson Title":
                if firstDone == False:
                    outFile.write(line + "\n")
                    firstDone = True
                else:
                    outFile.write("\n")
                    outFile.write(line + "\n")
            else:
                outFile.write(line + "\n")

def myParser():
    parser = argparse.ArgumentParser(
        prog = 'Course Content Extractor',
        description = 'Extracts course content from Educative platform',
        epilog = 'Happy Extraction!'
    )
    parser.add_argument(
        '--validationTimer', 
        type=int, 
        required=False,
        default=15,
        help='Number of seconds to wait for login validation. If you have a slow internet connection, increase the number of seconds. Default is 15 seconds.'
    )
    parser.add_argument(
        '--linksFetchingTimer', 
        type=int, 
        required=False,
        default=8,
        help='Number of seconds to wait for links fetching. If you have a slow internet connection, increase the number of seconds. Default is 8 seconds.'
    )
    parser.add_argument(
        '--lessonsExtractionTimer', 
        type=int, 
        required=False,
        default=6,
        help='Number of seconds to wait for individual lesson extraction. If you have a slow internet connection, increase the number of seconds. Default is 6 seconds.'
    )
    args = None
    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code == 2:
            print("")
            print('Execute python3 extracter.py --help on the terminal for details')
            print("")
            sys.exit(0)
        elif e.code == 0:
            sys.exit(0)
    return args

def main():
    if os.path.exists('course.txt') == True:
        os.remove("course.txt")
    if os.path.exists('links.txt') == True:
        os.remove("links.txt")
    if os.path.exists('temp.txt') == True:
        os.remove("temp.txt")
    args = myParser()
    validationTimer = args.validationTimer
    linksFetchingTimer = args.linksFetchingTimer
    lessonsExtractionTimer = args.lessonsExtractionTimer
    driver = startChrome()
    system('clear')
    print("Please log in using your account and then press enter to continue.")
    print('')
    goToEducativeMainPage(driver)
    input("")
    print('Validating if you are logged in. Please wait...')
    print('')
    driver.get("https://www.educative.io/learn")
    myProgressBar(validationTimer)
    print('')
    if driver.current_url not in "https://www.educative.io/learn":
        system('clear')
        print("We detected you are not logged in yet! Program aborted.")
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
            print("Please enter URL of any lesson of the course you want to scrape.")
            print('')
            while True:
                firstURL = input("Enter URL here: ")
                regex1 = re.compile('^https://www.educative.io/courses/')
                regex2 = re.compile('^https://www.educative.io/collection/page/')
                regex3 = re.compile('^https://www.educative.io/pageeditor/')
                flag1 = bool(re.match(regex1, firstURL))
                flag2 = bool(re.match(regex2, firstURL))
                flag3 = bool(re.match(regex3, firstURL))
                if flag1 == True:
                    if len(firstURL.split("//")[1].split("/")) != 4:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        break
                elif flag2 == True:
                    if len(firstURL.split("//")[1].split("/")) != 6:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        break
                elif flag3 == True:
                    if len(firstURL.split("//")[1].split("/")) != 5:
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
                print('Fetching course lesson links. Please wait...')
                print('')
                driver.get(firstURL)
                myProgressBar(linksFetchingTimer)
                print('')
                extractLessonLinks(driver)
                linksExtracted = True
            except:
                system('clear')
                print('Some error occured while fetching course lesson links. Please try later. Program aborted.')
                driver.quit()
            if linksExtracted == True:
                resp = getLinksFromFile()
                if resp[0] == False:
                    system('clear')
                    print('Links extraction failed. Program aborted.')
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
                            myProgressBar(lessonsExtractionTimer)
                            getH1Tags(driver)
                            getPTags(driver)
                            getliTags(driver)
                            print('Lesson: ', link, ' content added to course.txt file. Total lessons done = ', count + 1)
                            print('')
                            count = count + 1
                        system('clear')
                        parseFile()
                        print('All done. Content scrapped from a total of ', count, ' lessons.')
                        print('Open the course.txt file to see the results.')
                        if os.path.exists('temp.txt') == True:
                            os.remove("temp.txt")
                        driver.quit()
                    except:
                        system('clear')
                        print('Sorry! Something went wrong. Please try again later. Program aborted.')
                        driver.quit()
        else:
            system('clear')
            print("Please enter the URL of the lesson from where you want to start content scrapping.")
            print('')
            firstURL = None
            while True:
                firstURL = input("Enter URL here: ")
                regex1 = re.compile('^https://www.educative.io/courses/')
                regex2 = re.compile('^https://www.educative.io/collection/page/')
                regex3 = re.compile('^https://www.educative.io/pageeditor/')
                flag1 = bool(re.match(regex1, firstURL))
                flag2 = bool(re.match(regex2, firstURL))
                flag3 = bool(re.match(regex3, firstURL))
                if flag1 == True:
                    if len(firstURL.split("//")[1].split("/")) != 4:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        break
                elif flag2 == True:
                    if len(firstURL.split("//")[1].split("/")) != 6:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        break
                elif flag3 == True:
                    if len(firstURL.split("//")[1].split("/")) != 5:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        break
                else:
                    print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                    print('')

            system('clear')

            print("Please enter the URL of the lesson from where you want to stop content scrapping.")
            print('')
            secondURL = None
            while True:
                secondURL = input("Enter URL here: ")
                regex1 = re.compile('^https://www.educative.io/courses/')
                regex2 = re.compile('^https://www.educative.io/collection/page/')
                regex3 = re.compile('^https://www.educative.io/pageeditor/')
                flag1 = bool(re.match(regex1, secondURL))
                flag2 = bool(re.match(regex2, secondURL))
                flag3 = bool(re.match(regex3, secondURL))
                if flag1 == True:
                    if len(secondURL.split("//")[1].split("/")) != 4:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        if secondURL.split("//")[1].split("/")[2] != firstURL.split("//")[1].split("/")[2]:
                            print("URL does not seem to be from the same course as the URL entered previously. Please enter again.")
                            print('')
                        else:
                            break
                elif flag2 == True:
                    if len(secondURL.split("//")[1].split("/")) != 6:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        if (secondURL.split("//")[1].split("/")[3] != firstURL.split("//")[1].split("/")[3]) and (secondURL.split("//")[1].split("/")[4] != firstURL.split("//")[1].split("/")[4]):
                            print("URL does not seem to be from the same course as the URL entered previously. Please enter again.")
                            print('')
                        else:
                            break
                elif flag3 == True:
                    if len(secondURL.split("//")[1].split("/")) != 5:
                        print('URL does not seem to be from the lesson of an Educative course. Please enter again.')
                        print('')
                    else:
                        if (secondURL.split("//")[1].split("/")[2] != firstURL.split("//")[1].split("/")[2]) and (secondURL.split("//")[1].split("/")[3] != firstURL.split("//")[1].split("/")[3]):
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
                print('Checking order of both URLs. Checking if second URL comes after the first URL or not.')
                print('')
                driver.get(firstURL)
                myProgressBar(linksFetchingTimer)
                print('')
                extractLessonLinks(driver)
                linksExtracted = True
            except:
                system('clear')
                print('Some error occured while fetching course lesson links. Please try later. Program aborted.')
                driver.quit()

            if linksExtracted == True:
                resp = getLinksFromFile()
                if resp[0] == False:
                    system('clear')
                    print('Links extraction failed. Program aborted.')
                    os.remove("links.txt")
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
                        print('Try again later. Program aborted.')
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
                                myProgressBar(lessonsExtractionTimer)
                                getH1Tags(driver)
                                getPTags(driver)
                                getliTags(driver)
                                print('Lesson: ', link, ' content added to course.txt file. Total lessons done = ', count + 1)
                                print('')
                                count = count + 1
                            system('clear')
                            parseFile()
                            print('All done. Content scrapped from a total of ', count, ' lessons.')
                            print('Open the course.txt file to see the results.')
                            if os.path.exists('temp.txt') == True:
                                os.remove("temp.txt")
                            driver.quit()
                        except:
                            system('clear')
                            print('Sorry! Something went wrong. Please try again later. Program aborted.')
                            driver.quit()

main()
