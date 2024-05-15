import requests
from bs4 import BeautifulSoup

url = "https://app.testudo.umd.edu/soc/search?courseId=CMSC351&sectionId=&termId=202308&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on"

result = requests.get(url)
filtered_divs = []



doc = BeautifulSoup(result.text ,"html.parser")
#print(doc.prettify())
#spam = doc.find("span",id="open-seats-count")
#seats = doc.find_all(text="Open:")
divs = doc.find_all('div', class_='section delivery-f2f')

for div in divs:
    span = div.find('span', class_='section-id')
    if span and span.text.strip() == '0101':
        filtered_divs.append(div)
        seat_span = div.find('span', class_='open-seats-count')
        if seat_span:
            print((int(seat_span.text.strip())))
    
for div in filtered_divs:
    print(div.prettify())
    print("---------------------------------------------------")
    print("\n")
print(len(filtered_divs))