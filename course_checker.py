import requests

class_inputs = []

keep_going = 0
while keep_going == 0:

    user_input = input("Please Enter the class you want to track \nPlease make sure that you enter the class code in all CAPS for example ENGL101\n")
    second_user_input = input("Do you want to enter another class \n---> yes or no?\n")

    class_inputs.append(user_input)

    if second_user_input !=  "yes":
        keep_going = 1

def print_data():

	for user_input_data in class_inputs:
		parameters ={ 
    	"course_id": user_input_data,   
		}
        
		data = requests.get('https://api.umd.io/v1/courses/sections', params=parameters).json()

		for section_data in data:
			if(len(section_data.get('instructors')) == 0):
				print("TBA")
			else:
				print(section_data.get('instructors'))

			print(section_data.get('open_seats'))


print_data()
					
	
