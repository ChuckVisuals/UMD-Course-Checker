import { createClient } from "@supabase/supabase-js";
import { v4 as uuidv4 } from 'uuid';
import axios from "axios";
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);


// Function is used to process the user data that was entered and print the outputs
export async function printData(link) {
    try {
        let response = await axios.get(link);
        let data = response.data;

        if (data[0]) {
            form_model = false;
            isError = false;
            console.log(data[0]);
            data = data[0];
            class_array = [...class_array, data];
            // Checks to see if the instructor is TBA
            if (data.instructors.length === 0) {
                console.log("Instructor: TBA");
            } else {
                console.log(data.instructors[0]);
            }

            // Prints out the seat count
            console.log(`Seats left: ${data.open_seats}\n`);
        } else {
            console.error("No data received from the API");
            isError = true;
        }
    } catch (error) {
        isError = true;
        console.error("Error fetching data:", error.message);
        setTimeout(() => {
            isError = false; // Reset isError state after a delay
        }, 3000); // Adjust the delay (in milliseconds) based on the fade-out duration
    }
    console.log(class_array);
}

//=================================================================================================================//

//supabase db code
export async function add_class(uniqueKey, class_name, section, class_array) {

    try {
        let link = `https://api.umd.io/v1/courses/sections/${class_name}-${section}`;
        let response = await axios.get(link); //trying the link to make sure class is valid

        console.log(response.data);

        let apiData = response.data;
        console.log(apiData[0].instructors);

        // Add the class_name and section to the Supabase table
        const { data, error } = await supabase.from("data").insert([
            {
                uniqueKey: uniqueKey,
                class_name: class_name.toUpperCase(),
                section: section,
                api_link: link,
                instructors: apiData[0].instructors.length > 0 ? apiData[0].instructors : ['TBA'],
                open_seats: apiData[0].open_seats,
            },
        ]);


        if (error) {
            console.error("Error adding data to Supabase:", error.message);
            return fetchData();

        } else {
            console.log("Data added to Supabase successfully:", data);
            return fetchData();
        }
    } catch (error) {
        console.error("Error:", error.message);
        return fetchData();
    }
}

//==============================================================================================================//
//returning the unique key saved in local storage
export function setLocalStorage() {
    let uniqueKey;

    if (typeof window !== "undefined") {
        uniqueKey = JSON.parse(localStorage.getItem("uniqueKey"));

        if (!uniqueKey) {
            uniqueKey = uuidv4();
            localStorage.setItem("uniqueKey", JSON.stringify(uniqueKey));
        }
        console.log(uniqueKey);
    } else {
        console.warn(
            "localStorage is not available in this environment (probably SSR).",
        );
    }
    return uniqueKey;
}

//==============================================================================================================//

// Function to remove a class from the class_array
export async function removeClass(uniqueKey, index, class_info, class_array) {

    console.log(class_info);
    const { data, error } = await supabase
        .from("data")
        .delete()
        .eq("class_name", class_info.class_name.toUpperCase())
        .eq("section", class_info.section)
        .eq("uniqueKey", uniqueKey);
    console.log(class_info.class_name);
    console.log(class_info.section);
    console.log(uniqueKey);

    if (error) {
        console.error("Error deleting from Supabase:", error.message);
        return;
    }

    class_array.splice(index, 1);
    class_array = [...class_array];
    console.log(class_info);

    return class_array;
}

//==============================================================================================================//
//Helper function inside of ulit.js
async function fetchData() {

    let uniqueKey = setLocalStorage();
    // Fetch all rows with the given uniqueKey
    const { data, error } = await supabase
        .from("data")
        .select("*")
        .eq("uniqueKey", uniqueKey);

    console.log(data);

    if (error) {
        console.error("Error fetching API links:", error.message);
    }
    return data;
}

//==============================================================================================================//

export async function checkUserExists(uniqueKey) {
    if (uniqueKey) {
        const { data, error } = await supabase
            .from("user_data")
            .select("name, email")
            .eq("uniqueKey", uniqueKey);
        console.log(data);

        if (error) {
            console.error("Error fetching API links:", error.message);
            return false;
        } else {
            if (data.length > 0) {
                return true;
            } else {
                return false;
            }
        }
    }
    return false;
}

//==============================================================================================================//   
export async function checkOpenClasses(uniqueKey) {

    let openClasses = 0;
    // Fetch all rows with the given uniqueKey
    const { data, error } = await supabase
        .from("data")
        .select("*")
        .eq("uniqueKey", uniqueKey);

    if (error) {
        console.error("Error fetching API links:", error.message);
    } else {
        console.log(data);
        for (let i = 0; i < data.length; i++) {
            if (data[i].sent == true) {
                openClasses++;
            }
        }
        console.log(openClasses);
    }
    return openClasses;
}