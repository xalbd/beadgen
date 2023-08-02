<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";

  const material = new THREE.MeshPhongMaterial({
    color: 0x5e2d39,
    specular: 100,
    shininess: 100,
  });

  let loader = new STLLoader();
  let scene = new THREE.Scene();

  let length = 5;
  let segments = 5;

  let api_path: string;
  $: api_path = `http://localhost:8000/api/bead_line?segments=${segments}&length=${length}`;

  onMount(() => {
    loadSTL(loader, scene, material, api_path);
    createViewer(scene, "bead-path-stl");
  });
</script>

<div class="flex flex-row flex-1">
  <div class="flex flex-col">
    <label for="length-input"> Length </label>
    <input
      name="length-input"
      class="h-10 bg-blue-400"
      type="number"
      bind:value={length}
    />

    <label for="segments-input"> Segments </label>
    <input
      name="length-input"
      class="h-10 bg-blue-300"
      type="number"
      bind:value={segments}
    />

    <button
      class="h-10 rounded-full bg-green-500"
      on:click={() => {
        loadSTL(loader, scene, material, api_path);
      }}
    >
      Update Bead Path
    </button>
  </div>
  <div class="relative flex-1 p-2 bg-slate-200" id="bead-path-stl" />
</div>

<style></style>
