<script>
  import { onMount, onDestroy, afterUpdate } from "svelte";

  let days = 0;
  let hours = 0;
  let minutes = 0;
  let seconds = 0;

  // Set the target date (January 10, 2024)
  const targetDate = new Date("2024-01-10T00:00:00").getTime();

  function updateCountdown() {
    const now = new Date().getTime();
    const timeDifference = targetDate - now;

    if (timeDifference > 0) {
      days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
      hours = Math.floor(
        (timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60),
      );
      minutes = Math.floor((timeDifference % (1000 * 60 * 60)) / (1000 * 60));
      seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
    } else {
      // Countdown reached or passed the target date
      days = hours = minutes = seconds = 0;
      clearInterval(interval);
    }
  }

  // Update the countdown every second
  let interval;
  onMount(() => {
    interval = setInterval(updateCountdown, 1000);
  });

  afterUpdate(() => {
    updateCountdown(); // Ensure countdown is updated after each render
  });

  onDestroy(() => {
    clearInterval(interval); // Cleanup when the component is destroyed
  });
</script>

<div class="flex gap-5">
  <div>
    <span class="countdown font-mono text-4xl">
      <span style={days}></span>
    </span>
    days
  </div>
  <div>
    <span class="countdown font-mono text-4xl">
      <span style="--value:10;"></span>
    </span>
    hours
  </div>
  <div>
    <span class="countdown font-mono text-4xl">
      <span style="--value:24;"></span>
    </span>
    min
  </div>
  <div>
    <span class="countdown font-mono text-4xl">
      <span style="--value:38;"></span>
    </span>
    sec
  </div>
</div>
