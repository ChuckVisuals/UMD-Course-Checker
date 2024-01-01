<script>
    // Function is used to process the user data that was entered and print the outputs
    export function printData(class_name, id) {
    // Processes each CourseData Object
    classInputs.forEach(async () => {
        // Pulls the data using an API
        try {
        let response = await axios.get(
            `https://api.umd.io/v1/courses/sections/${class_name}-${id}`
        );
        let data = response.data;

        // For loop used to access the data in the JSON file returned by the API
        data.forEach((sectionData) => {
            // Checks to see if the instructor is TBA
            if (sectionData.instructors.length === 0) {
            console.log("Instructor: TBA");
            } else {
            console.log(sectionData.instructors);
            }

            // Prints out the seat count
            console.log(`Seats left: ${sectionData.open_seats}\n`);
            seatCount = sectionData.open_seats;
        });
        } catch (error) {
        console.error("Error fetching data:", error.message);
        }
    });
    }
  </script>
  