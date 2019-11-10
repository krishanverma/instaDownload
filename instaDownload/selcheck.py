import time
from datetime import datetime
#Selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
#BS4 libraries
import requests
import bs4
from bs4 import BeautifulSoup as soup


#region VARIABLES
links = list()
startTime = datetime.now()
log = "" + str(startTime) + "- Script initiated\n"
#endregion


#region Functions

def findElemType(elem):
    #check type
    if elem.find_all(attrs={"aria-label":"Carousel"}):
        return "Carousel"
    elif elem.find_all(attrs={"aria-label":"Video"}):
        return "Video"
    else:
        if elem.find_all('div'):
            return "Image"
        else:
            return "EMPTY"


def elementContentLinkGrab(singleElement, rowNum, colNum):
    global log
    elemType = findElemType(singleElement)
    log += str(datetime.now()) + "- element type is "  + elemType + "\n"
    if elemType == "Video":
        hrefXPATH = "html/body/span/section/main/div/div[2]/article/div/div/div[{0}]/div[{1}]/a".format(rowNum+1,colNum+1)
        elemSnip = driver.find_element_by_xpath(hrefXPATH)
        elemSnip.send_keys(Keys.ENTER)
        #video = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[1]/div/div/div[3]")
        # WE CAN USE BEAUTIFUL SOUP HERE
        videoPathElem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/article/div[1]/div/div/div[1]/div/div/video")
        src = videoPathElem.get_attribute("src")
        #elementNumber = (rowNum+1)*
        links.append([rowNum, colNum,src])
        log += str(datetime.now()) + "- element added successfully\n" 
    elif elemType == "Image":
        src = singleElement.find('img')['src']
        links.append([rowNum, colNum,src])
        log += str(datetime.now()) + "- element added successfully\n" 
    elif elemType == "Carousel":
        # XPATH for ul containing all images /html/body/div[3]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/ul
        hrefXPATH = "html/body/span/section/main/div/div[2]/article/div/div/div[{0}]/div[{1}]/a".format(rowNum+1,colNum+1)
        elemSnip = driver.find_element_by_xpath(hrefXPATH)
        elemSnip.send_keys(Keys.ENTER)
        carouselPath = driver.find_element_by_xpath("html/body/div[3]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/ul")
        time.sleep(.1)
        carousel_soup = soup(carouselPath.get_attribute('innerHTML'), "html.parser")
        itemsSrcs = carousel_soup.find_all('video')
        for vidItem in itemsSrcs:
            for sibling in vidItem.next_siblings:
                sibling.decompose()
        itemsSrcs += carousel_soup.find_all('img')
        log += str(datetime.now()) + "- number of elements in carousel : " + str(len(itemsSrcs)) + "\n"
        for oneElem in itemsSrcs:
            src = oneElem['src']
            links.append([rowNum, colNum,src])
            log += str(datetime.now()) + "- element added successfully\n" 
    elif elemType == "EMPTY":
        log += str(datetime.now()) + "- element was empty\n" 
    


def gettingLinks(flex_soup):
    #Creating rows element and counting rows
    global log
    log += str(datetime.now()) + "- Gathering links now\n"
    rows = flex_soup.find_all(True, recursive=False)
    log += str(datetime.now()) + "- Number of rows found" + str(len(rows)) + "\n"
    rowNumber = 0
    for row in rows:
        rowElements = row.find_all(True, recursive=False)
        columnNumber = 0
        for singleElement in rowElements:
            log += str(datetime.now()) + "- Working on element " + str(rowNumber) + "," + str(columnNumber) + "\n"
            try:
                elementContentLinkGrab(singleElement,rowNumber,columnNumber)
            except:
                log += str(datetime.now()) + "- error getting element" 
            columnNumber = columnNumber + 1
        rowNumber = rowNumber + 1
    

def downloadLinks():
    #Downloading files
    global log
    fileNumber = 0
    log += str(datetime.now()) + "- Initiated DOWNLOAD PROCESS\n" 
    for file in links:
        fileNumber += 1
        log += str(datetime.now()) + "- file " + str(fileNumber) + " - "
        try:
            r = requests.get(file[2])
            filename = str(fileNumber)
            if r.headers['content-type'] == "video/mp4":
                loc = "downloads/{0}.mp4".format(filename)
            elif r.headers['content-type'] == "image/jpeg":
                loc = "downloads/{0}.jpeg".format(filename)
            else:
                print "Unknown extension"
            with open(loc, 'wb') as f:
                f.write(r.content)
            
            log += "download successful\n"
        except:
            log += str(datetime.now()) + "- error downloading\n" 
        
    

#endregion

#region MainCode

log += str(datetime.now())+ "- Selenium initialization begin\n"
driver = webdriver.Firefox(executable_path="drivers\geckodriver.exe")
#If you want to use chrome driver
#driver = webdriver.Chrome(executable_path="drivers\chromedriver.exe")
driver.set_page_load_timeout(10)
url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
driver.get(url)
wait = WebDriverWait(driver, 10)
driver.implicitly_wait(5)
log += str(datetime.now())+ "- Instagram Loaded\n"
try:
    username = "asdn9651"
    password = "xohowib778@imailto.net"
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    log += str(datetime.now()) + "- Username and Password fields populated\n"
    driver.implicitly_wait(5)
    login = driver.find_element_by_xpath("/html/body/span/section/main/div/article/div/div[1]/div/form/div[4]")
    login.click()
    log += str(datetime.now()) + "- Login pressed\n"
    driver.implicitly_wait(5)
    not_now = driver.find_element_by_xpath("/html/body/div[3]/div/div/div[3]/button[2]")
    not_now.click()
    log += str(datetime.now()) + "- Not now box clicked\n"
    driver.implicitly_wait(5)
    prof = driver.find_element_by_xpath("/html/body/span/section/nav/div[2]/div/div/div[3]/div/div[3]/a")
    prof.click()
    log += str(datetime.now()) + "- Profile page opened\n"
    saved = driver.find_element_by_xpath("/html/body/span/section/main/div/div[1]/a[3]")
    saved.click()
    log += str(datetime.now()) + "- Saved tab opened\n"

    #Getting all the rows and columns of post snips
    flex = driver.find_element_by_xpath("/html/body/span/section/main/div/div[2]/article/div/div") #XPATH for the FLEX
    log += str(datetime.now()) + "- Flex data gathered\n"
    log += str(datetime.now()) + "- Using beautiful Soup\n"
    #Gathering HTML and creating BS element
    flex_soup = soup(flex.get_attribute('innerHTML'), "html.parser")
    gettingLinks(flex_soup)

    log += "TOTAL " + str(len(links)) +" FILES TO DOWNLOAD\n" 
    #Download all files
    downloadLinks()
    
finally:
    time.sleep(0.3)
    log += "All Files downloaded\n" 
    log += "Quitting browser****************************************"
    print("Writing log to log.txt")
    f= open("log.txt","w+")
    f.write(log)
    f.close()
    driver.quit()

#endregion