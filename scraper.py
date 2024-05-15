import requests
from bs4 import BeautifulSoup
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
print(url, key)
supabase: Client = create_client(url, key)


# gets the seat count from testudo for a specific class and section
def get_seats(class_name, section_id):
    url = f'https://app.testudo.umd.edu/soc/search?courseId={class_name.upper()}&sectionId=&termId=202401&_openSectionsOnly=on&creditCompare=%3E%3D&credits=0.0&courseLevelFilter=ALL&instructor=&_facetoface=on&_blended=on&_online=on&courseStartCompare=&courseStartHour=&courseStartMin=&courseStartAM=&courseEndHour=&courseEndMin=&courseEndAM=&teachingCenter=ALL&_classDay1=on&_classDay2=on&_classDay3=on&_classDay4=on&_classDay5=on'

    result = requests.get(url)
    filtered_divs = []

    doc = BeautifulSoup(result.text ,"html.parser")
    divs = doc.find_all('div', class_='section delivery-f2f')

    for div in divs:
        span = div.find('span', class_='section-id')
        if span and span.text.strip() == section_id:
            filtered_divs.append(div)
            seat_span = div.find('span', class_='open-seats-count')
            if seat_span:
                return int(seat_span.text.strip())
            
print(get_seats('CMSC131', '0101'))


def update_seats(class_name, section_id):
    
    seats = get_seats(class_name, section_id)
    supabase.table('data').update({'open_seats': seats}).eq('class_name', class_name).execute()


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

print("Done")