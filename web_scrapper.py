import requests
from bs4 import BeautifulSoup

# URL of the Testudo page you want to scrape
url = 'https://app.testudo.umd.edu/soc/202308/CMSC/CMSC351'

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the element that contains the seat count
seat_count_element = soup.find('span', class_='open-seats-count')

print(seat_count_element)

# Extract the seat count value
seat_count = seat_count_element.text if seat_count_element else 'Not available'

# Print the seat count
print(f"Seat count: {seat_count}")