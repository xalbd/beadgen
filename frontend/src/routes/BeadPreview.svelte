<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";

  const material = new THREE.MeshPhongMaterial({
    color: 0x9e8db9,
    specular: 100,
    shininess: 100,
  });

  let loader = new STLLoader();
  let scene = new THREE.Scene();

  let result_type = "bead";
  let length = 5;
  let segments = 1;

  let api_path: string;
  $: {
    if (result_type == "bead") {
      api_path = `http://localhost:8000/api/bead?length=${length}`;
    } else if (result_type == "line") {
      api_path = `http://localhost:8000/api/bead_line?segments=${segments}&length=${length}`;
    }
  }

  onMount(() => {
    loadSTL(loader, scene, material, api_path);
    createViewer(scene, "bead-stl");
  });
</script>

<div class="flex flex-row flex-1">
  <div class="flex flex-col">
    <label for="result-type"> Result Type </label>
    <select name="result-type" bind:value={result_type}>
      <option value="bead">Bead</option>
      <option value="line">Line</option>
    </select>

    <label for="length-input"> Length </label>
    <input
      name="length-input"
      class="h-10 bg-blue-400"
      type="number"
      bind:value={length}
    />

    {#if !result_type || result_type == "Line"}
      <label for="segments-input"> Segments </label>
      <input
        name="length-input"
        class="h-10 bg-blue-300"
        type="number"
        bind:value={segments}
      />
    {/if}

    <button
      class="h-10 rounded-full bg-green-500"
      on:click={() => {
        loadSTL(loader, scene, material, api_path);
      }}
    >
      Update Generation
    </button>

    <button
      class="h-10 rounded-full bg-red-300"
      on:click={() => {
        window.location.href = api_path;
      }}
    >
      Download Generation
    </button>
  </div>
  <div class="relative flex-1 p-2 bg-slate-200" id="bead-stl" />
</div>

<style></style>
