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
  $: class_array; // Ensure reactivity
  let uniqueKey = setLocalStorage();

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

  onMount(fetchData);

  console.log(class_array);
  user_found = checkUserExists(uniqueKey);
</script>

<Navbar />
{#if !user_found}
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
  <div class="overflow-x-auto z-0">
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
            <td>{classData.instructors ? classData.instructors[0] : "TBA"}</td>
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
        {/each}
      </tbody>
    </table>
  </div>
{/if}
