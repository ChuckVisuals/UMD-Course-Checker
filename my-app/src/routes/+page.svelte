<script>
    import "../app.css";
    import "./course_checker.svelte";
    import axios from 'axios';

    let form_model = false;
    let class_name = "";
    let section = "";
    let class_array = [];

    function add_class(){
      console.log(class_name)
      console.log(section)
      printData(class_name, section)
      class_name = "";
      section = "";
      form_model = false
    }

  // Function is used to process the user data that was entered and print the outputs
    async function printData(class_name, id) {
    try {
      let response = await axios.get(
        `https://api.umd.io/v1/courses/sections/${class_name}-${id}`
      );
      let data = response.data;

      if (data) {
        // For loop used to access the data in the JSON file returned by the API
        data.forEach((sectionData) => {
          // Checks to see if the instructor is TBA
          if (sectionData.instructors.length === 0) {
            console.log("Instructor: TBA");
          } else {
            console.log(sectionData.instructors[0]);
          }

          // Prints out the seat count
          console.log(`Seats left: ${sectionData.open_seats}\n`);
        });
      } else {
        console.error("No data received from the API");
      }
    } catch (error) {
      console.error("Error fetching data:", error.message);
    }
  }
</script>

<style>
 
</style>

<div class="navbar bg-base-100">
  <div class="flex-1">
    <a href="./" class="btn btn-ghost text-xl">UMD Course Checker</a>
  </div>
  <div class="navbar-end">
    <button class="btn" on:click={() => form_model = !form_model}>Add another class </button>
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
      <!-- row 1 -->
      <tr class="hover">
        <th>1</th>
        <td>Cy Ganderton</td>
        <td>Quality Control Specialist</td>
        <td>Blue</td>
      </tr>
      <!-- row 2 -->
      <tr class="hover">
        <th>2</th>
        <td>Hart Hagerty</td>
        <td>Desktop Support Technician</td>
        <td>Purple</td>
      </tr>
      <!-- row 3 -->
      <tr class="hover">
        <th>3</th>
        <td>Brice Swyre</td>
        <td>Tax Accountant</td>
        <td>Red</td>
      </tr>
    </tbody>
  </table>
</div>


{#if form_model}
<div class="w-screen h-screen fixed top-0 left-0 grid place-items-center backdrop-blur-lg bg-black/20">
  <div class="flex justify-center gap-4 flex-col bg-base-100 p-8 rounded-xl shadow-xl">
    <input type="text" placeholder="Class Name" bind:value={class_name}
        class="input input-bordered input-primary w-full max-w-xs px-4 py-2 ">

    <input type="text" placeholder="Section Number" bind:value={section}
        class="input input-bordered input-primary w-full max-w-xs px-4 py-2">
    <button class="btn bg-indigo-500 hover:bg-indigo-700 text-lg" on:click={add_class}> submit <button>
  </div>
</div>
{/if}