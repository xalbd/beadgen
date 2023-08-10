<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";
  import DownloadButton from "$lib/DownloadButton.svelte";
  import UpdateButton from "$lib/UpdateButton.svelte";

  const material = new THREE.MeshPhongMaterial({
    color: 0xa345bf,
    specular: 100,
    shininess: 100,
  });

  let loader = new STLLoader();
  let scene = new THREE.Scene();

  let struct_type = "triangle";
  let corner_type = "1";
  let side_length = 30;
  let beads_per_side = 3;
  let hole_radius = 1;
  let num_sides = 3;

  let api_path: string;
  function updateAPIPath() {
    if (struct_type == "square") {
      api_path = `http://localhost:8000/api/square-struct?side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}&corner_type=${corner_type}`;
    } else if (struct_type == "triangle") {
      api_path = `http://localhost:8000/api/triangle-struct?side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}&corner_type=${corner_type}`;
    } else if (struct_type == "polygon") {
      api_path = `http://localhost:8000/api/polygon-struct?num_sides=${num_sides}&side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}&corner_type=${corner_type}`;
    }

    loadSTL(loader, scene, material, api_path);
  }

  onMount(() => {
    updateAPIPath();
    createViewer(scene, "struct-stl");
  });
</script>

<svelte:head>
  <title>Structure Generation</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<div class="flex flex-row h-screen p-2">
  <div class="flex flex-col w-1/5">
    <div class="flex flex-row">
      <label for="result-type" class="pr-3"> Structure Type: </label>
      <select
        name="result-type"
        class="outline outline-slate-600 rounded-lg mb-2"
        bind:value={struct_type}
      >
        <option value="square">Square</option>
        <option value="triangle">Triangle</option>
        <option value="polygon">Polygon</option>
      </select>
    </div>

    <div class="flex flex-row">
      <label for="corner-type" class="pr-3"> Corner Type: </label>
      <select
        name="corner-type"
        class="outline outline-slate-600 rounded-lg"
        bind:value={corner_type}
      >
        <option value="0">Large Sphere</option>
        <option value="1">Curved Cylinder</option>
      </select>
    </div>

    {#if !struct_type || struct_type == "polygon"}
      <label for="num-sides-input"> Number of Sides </label>
      <input
        name="num-sides-input"
        class="h-10 bg-purple-400"
        type="number"
        bind:value={num_sides}
      />
    {/if}

    <label for="side-length-input"> Side Length </label>
    <input
      name="side-length-input"
      class="h-10 bg-purple-400"
      type="number"
      bind:value={side_length}
    />

    <label for="beads-per-side-input"> Beads Per Side </label>
    <input
      name="beads-per-side-input"
      class="h-10 bg-purple-200"
      type="number"
      bind:value={beads_per_side}
    />

    <label for="hole-radius-input"> Hole Radius </label>
    <input
      name="hole-radius-input"
      class="h-10 bg-purple-300"
      type="number"
      bind:value={hole_radius}
    />

    <UpdateButton on:requestUpdate={updateAPIPath} />
    <DownloadButton {api_path} />
  </div>
  <div class="relative flex-1 ml-2" id="struct-stl" />
</div>

<style>
</style>
