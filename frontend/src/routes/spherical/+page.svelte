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

  let bead_type = "multi";
  let radius = 5;
  let hole_radius = 0.5;
  let effective_angle = 30;
  let current_angle_input = 20;
  let angles = [45, 0];
  let copies = 1;

  let api_path: string;
  $: {
    if (bead_type == "simple") {
      api_path = `http://localhost:8000/api/simple_sphere?radius=${radius}&hole_radius=${hole_radius}&copies=${copies}`;
    } else if (bead_type == "normal") {
      api_path = `http://localhost:8000/api/sphere?radius=${radius}&hole_radius=${hole_radius}&effective_angle=${effective_angle}&copies=${copies}`;
    } else if (bead_type == "multi") {
      api_path = `http://localhost:8000/api/angled-sphere?radius=${radius}&hole_radius=${hole_radius}`;
      angles.forEach((angle) => {
        api_path += `&angles=${angle}`;
      });
    }
  }

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
  <div class="flex flex-col w-1/5">
    <label for="result-type"> Bead Type </label>
    <select name="result-type" bind:value={bead_type}>
      <option value="simple">Simple</option>
      <option value="normal">Normal</option>
      <option value="multi">Multi Angle</option>
    </select>

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

    {#if !bead_type || bead_type == "normal"}
      <label for="effective-angle-input"> Effective Angle </label>
      <input
        name="effective-angle-input"
        class="h-10 bg-purple-100"
        type="number"
        bind:value={effective_angle}
      />
    {/if}

    {#if !bead_type || bead_type == "multi"}
      <label for="angle-input"> Angle Editor </label>
      <div class="flex flex-row">
        <input
          name="angle-input"
          class="flex-1 h-10 min-w-0 bg-purple-100"
          type="number"
          bind:value={current_angle_input}
        />
        <button
          class="h-10 rounded-full w-1/4 bg-rose-300"
          on:click={() => {
            if (!angles.includes(current_angle_input)) {
              angles.push(current_angle_input);
              angles = angles;
            }
          }}
        >
          Add
        </button>
        <button
          class="h-10 rounded-full w-1/4 bg-rose-500"
          on:click={() => {
            angles = [0];
          }}
        >
          Reset
        </button>
      </div>
      <p>
        Current Angles: {angles}
      </p>
    {/if}

    <label for="copies-input"> Copies </label>
    <input
      name="copies-input"
      class="h-10 bg-purple-200"
      type="number"
      bind:value={copies}
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
