<script lang="ts">
  import axios from "axios";

  let svg_path = "";
  let width = 0;
  let height = 0;
  let source = "http://localhost:8000/api/square";
</script>

<section class="flex flex-row w-screen">
  <img class="w-1/4 flex-initial" src={source} alt="bruh" />

  <button
    class="w-40 h-10 rounded-full bg-slate-800"
    on:click={() => {
      source =
        "http://localhost:8000/api/square?width=" + width + "&height=" + height;
    }}
  />

  <input class="h-10 bg-slate-200" type="number" bind:value={width} />
  <input class="h-10 bg-slate-300" type="number" bind:value={height} />
</section>

<style>
</style>
