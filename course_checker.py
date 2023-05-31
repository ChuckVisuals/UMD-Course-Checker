import requests


# Class Object used to store the data for the course data
class CourseData(object):
	id = ""
	class_name = ""

	def __init__ (self,id, class_name):
		self.id = id
		self.class_name = class_name


class_inputs = []

# While loop used to process user input 
keep_going = 0
while keep_going == 0:

    user_input = input("Please Enter the class you want to track \nMake sure that you enter the class code in all CAPS for example ENGL101\n")
    user_section_input = input("Please Enter the section number for the class you want to track\n")
    second_user_input = input("Do you want to enter another class \n---> yes or no?\n")
    
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
			print("Seats left:" + section_data.get('open_seats'))


print_data()

input("Enter Anything to close\n")
					
	
