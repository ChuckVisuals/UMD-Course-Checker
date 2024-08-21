<script>
    import {
        setLocalStorage,
        add_class,
        checkOpenClasses,
        fetchData,
    } from "$lib/utils.js";
    import { onMount } from "svelte";
    import { classData } from "$lib/store.js";
    import Layout from "../routes/changelogs/+layout.svelte";

    //form inputs and variables
    let form_model = false;
    let classCounter = 0;
    let class_name = "";
    let section = "";
    let isError = false;
    let class_array = [];
    let uniqueKey = setLocalStorage();
    $: openClasses = 0;
    $: currentUrl = "";
    $: pathname = "";
    onMount(async () => {
        openClasses = await checkOpenClasses(uniqueKey);
        class_array = await fetchData();
        currentUrl = window.location.href;
        const url = new URL(currentUrl);
        pathname = url.pathname;
        console.log(pathname);
    });
    console.log(checkOpenClasses(uniqueKey));
</script>

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
                <li><a href="/user">Your Profile</a></li>
                <li><a href="/about">About</a></li>
            </ul>
        </div>
    </div>

    <div class="navbar-center hidden md:block">
        <a href="./" class="btn btn-ghost text-xl">UMD Course Checker</a>
    </div>
    {#if pathname == "/"}
        <button
            class="btn btn-neutral md:hidden"
            on:click={() => (form_model = !form_model)}
            >Add another class
        </button>

        <div class="navbar-end">
            <button
                class="btn btn-neutral hidden md:block"
                on:click={() => (form_model = !form_model)}
                >Add another class
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
                    {#if openClasses > 0}
                        <span
                            class="badge badge-xs badge-primary indicator-item"
                        ></span>
                    {/if}
                </div>
            </button>
        </div>
    {/if}
</div>

{#if form_model}
    <div class="popup-container z-10">
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
                    on:click={add_class(uniqueKey, class_name, section).then(
                        (data) => {
                            classData.set(data);
                            if (data.length == class_array.length) {
                                isError = true;
                                setTimeout(() => {
                                    isError = false;
                                    console.log(
                                        "isError set to false after 3 seconds",
                                    );
                                }, 3000);
                            } else {
                                form_model = false;
                                class_name = "";
                                section = "";
                            }
                        },
                    )}
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
                    <span>Error! Class Doesn't Exist or Duplicate</span>
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
