<script>
  import { v4 as uuidv4 } from "uuid";
  import { createClient } from "@supabase/supabase-js";
  import { printData, setLocalStorage } from "$lib/utils.js";
  import { onMount } from "svelte";

  const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
  const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;
  const supabase = createClient(supabaseUrl, supabaseKey);

  let user_found = false;
  let form_model;
  let email;
  let name;
  $: name;
  let loading = true;

  //local storage code
  let uniqueKey = setLocalStorage();
  console.log(uniqueKey);

  //updates the user from db based on device
  onMount(async () => {
    if (uniqueKey) {
      // Fetch all rows with the given uniqueKey
      const { data, error } = await supabase
        .from("user_data")
        .select("name, email")
        .eq("uniqueKey", uniqueKey);
      console.log(data);

      if (error) {
        console.error("Error fetching API links:", error.message);
      } else {
        if (data.length > 0) {
          name = data[0].name || "";
          email = data[0].email || "";
          user_found = true;
          loading = false;
        } else {
          name = "";
          email = "";
          loading = false;
        }
      }
    }
  });

  async function add_user() {
    if (!user_found) {
      console.log("not found");
      try {
        // Add the email and user's name to the Supabase table
        const { data, error } = await supabase.from("user_data").insert([
          {
            uniqueKey: uniqueKey,
            email: email,
            name: name,
          },
        ]);
        form_model = false;
        user_found = true;

        //sends email to user thru the api call for init registration
        try {
          const response = await fetch(
            "https://umd-course-checker-api.vercel.app/sendEmailOnRegistar",
            {
              method: "POST",
              body: JSON.stringify({
                email: email,
                name: name,
              }),
              headers: {
                "Content-type": "application/json; charset=UTF-8",
              },
            },
          );

          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }

          const data = await response.json();
          console.log(data);
        } catch (error) {
          console.error("Error:", error);
        }

        if (error) {
          console.error("Error adding data to Supabase:", error.message);
        } else {
          console.log("Data added to Supabase successfully:", data);
        }
      } catch (error) {
        console.error("Error:", error.message);
      }
    } else {
      console.log("found user");
      //updates the user from db based on device
      try {
        if (uniqueKey) {
          // Fetch all rows with the given uniqueKey
          const { data, error } = await supabase
            .from("user_data")
            .update({ name: name, email: email })
            .eq("uniqueKey", uniqueKey);
          form_model = false;
        }
      } catch (error) {
        console.error("Error fetching API links:", error.message);
      }
    }
  }

  async function handleClick() {
    form_model = !form_model; // Update the state
  }
</script>

{#if loading}
  <div
    class="flex items-center justify-center h-screen w-screen fixed top-0 left-0 place-items-center backdrop-blur-lg bg-black/20 z-20"
  >
    <span class="loading loading-infinity loading-lg z-20"></span>
  </div>
{:else}
  <body>
    <div class="navbar bg-base-200">
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

          <!-- svelte-ignore a11y-no-noninteractive-tabindex -->
          <ul
            tabindex="0"
            class="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52 border-2 border-neutral"
          >
            <li><a href="/">Dashboard</a></li>
            <li><a href="/about">About</a></li>
          </ul>
        </div>
      </div>

      <button
        class="btn btn-neutral md:hidden"
        on:click={() => (form_model = !form_model)}
        >Enter User Data
      </button>

      <div class="navbar-center hidden md:block">
        <a href="./" class="btn btn-ghost text-xl">UMD Course Checker</a>
      </div>

      <div class="navbar-end">
        <button
          class="btn btn-neutral hidden md:block"
          on:click={() => (form_model = !form_model)}
          >Enter User Data
        </button>
        <button class="btn btn-ghost btn-circle ml-4">
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

    {#if !user_found}
      <div class="my-20 mx-20 flex justify-center text-xl">
        <p>
          Enter in your email to get alerts on when your class will be open
          above using the enter user data button. Please note that using your
          terpmail will not work!!!
        </p>
      </div>
    {:else}
      <div class="flex flex-col justify-center items-center my-16">
        <div
          class="card w-fit bg-primary text-primary-content shadow-2xl mx-10"
        >
          <div class="card-body">
            <h2 class="card-title">
              {#if name}
                Welcome back {name}
              {:else}
                Welcome, please sign in.
              {/if}
            </h2>
            {#if user_found}
              <div class="text-2xl">
                Current Email: {email}
              </div>
            {/if}
          </div>
          <div class="card-actions justify-end m-5">
            <a href="/" class="btn">Go Home</a>
          </div>
        </div>
        <div class="my-20 mx-20 flex justify-center text-xl">
          <p>
            If you would like to change your email or phone number, please use
            the enter user data button
          </p>
        </div>
      </div>
    {/if}

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
              placeholder="Your Name"
              bind:value={name}
              class="input input-bordered input-primary w-full max-w-xs px-4 py-2"
            />

            <input
              type="text"
              placeholder="Your Email"
              bind:value={email}
              class="input input-bordered input-primary w-full max-w-xs px-4 py-2"
            />

            <button
              class="btn bg-indigo-500 hover:bg-indigo-700 text-lg"
              on:click={add_user}
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
        </div>
      </div>
    {/if}
  </body>
{/if}
