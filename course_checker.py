import requests
from twilio.rest import Client
import time
import json

# Class Object used to store the data for the course data
class CourseData(object):
	id = ""
	class_name = ""

	def __init__ (self,id, class_name):
		self.id = id
		self.class_name = class_name

 

# Specify the path to your JSON file
file_path = r'C:\Users\first\Desktop\New folder\UMD-Course-Checker\keys.json'

# Open the JSON file and load its contents
with open(file_path, 'r') as file:
    key_data = json.load(file)
    
with open(file_path, 'r') as file:
    account_sid_data = json.load(file)
    
# SMS Information
account_sid = account_sid_data['sid']
auth_token = key_data['key']
client = Client(account_sid, auth_token)


# Global Variables
class_inputs = []
seat_count = 0

# While loop used to process user input 
keep_going = 0
user_number = input("Please enter your number\n")
while keep_going == 0:
    
    user_input = input("Please Enter the class you want to track \nMake sure that you enter the class code in all CAPS for example ENGL101\n\n")
    user_section_input = input("Please Enter the section number for the class you want to track\n\n")
    second_user_input = input("Do you want to enter another class \n---> yes or no?\n\n")
    
    
    course_data = CourseData(user_section_input,user_input)

    class_inputs.append(course_data)

    if second_user_input !=  "yes":
        keep_going = 1

# Function is used to process the user data that was entered and print the outputs
def print_data():

	# Processes each CourseData Object
	for course_data in class_inputs:
		# Pulls the data using a API
		data = requests.get('https://api.umd.io/v1/courses/sections/' + course_data.class_name + '-' + course_data.id).json()


		# Processes and print out the course data
		for section_data in data:

			# Checks to see if the instructor is a TBA
			if(len(section_data.get('instructors')) == 0):
				print("Instructor: TBA")
			else:
				print(section_data.get('instructors'))

			# Prints out the seat count
			print("Seats left: " + section_data.get('open_seats') + "\n")
			seat_count = section_data.get('open_seats')


print_data()

# Start Message to check if the class if available 
message = client.messages.create(
				body="You have successfully set up your data in the script, you will receive a message when your class has seats available",
				from_="+18334320310",
				to="+1" + user_number
				)

# Used to Check if the seat count is greater then 0 it will send a SMS message to
# the user
while True:

	for course_data in class_inputs:
		# Pulls the data using a API
		data = requests.get('https://api.umd.io/v1/courses/sections/' + course_data.class_name + '-' + course_data.id).json()

		# Check to see if theres seats open for the course
		for section_data in data:
			if int(section_data.get('open_seats')) > 0:

				message = client.messages.create(
				body="Theres a seat available for " + course_data.class_name + " hurry and sign up!!!",
				from_="+18334320310",
				to="+1" + user_number
				)

				# Waits a day before checking again
				time.sleep(86400)


input("Enter Anything to close\n")
					
	
