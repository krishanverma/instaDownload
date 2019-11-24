import bs4
import requests
import urllib
from bs4 import BeautifulSoup as soup

star = "some\n"
star += "thing"
num = 5
star += str(num) + "here"
print(star)
#myurl= "fullHTML.html"
#myurl= "recordedHTML.html"

#flexHTML = urllib.urlopen(myurl)
#page_soup = soup(flexHTML, "html.parser")

#print("Len ",len(page_soup.find_all(True, recursive=False))) # . find_all(True) here deletes all elements which are empty and recurseive false stops cursor from returning every single object

#number of rows
#rows = page_soup.find_all(True, recursive=False)
#print(len(rows[0].find_all(True, recursive=False)))

#Number of columns in each row
#for row in rows:
#    print("Length of this row ::",len(row.find_all(True, recursive=False)))

#singleElement = urllib.urlopen("singleElement.html")
#elem_soup = soup(singleElement,"html.parser")
#
#print("length : ",len(elem_soup))
#
#print("num of elems : ",len(elem_soup.a))
## elements in a 
#a_elements = elem_soup.a.find_all(True, recursive = False)
#print(a_elements[1].span["aria-label"])


#diffElems = urllib.urlopen("singleElement.html")
#elem_soup = soup(diffElems,"html.parser")
#src = elem_soup.find('img')['src']
#
#print(src)

#counter = 0
#for elem in elem_soup.find_all(True, recursive=False):
#    counter = counter +1
#    print "Element no : ", counter
#    #print "$$$", str(elem.div),"$$$"
#    if elem.find_all(attrs={"aria-label":"Carousel"}):
#        print "Carousel"
#    elif elem.find_all(attrs={"aria-label":"Video"}):
#        print "Video"
#    else:
#        if elem.find_all('div'):
#            print "Image"
#        else:
#            print "EMPTY"
#

#/html/body/span/section/main/div/div[2]/article/div/div/div[1]/div[1]/a
#/html/body/span/section/main/div/div[2]/article/div/div/div[1]/div[2]/a
#/html/body/span/section/main/div/div[2]/article/div/div/div[1]/div[3]/a
#/html/body/span/section/main/div/div[2]/article/div/div/div[2]/div[1]/a
#/html/body/span/section/main/div/div[2]/article/div/div/div[2]/div[2]/a
#/html/body/span/section/main/div/div[2]/article/div/div/div[2]/div[3]/a
#/html/body/span/section/main/div/div[2]/article/div/div/div[3]/div[1]/a


#print('Beginning file download with requests')
#
#url = 'https://instagram.fybz2-2.fna.fbcdn.net/vp/4cfde618fa6ccd1b966de11f92cea579/5DC92AAB/t50.2886-16/77210978_1343855609122300_884469628612897661_n.mp4?_nc_ht=instagram.fybz2-2.fna.fbcdn.net&_nc_cat=104'
#r = requests.get(url)
#if r.headers['content-type'] == "video/mp4":
#    loc = 'downloads/file.mp4'
#elif r.headers['content-type'] == "image/jpeg":
#    loc = 'downloads/file.jpeg'
#with open(loc, 'wb') as f:
#    f.write(r.content)
#
## Retrieve HTTP meta-data
#print(r.status_code)
#print(r.headers)
#print(r.encoding)