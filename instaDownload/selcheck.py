import time
from datetime import datetime
import os
#Selenium libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
#BS4 libraries
import requests
import bs4
from bs4 import BeautifulSoup as soup


#region VARIABLES
links = list()
startTime = datetime.now()
log = "" + str(startTime) + "- Script initiated\n"
hrefList = list()
username = "asdn9651" #USERNAME here
password = "xohowib778@imailto.net" #PASSWORD here
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, executable_path="drivers\geckodriver.exe")
#endregion


#region Functions
def openBrowser():
    global log
    log += str(datetime.now())+ "- Browser load successful\n"
    driver.set_page_load_timeout(10)
    url = 'https://www.instagram.com/accounts/login/?source=auth_switcher'
    driver.get(url)
    driver.implicitly_wait(5)
    log += str(datetime.now())+ "- Instagram loaded successfully\n"
    print "Browser load successful"


def getAllATags():
    global log
    log += str(datetime.now()) + "- Fetching tags \n"
    last_height = driver.execute_script("return document.body.scrollHeight")
    new_height = -1
    postNum = 0
    while True:
        flex = driver.find_element_by_xpath("/html/body/span/section/main/div/div[2]/article/div/div") #XPATH for the FLEX
        elems = flex.find_elements_by_tag_name("a")
        for item in elems:
            tagHREF = item.get_attribute("href")
            if (tagHREF in hrefList) == False:
                hrefList.append(tagHREF)
                postNum += 1
                try:
                    print postNum, " parsing"
                    log += str(datetime.now()) + "- Parsing element "+ str(postNum) +"\n"
                    elementContentLinkGrab(item,postNum)
                except Exception as e:
                    log += str(datetime.now()) + "- Error parsing element \n"

        #now scrolling page
        print "scrolling now"
        scrollDOWN()
        new_height = driver.execute_script("return document.body.scrollHeight") 
        if new_height == last_height:
            print "no new content"
            break
        last_height = new_height
    print "Gathered all links"

def scrollDOWN():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def findElemType(elemen):
    #check type using Beautiful soup
    elem = soup(elemen.get_attribute('innerHTML'),"html.parser")
    try:
        if elem.find_all(attrs={"aria-label":"Carousel"}):
            return "Carousel"
        elif elem.find_all(attrs={"aria-label":"Video"}):
            return "Video"
        else:
            if elem.find_all('div'):
                return "Image"
    except Exception as e:
        print "Exception ::: ",e


def elementContentLinkGrab(singleElement, postNum):
    #singleElement is of type selenium Tag
    global log
    elemType = findElemType(singleElement)
    tagHREF = singleElement.get_attribute("href")[25:]
    #log += str(datetime.now()) + "- element type is "  + elemType + "\n"
    if elemType == "Video":
        singleElement.send_keys(Keys.ENTER)
        src = driver.find_element_by_tag_name('video').get_attribute('src')
        links.append([postNum, src])
        log += str(datetime.now()) +"- " + str(postNum) + " link added successfully\n" 
    elif elemType == "Image":
        src = singleElement.find_element_by_tag_name('img').get_attribute('src')
        links.append([postNum,src])
        log += str(datetime.now()) +"- " + str(postNum) + " link added successfully\n" 
    elif elemType == "Carousel":
        singleElement.send_keys(Keys.ENTER)
        carouselPath = driver.find_element_by_xpath("html/body/div[3]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/ul")
        #time.sleep(.1)
        carousel_soup = soup(carouselPath.get_attribute('innerHTML'), "html.parser")
        totalItems = len(carousel_soup)
        all_li_elements = list()
        for i in range(0,totalItems):
            try:
                carousel_soup = soup(carouselPath.get_attribute('innerHTML'), "html.parser")
                liElem = carousel_soup.contents[i]
                all_li_elements.append(liElem)
            except Exception as e:
                print e
            #Finding the next button on carousel
            if len(all_li_elements) <  totalItems:
                try:
                    #This finds the right carousel chevron button and clicks on it
                    right_button = driver.find_element_by_xpath("//*[contains(@class, 'RightChevron')]").click()
                except Exception as e:
                    print e
        log += str(datetime.now()) + "- number of elements in carousel : " + str(len(all_li_elements)) + "\n"
        #Joing the list
        newHTMLCarousel = ''
        for joinItem in all_li_elements:
            newHTMLCarousel += str(joinItem)
        newCarouselSoup = soup(newHTMLCarousel,"html.parser")
        itemNo = 0
        for item in newCarouselSoup:
            itemNo += 1
            if item.find('video'):
                postFileName = str(postNum) + "(" + str(itemNo) + ")"
                links.append([postFileName ,item.find('video')['src']])
                log += str(datetime.now()) +"- " + str(postFileName) + " link added successfully\n" 
            else:
                postFileName = str(postNum) + "(" + str(itemNo) + ")"
                links.append([postFileName ,item.find('img')['src']])
                log += str(datetime.now()) +"- " + str(postFileName) + " link added successfully\n" 

def downloadLinks():
    global log

    #Setting folders
    time = datetime.now()
    timeStamp = str(time.date()) + ' ' + str(time.hour) + str(time.minute) + str(time.second)
    dirName = 'downloads/' + timeStamp
    if not os.path.exists(dirName):
        os.makedirs(dirName)
        print("Directory " , dirName ,  " created ")
        log += "Folder created successfully\n"
    else:    
        print("Directory " , dirName ,  " could not be created")
        log += "Folder creation Error\n"

    #Downloading files
    fileNumber = 0
    log += str(datetime.now()) + "- Initiated DOWNLOAD process\n"
    for file in links:
        fileNumber += 1
        log += str(datetime.now()) + "- file " + str(fileNumber) + " - "
        try:
            r = requests.get(file[1])
            filename = str(file[0])
            if r.headers['content-type'] == "video/mp4":
                loc = "{0}/{1}.mp4".format(dirName, filename)
            elif r.headers['content-type'] == "image/jpeg":
                loc = "{0}/{1}.jpeg".format(dirName, filename)
            else:
                print "Unknown extension"
            with open(loc, 'wb') as f:
                f.write(r.content)
            print filename , "downloaded"
            log += "download successful\n"
        except:
            log += str(datetime.now()) + "- error downloading\n" 
        
    

#endregion

#region MainCode

log += str(datetime.now())+ "- Selenium initialization begin\n"

#region Open Instagram login page
try:
    openBrowser()
except Exception as e:
    log += str(datetime.now())+ "- Error loading webpage"
    print "Error loading browser"
#endregion


try:
    #region SignIn and navigate to Saved posts page
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
    print "Reached Saved tab"
    #endregion
    #Gathering all links
    try:
        print "Getting links INITIATED"
        getAllATags()
    except Exception as e:
        log += str(datetime.now()) + "- Error getting tag \n" + str(e)

    try:
        log += str(datetime.now()) + "- Writing links to downloadLinks.txt \n"
        print "Writing downloadLinks.txt -"
        with open('downloadLinks.txt', 'w') as f:
            for item in links:
                f.write("%s\n" % item)  
        print "successful \n"
    except Exception as e:
        log += str(datetime.now()) + "- Error writing downloading links \n"
        print "failed \n"
    

    log += "TOTAL " + str(len(links)) +" FILES TO DOWNLOAD\n"
    print str(len(links)) , " files to download "

    #Download all files
    print "download begin"
    try:
        downloadLinks()
        log += str(datetime.now()) + "- All files downloaded successfully \n"
    except Exception as e:
        print e
        log += str(datetime.now()) + "- Error downloading \n" + str(e)
    
finally:
    time.sleep(0.1)
    elapsedTime = datetime.now() - (startTime)
    timeTaken = str(divmod(elapsedTime.total_seconds(), 60))
    log += "Time elapsed - " + timeTaken + "\n"
    print "Time elapsed - " , str(timeTaken)
    log += "Quitting browser****************************************"
    driver.quit()
    print "Browser closed"
    print("Writing log to log.txt")
    f= open("log.txt","w+")
    f.write(log)
    f.close()

#endregion