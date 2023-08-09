<script lang="ts">
  export let api_path = "";
</script>

<button
  class="h-10 rounded-full bg-red-300 mt-2 flex flex-row items-center justify-center"
  on:click={() => {
    window.location.href = api_path;
  }}
>
  <svg
    class="fill-current w-4 h-4 mr-2"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 20 20"
    ><path
      d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"
    /></svg
  >Download
</button>
