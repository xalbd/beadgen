<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();
  function requestAPIUpdate() {
    dispatch("requestUpdate");
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.code == "Enter") {
      dispatch("requestUpdate");
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

<button
  class="h-10 rounded-full bg-green-400 hover:bg-green-500 active:bg-green-600 mt-2 flex flex-row items-center justify-center"
  on:click={() => {
    requestAPIUpdate();
  }}
>
  <svg
    class="fill-current w-4 h-4 mr-2"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    ><path
      d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
    /></svg
  >Refresh Preview
</button>
