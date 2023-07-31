<script lang="ts">
  let width = 100;
  let height = 200;
  let source = `http://localhost:8000/api/square?width=${width}&height=${height}`;
</script>

<section class="flex flex-row flex-wrap w-screen bg-slate-100">
  <img class="w-1/4" src={source} alt="SVG Preview" />

  <button
    class="w-40 h-10 rounded-full bg-slate-600"
    on:click={() => {
      source = `http://localhost:8000/api/square?width=${width}&height=${height}`;
    }}
  >
    make square
  </button>

  <input class="h-10 bg-slate-200" type="number" bind:value={width} />
  <input class="h-10 bg-slate-300" type="number" bind:value={height} />
</section>

<style>
</style>
