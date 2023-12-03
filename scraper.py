import requests
from bs4 import BeautifulSoup

url = "https://app.testudo.umd.edu/soc/search?courseId=CMSC351&sectionId=&termId=202308&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"

result = requests.get(url)



doc = BeautifulSoup(result.text ,"html.parser")
spam = doc.find("span",id="open-seats-count")
#seats = doc.find_all(text="Open:")

print(spam)