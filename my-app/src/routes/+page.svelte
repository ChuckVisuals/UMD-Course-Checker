<script>
  import "../app.css";
  import Navbar from "$lib/navbar.svelte";
  import { checkUserExists, setLocalStorage, removeClass } from "$lib/utils.js";
  import { classData } from "$lib/store.js";

  import { createClient } from "@supabase/supabase-js";
  import { onMount } from "svelte";

  const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
  const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;
  const supabase = createClient(supabaseUrl, supabaseKey);

  let class_array = [];
  let user_found = false;
  $: user_found;
  $: class_array; // Ensure reactivity
  let uniqueKey = setLocalStorage();
  let loading = true;
  let loading2 = true;
  let showAlert = true;

  classData.subscribe((value) => {
    console.log(value);
    class_array = value;
  });

  //gets the data from the db and updates the table
  async function fetchData() {
    if (uniqueKey) {
      // Fetch all rows with the given uniqueKey
      const { data, error } = await supabase
        .from("data")
        .select("*")
        .eq("uniqueKey", uniqueKey);

      class_array = data;
    }
  }

  //fetches the data from the db on page load
  onMount(() => {
    fetchData();
    setTimeout(() => {
      loading2 = false;
    }, 200); // waits for 200ms for smoother loading
    console.log("fetching data");
  });

  console.log(class_array);

  //Checks if the user exists in the db on page load
  onMount(() => {
    checkUserExists(uniqueKey).then((result) => {
      user_found = result;
      loading = false;
      console.log("fetching user");
    });
  });

  //Shows alert on new page load
  onMount(() => {
    setTimeout(() => {
      showAlert = false;
    }, 5000); // waits for 5 seconds
  });
</script>

<Navbar />
{#if loading || loading2}
  <div
    class="flex items-center justify-center h-screen w-screen fixed top-0 left-0 place-items-center backdrop-blur-lg bg-black/20 z-20"
  >
    <span class="loading loading-infinity loading-lg"></span>
  </div>
{:else if !user_found}
  <div class="hero min-h-screen bg-base-200">
    <div class="hero-content text-center">
      <div class="max-w-md">
        <h1 class="text-5xl font-bold">Welcome to UMD Course Checker</h1>
        <p class="py-6">
          This is a simple web app that allows you to track the availability of
          classes at the University of Maryland, College Park. This is useful
          for classes that are full and you want to know when a spot opens up.
        </p>
        <a href="/user" class="btn btn-primary">Get Started</a>
      </div>
    </div>
  </div>
{:else}
  <div
    class="overflow-x-auto z-0 sm:mx-20 my-4 rounded-md border border-1 border-gray-800 shadow-xl"
  >
    <table class="table">
      <!-- head -->
      <thead>
        <tr class="text-center">
          <th>#</th>
          <th>Professor</th>
          <th>Class</th>
          <th>Seat Count</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {#each class_array as classData, index (index)}
          {#if classData.sent == true}
            <tr
              class="hover:bg-emerald-700 bg-emerald-600 text-black cursor-pointer text-center"
            >
              <th>{index + 1}</th>
              <td>{classData.instructors ? classData.instructors[0] : "TBA"}</td
              >
              <td>{`${classData.class_name}-${classData.section}`}</td>
              <td>{classData.open_seats}</td>
              <td
                ><button
                  on:click={() => {
                    removeClass(uniqueKey, index, classData, class_array).then(
                      () => {
                        fetchData();
                      },
                    );
                  }}
                >
                  Remove
                </button>
              </td>
            </tr>{:else}
            <tr class="hover cursor-pointer text-center">
              <th>{index + 1}</th>
              <td>{classData.instructors ? classData.instructors[0] : "TBA"}</td
              >
              <td>{`${classData.class_name}-${classData.section}`}</td>
              <td>{classData.open_seats}</td>
              <td
                ><button
                  on:click={() => {
                    removeClass(uniqueKey, index, classData, class_array).then(
                      () => {
                        fetchData();
                      },
                    );
                  }}
                >
                  Remove
                </button>
              </td>
            </tr>
          {/if}
        {/each}
      </tbody>
    </table>
  </div>

  <div
    role="alert"
    class={`alert alert-success fixed bottom-0 left-0 w-fit ml-20 mb-10 transition duration-500 ${
      showAlert ? "opacity-100" : "opacity-0"
    }`}
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
        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
      /></svg
    >
    <span
      >You will receive an email once one of your classes have available seats!</span
    >
  </div>
{/if}

<div class="absolute bottom-5 right-5">
  <a class="link link-primary" href="/changelogs">View Change Logs Here!</a>
</div>
