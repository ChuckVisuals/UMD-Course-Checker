import requests
from twilio.rest import Client
import time
import json
import time 

# Class Object used to store the data for the course data
class CourseData(object):
	id = ""
	class_name = ""

	def __init__ (self,id, class_name,mytime):
		self.id = id
		self.class_name = class_name
		self.mytime = mytime
		self.processed = 0
		self.seat_open = False

 

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
    
	#Stores the time when the object was created
    start_time = time.time() 
    
    course_data = CourseData(user_section_input,user_input, start_time)

    class_inputs.append(course_data)

    if second_user_input !=  "yes":
        keep_going = 1
	


# Function is used to process the user data that was entered and print the outputs
def print_data():

	# Processes each CourseData Object
	for course_data in class_inputs:
		# Pulls the data using a API
		data = requests.get('https://api.umd.io/v1/courses/sections/' + course_data.class_name + '-' + course_data.id).json()


		# For loop used to access the data in the json file returned by the API
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

	# Processes each CourseData Object
	for course_data in class_inputs:
		# Pulls the data using a API
		data = requests.get('https://api.umd.io/v1/courses/sections/' + course_data.class_name + '-' + course_data.id).json()

		# For loop used to access the data in the json file returned by the API
		for section_data in data:
			
			# Checks the time and updates if course has been processed or not
			if time.time() - course_data.mytime > (1):
				course_data.processed = 0
				new_time = time.time()
				course_data.mytime = new_time


			#If (course is not processed and have seats left)
			if course_data.processed == 0 and int(section_data.get('open_seats')) > 0 and course_data.seat_open == False:

				course_data.processed = 1

				message = client.messages.create(
				body="Theres a seat available for " + course_data.class_name + " hurry and sign up!!!",
				from_="+18334320310",
				to="+1" + user_number
				)
				course_data.seat_open = True
				# Waits a day before checking again
				# time.sleep(86400)


input("Enter Anything to close\n")
					
	
