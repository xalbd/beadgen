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
    ><path d="M13 8V2H7v6H2l8 8 8-8h-5zM0 18h20v2H0v-2z" /></svg
  >Download
</button>
