<body class="overflow-hidden">
  <div class="navbar bg-base-200 z-100">
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
          <li><a href="/user">Your Profile</a></li>
        </ul>
      </div>
    </div>

    <div class="navbar-center">
      <a href="/" class="btn btn-ghost text-xl">UMD Course Checker</a>
    </div>

    <div class="navbar-end">
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

  <div class="my-32 mx-20 flex justify-center text-2xl flex-col">
    <p>
      Hey, I made this project so that victims like myself wont be screwed over
      with the testudo registration. This build is in beta so if you find any
      bugs feel free to submit a issue request over to the <a
        class="link link-primary"
        href="https://github.com/ChuckVisuals/UMD-Course-Checker/issues"
        >github repo</a
      > :]
    </p>
  </div></body
>
