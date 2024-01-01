<script>
  import "../app.css";
  import "./course_checker.svelte";
  import axios from 'axios';

  let form_model = false;
  let class_name = "";
  let section = "";
  let isError = false;
  let class_array = [];

  function add_class(){
    console.log(class_name)
    console.log(section)
    printData(class_name, section)
    class_name = "";
    section = "";
  }

  // Function is used to process the user data that was entered and print the outputs
  async function printData(class_name, id) {
    try {
      let response = await axios.get(
        `https://api.umd.io/v1/courses/sections/${class_name}-${id}`
      );
      let data = response.data;

      if (data) {
          form_model = false
          isError = false
          console.log(data[0])
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
      }
    } catch (error) {
      isError = true;
      console.error("Error fetching data:", error.message);
      
    }
    console.log(class_array)
  }

  // Function to remove a class from the class_array
  function removeClass(index) {
    class_array.splice(index, 1);
  }
  $: class_array; // Ensure reactivity
</script>

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
      {#each class_array as classData, index (index)}
        <tr class="hover">
          <th>{index + 1}</th>
          <td>{classData.instructors.length > 0 ? classData.instructors[0] : 'TBA'}</td>
          <td>{classData.section_id}</td>
          <td>{classData.open_seats}</td>
          <td><button on:click={() => removeClass(index)}>Remove</button></td>
        </tr>
      {/each}
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

    <button class="btn bg-indigo-500 hover:bg-indigo-700 text-lg" on:click={add_class}> Submit </button>
    <button class="btn bg-indigo-500 hover:bg-indigo-700 text-lg" on:click={() => form_model = !form_model}> Go Back </button>
      
  </div>
  {#if isError}
    <div role="alert" class="alert alert-error ">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
      <span>Error! Class Doesn't Exist</span>
    </div>
    {/if}
</div>
{/if}