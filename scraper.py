import requests
from bs4 import BeautifulSoup
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import time
from random import randint

#USED FOR LOCAL DEV ONLY
load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
password = os.getenv("PASSWORD")

#USED FOR GH ACTIONS ONLY
url: str = os.environ["url"]
key: str = os.environ["key"]
password: str = os.environ["PASSWORD"]
print(url, key)

#GLOBAL STUFF
email = "umdcoursechecker@outlook.com"
supabase: Client = create_client(url, key)


#Class for open class data
class ClassData:
    def __init__(self, key, name, section, teacher):
        self.key = key
        self.name = name
        self.section = section
        self.teacher = teacher
        
    def print(self):
        print(f"Key: {self.key}, Name: {self.name}, Section: {self.section}, Teacher: {self.teacher}")


# gets the seat count from testudo for a specific class and section
def get_seats(class_name, section_id):
    url = f'https://app.testudo.umd.edu/soc/search?courseId={class_name.upper()}&sectionId=&termId=202408&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on'

    result = requests.get(url)
    filtered_divs = []

    doc = BeautifulSoup(result.text ,"html.parser")
    #print(doc.prettify())
    divs = doc.find_all('div', class_=['section delivery-f2f','section delivery-online','section delivery-blended'])

    for div in divs:
        span = div.find('span', class_='section-id')
        if span and span.text.strip() == section_id:
            filtered_divs.append(div)
            seat_span = div.find('span', class_='open-seats-count')
            if seat_span:
                return int(seat_span.text.strip())
            
#print("Seats" + str(get_seats('CMSC335', '0201')))


def update_seats(class_name, section_id):
    
    seats = get_seats(class_name, section_id)
    supabase.table('data').update({'open_seats': seats}).eq('class_name', class_name).eq('section', section_id).execute()


# Loop through each row in the database and update the seat count
def update_all_seats():
    # Fetch all rows from the database table
    rows = supabase.table('data').select('*').execute()
    
    # Iterate through each row
    for row in rows.data:
        class_name = row['class_name']
        section_id = row['section']
        
        # Update the seat count for the current row
        update_seats(class_name, section_id)


# Call the function to update all seats
update_all_seats()


MAX_RETRIES = 5
def sendEmails():
    class_array = []
    # Fetch all rows from the database table
    rows = supabase.table('data').select('*').execute()
    
    # Iterate through each row
    for row in rows.data:
        if row["open_seats"] != None and row["open_seats"] > 0 and row["sent"] == False:
            newclass = ClassData(row['uniqueKey'],row["class_name"], row["section"], row["instructors"])
            class_array.append(newclass)
    
    
    retries = 0
    while retries < MAX_RETRIES:
        
        #trys to send the email atleast 5 times
        try:
            server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            server.starttls()
            server.login(email, password)
            
            # Fetch all rows from the database table
            for classInfo in class_array:
                row = supabase.table('user_data').select('*').eq('uniqueKey', classInfo.key).execute()
                
                # Reduce errors if user is not found etc
                if len(row.data) > 0:
                    try:
                        print("sending")
                        server.sendmail(email, row.data[0]['email'].strip(), f"Subject: {classInfo.name} {classInfo.section} is now open!\n\nHello, {row.data[0]['name']}!\n\nThe class {classInfo.name} {classInfo.section} is now open! Go to testudo to register now!")
                        supabase.table('data').update({'sent': True}).eq('uniqueKey', row['uniqueKey']).eq('class_name', row['class_name']).execute()
                        print("sent to " + row.data[0]['email'])
                    except Exception as e:
                        print("Error sending email:", e)
                
            server.quit()
            break
        except smtplib.SMTPAuthenticationError as e:
            print(f"SMTPAuthenticationError: {e}")
            retries += 1
            wait_time = 2 ** retries + randint(0, 1000) / 1000  # Exponential backoff with jitter
            print(f"Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break  # Exit the loop if an unexpected error occurs

            
sendEmails()

print("Done")