<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";

  const material = new THREE.MeshPhongMaterial({
    color: 0xa345bf,
    specular: 100,
    shininess: 100,
  });

  let loader = new STLLoader();
  let scene = new THREE.Scene();

  let radius = 5;
  let hole_radius = 1;
  let cut_amount = 2;

  let api_path: string;
  $: api_path = `http://localhost:8000/api/sphere?radius=${radius}&hole_radius=${hole_radius}&cut_amount=${cut_amount}`;

  onMount(() => {
    loadSTL(loader, scene, material, api_path);
    createViewer(scene, "sphere-stl");
  });
</script>

<svelte:head>
  <title>Bead Generation (Spheres)</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<div class="flex flex-row h-screen">
  <div class="flex flex-col">
    <label for="radius-input"> Radius </label>
    <input
      name="radius-input"
      class="h-10 bg-purple-400"
      type="number"
      bind:value={radius}
    />

    <label for="hole-radius-input"> Hole Radius </label>
    <input
      name="hole-radius-input"
      class="h-10 bg-purple-300"
      type="number"
      bind:value={hole_radius}
    />

    <label for="cut-amount-input"> Cut Amount </label>
    <input
      name="cut-amount-input"
      class="h-10 bg-purple-200"
      type="number"
      bind:value={cut_amount}
    />

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
  <div class="relative flex-1 p-2 bg-slate-200" id="sphere-stl" />
</div>

<style>
</style>
