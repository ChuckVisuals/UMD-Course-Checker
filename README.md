Course Data Tracker

This Python script allows you to track and retrieve information about specific courses and their sections using the UMD.io API. The script prompts the user to enter the class code and section number of the courses they want to track. It then fetches the data from the API and prints out the instructor(s) and the number of open seats for each section.

Prerequisites
Python 3.x
requests library
Installation
Clone or download the script to your local machine.
Install the requests library by running the following command in your terminal:
Copy code
pip install requests
Usage
Run the script using a Python interpreter.
Enter the class code (in all CAPS) and section number for the course you want to track when prompted.
If you want to track additional courses, enter "yes" when asked.
Once you have entered all the desired courses, the script will fetch the data from the UMD.io API and display the instructor(s) and number of open seats for each section.
The program will pause after displaying the results. Press any key to close the script.
Please note that this script relies on the UMD.io API to retrieve course data. Make sure you have an active internet connection to access the API.

Acknowledgments
This script utilizes the UMD.io API to retrieve course data.