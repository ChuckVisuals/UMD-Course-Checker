# Course Data Tracker

The Course Data Tracker is a Python script designed to help you monitor and retrieve details about specific courses and their sections through the UMD.io API. Here's a guide on how to use and install the script:

## Prerequisites

Ensure the following prerequisites are met:

- Python 3.x installed on your system.
- The `requests` library is required. Install it by executing the following command in your terminal:

```bash
pip install requests
```

## Installation

Follow these steps to install the Course Data Tracker:

1. Clone or download the script to your local machine.
2. Install the `requests` library as instructed above.

## Usage

To utilize the script:

1. Run the script using a Python interpreter.
2. Enter the class code (in all CAPS) and section number for the course you wish to track when prompted.
3. To track additional courses, respond with "yes" when prompted.
4. After entering all desired courses, the script will retrieve data from the UMD.io API, presenting the instructor(s) and the number of open seats for each section.
5. The program will pause after displaying results. Press any key to close the script.

**Note:** The script relies on the UMD.io API to obtain course data. Ensure your internet connection is active to access the API.

## Acknowledgments

This script makes use of the UMD.io API for retrieving course data. Special acknowledgments to the UMD.io API for providing this functionality.