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

  let length = 5;

  let api_path: string;
  $: api_path = `http://localhost:8000/api/bead?length=${length}`;

  onMount(() => {
    loadSTL(loader, scene, material, api_path);
    createViewer(scene);
  });
</script>

<div class="flex flex-row w-screen">
  <div class="flex flex-col">
    <label for="length-input"> Length </label>
    <input
      name="length-input"
      class="h-10 bg-blue-400"
      type="number"
      bind:value={length}
    />

    <button
      class="h-10 rounded-full bg-green-500"
      on:click={() => {
        loadSTL(loader, scene, material, api_path);
      }}
    >
      Generate STL
    </button>
  </div>
  <div class="relative w-fill flex-1 min-w-0 bg-slate-500" id="model" />
</div>

<style></style>
