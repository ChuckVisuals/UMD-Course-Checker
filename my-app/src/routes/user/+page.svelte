<script>
  import { v4 as uuidv4 } from "uuid";
  import { createClient } from "@supabase/supabase-js";
  import { onMount } from "svelte";

  const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
  const supabaseKey = import.meta.env.VITE_SUPABASE_KEY;
  const supabase = createClient(supabaseUrl, supabaseKey);

  let user_found = false;
  let form_model;
  let email;
  let name;
  $: name;

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
        } else {
          name = "";
          email = "";
        }
      }
    }
  });

  async function add_user() {
    if (!user_found) {
      try {
        // Add the class_name and section to the Supabase table
        const { data, error } = await supabase.from("user_data").insert([
          {
            uniqueKey: uniqueKey,
            email: email,
            name: name,
          },
        ]);
        form_model = false;
        user_found = true;
        if (error) {
          console.error("Error adding data to Supabase:", error.message);
        } else {
          console.log("Data added to Supabase successfully:", data);
        }
      } catch (error) {
        console.error("Error:", error.message);
      }
    } else {
      //updates the user from db based on device
      try {
        if (uniqueKey) {
          // Fetch all rows with the given uniqueKey
          const { data, error } = await supabase
            .from("user_data")
            .update({ name: name, email: email })
            .eq("uniqueKey", uniqueKey);
          console.log(data);
          form_model = false;
        }
      } catch (error) {
        console.error("Error fetching API links:", error.message);
      }
    }
  }
</script>

<body>
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
          <li><a href="/about">About</a></li>
        </ul>
      </div>
    </div>

    <div class="navbar-center">
      <a href="/" class="btn btn-ghost text-xl">UMD Course Checker</a>
    </div>

    <div class="navbar-end">
      <button class="btn m-4" on:click={() => (form_model = !form_model)}
        >Enter User Data
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

  <div class="p-14 text-2xl">
    Welcome back {name}
  </div>
  {#if user_found}
    <div class="px-14 py-14 text-2xl">
      Current Email: {email}
    </div>
  {/if}

  {#if !user_found}
    <div class="py-52 px-20 flex justify-center text-xl">
      <p>
        Enter in your email/terpmail and or phone number to get alerts on when
        your class will be open above using the enter user data button
      </p>
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
