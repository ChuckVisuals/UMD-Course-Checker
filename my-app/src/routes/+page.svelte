<script>
  import "../app.css";
  import "./course_checker.svelte";
  import axios from "axios";
  import { v4 as uuidv4 } from "uuid";
  import { createClient } from "@supabase/supabase-js";
  import { onMount } from "svelte";

  const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
  const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;
  const supabase = createClient(supabaseUrl, supabaseKey);

  let form_model = false;
  let class_name = "";
  let section = "";
  let isError = false;
  let class_array = [];
  let apiLinks = [];

  //local storage code
  let uniqueKey;
  console.log("here");

  if (typeof localStorage !== "undefined") {
    // Check if localStorage is defined (not in SSR)
    uniqueKey = JSON.parse(localStorage.getItem("uniqueKey"));

    if (!uniqueKey) {
      uniqueKey = uuidv4();
      localStorage.setItem("uniqueKey", JSON.stringify(uniqueKey));
    }
    console.log(uniqueKey);
  } else {
    // Handle the case when localStorage is not available (SSR)
    console.warn(
      "localStorage is not available in this environment (probably SSR)."
    );
  }

  //updates the table from the data based on device
  onMount(async () => {
    if (uniqueKey) {
      // Fetch all rows with the given uniqueKey
      const { data, error } = await supabase
        .from("data")
        .select("api_link")
        .eq("uniqueKey", uniqueKey);

      if (error) {
        console.error("Error fetching API links:", error.message);
      } else {
        // Extract API links from the data
        apiLinks = data.map((row) => row.api_link);
      }
    }
    console.log(apiLinks);
    for (const apiLink of apiLinks) {
      await printData(apiLink);
    }
  });

  //supabase db code
  async function add_class() {
    console.log(class_name);
    console.log(section);
    let link = `https://api.umd.io/v1/courses/sections/${class_name}-${section}`;

    try {
      //let response = await axios.get(link); //trying the link to make sure class is valid
      // Add the class_name and section to the Supabase table
      const { data, error } = await supabase.from("data").insert([
        {
          uniqueKey: uniqueKey,
          class_name: class_name.toUpperCase(),
          section: section,
          api_link: link,
        },
      ]);

      if (error) {
        console.error("Error adding data to Supabase:", error.message);
      } else {
        console.log("Data added to Supabase successfully:", data);
      }
    } catch (error) {
      console.error("Error:", error.message);
    }

    // Call the existing printData function to fetch and display the data
    printData(link);
    // Optionally, you can reset form fields or perform other actions after successful data addition
    class_name = "";
    section = "";
  }

  // Function is used to process the user data that was entered and print the outputs
  async function printData(link) {
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

  // Function to remove a class from the class_array
  async function removeClass(index, class_info) {
    const { data, error } = await supabase
      .from("data")
      .delete()
      .eq("class_name", class_info.course.toUpperCase())
      .eq("section", class_info.number)
      .eq("uniqueKey", uniqueKey);
    console.log(class_info.course);
    console.log(class_info.number);
    console.log(uniqueKey);

    if (error) {
      console.error("Error deleting from Supabase:", error.message);
      return;
    }

    class_array.splice(index, 1);
    class_array = [...class_array];
    console.log(class_info);
  }
  $: class_array; // Ensure reactivity
</script>

<div class="navbar bg-base-100">
  <div class="navbar-start">
    <div class="dropdown">
      <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          ><path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h7"
          /></svg
        >
      </div>
      <ul
        tabindex="0"
        class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52"
      >
        <li><a href="/user">Your Profile</a></li>
        <li><a href="/about">About</a></li>
      </ul>
    </div>
  </div>

  <div class="navbar-center">
    <a href="./" class="btn btn-ghost text-xl">UMD Course Checker</a>
  </div>

  <div class="navbar-end">
    <button class="btn m-4" on:click={() => (form_model = !form_model)}
      >Add another class
    </button>
    <button class="btn btn-ghost btn-circle">
      <div class="indicator">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          ><path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
          /></svg
        >
        <span class="badge badge-xs badge-primary indicator-item"></span>
      </div>
    </button>
  </div>
</div>

<div class="overflow-x-auto">
  <table class="table">
    <!-- head -->
    <thead>
      <tr>
        <th></th>
        <th>Professor</th>
        <th>Class</th>
        <th>Seats Available</th>
      </tr>
    </thead>
    <tbody>
      {#each class_array as classData, index (index)}
        <tr class="hover">
          <th>{index + 1}</th>
          <td
            >{classData.instructors.length > 0
              ? classData.instructors[0]
              : "TBA"}</td
          >
          <td>{classData.section_id}</td>
          <td>{classData.open_seats}</td>
          <td
            ><button on:click={() => removeClass(index, classData)}
              >Remove</button
            ></td
          >
        </tr>
      {/each}
    </tbody>
  </table>
</div>

{#if form_model}
  <div class="popup-container">
    <div
      class="w-screen h-screen fixed top-0 left-0 grid place-items-center backdrop-blur-lg bg-black/20"
    >
      <div
        class="flex justify-center gap-4 flex-col bg-base-100 p-8 rounded-xl shadow-xl"
      >
        <input
          type="text"
          placeholder="Class Name"
          bind:value={class_name}
          class="input input-bordered input-primary w-full max-w-xs px-4 py-2"
        />

        <input
          type="text"
          placeholder="Section Number"
          bind:value={section}
          class="input input-bordered input-primary w-full max-w-xs px-4 py-2"
        />

        <button
          class="btn bg-indigo-500 hover:bg-indigo-700 text-lg"
          on:click={add_class}
        >
          Submit
        </button>
        <button
          class="btn bg-indigo-500 hover:bg-indigo-700 text-lg"
          on:click={() => (form_model = !form_model)}
        >
          Go Back
        </button>
      </div>
      {#if isError}
        <div
          role="alert"
          class="alert alert-error flex justify-center max-w-md absolute inset-x-50 bottom-20"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="stroke-current shrink-0 h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            ><path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
            /></svg
          >
          <span>Error! Class Doesn't Exist</span>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  .alert-error {
    animation: fadeOut 3s ease-in-out; /* Set the duration of the fade-out animation */
  }

  @keyframes fadeOut {
    from {
      opacity: 1;
    }

    to {
      opacity: 0;
    }
  }
  .popup-container {
    position: fixed;
    top: 0%;
    left: 0%;
  }
</style>
