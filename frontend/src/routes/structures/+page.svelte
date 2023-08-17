<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";
  import DownloadButton from "$lib/DownloadButton.svelte";
  import UpdateButton from "$lib/UpdateButton.svelte";
  import ModeSelect from "$lib/ModeSelect.svelte";

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
  let shape1_sides = 4;
  let shape2_sides = 5;
  let total_length = 200;
  let total_beads = 20;

  const struct_types = {
    square: "Square",
    triangle: "Triangle",
    polygon: "Polygon",
    shapeShifting: "Shape Shifting"
  };
  const corner_types = { 0: "Large Sphere", 1: "Curved Cylinder" };

  let api_path: string;
  function updateAPIPath() {
    if (struct_type == "square") {
      api_path = `http://localhost:8000/api/square-struct?side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}&corner_type=${corner_type}`;
    } else if (struct_type == "triangle") {
      api_path = `http://localhost:8000/api/triangle-struct?side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}&corner_type=${corner_type}`;
    } else if (struct_type == "polygon") {
      api_path = `http://localhost:8000/api/polygon-struct?num_sides=${num_sides}&side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}&corner_type=${corner_type}`;
    } else if (struct_type == "shapeShifting") {
      api_path = `http://localhost:8000/api/shape-shifting-struct?shape1_sides=${shape1_sides}&shape2_sides=${shape2_sides}&total_length=${total_length}&total_beads=${total_beads}&hole_radius=${hole_radius}`;
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

<div class="flex flex-row flex-1 p-2">
  <div class="flex flex-col w-1/5">
    <ModeSelect
      label="Structure Type:"
      bind:binding={struct_type}
      values={struct_types}
    />
    {#if struct_type != "shapeShifting"}
    <ModeSelect
      label="Corner Type:"
      bind:binding={corner_type}
      values={corner_types}
    />
    {/if}

    {#if !struct_type || struct_type == "polygon"}
      <label for="num-sides-input"> Number of Sides </label>
      <input
        name="num-sides-input"
        class="h-10 bg-purple-400"
        type="number"
        bind:value={num_sides}
      />
    {/if}

    {#if !struct_type || struct_type == "shapeShifting"}
      <label for="shape1-sides-input"> Shape 1 # of Sides </label>
      <input
        name="shape1-sides-input"
        class="h-10 bg-purple-400"
        type="number"
        bind:value={shape1_sides}
      />

      <label for="shape2-sides-input"> Shape 2 # of Sides </label>
      <input
        name="shape2-sides-input"
        class="h-10 bg-purple-400"
        type="number"
        bind:value={shape2_sides}
      />

      <label for="total-length-input"> Total Length </label>
      <input
        name="total-length-input"
        class="h-10 bg-purple-400"
        type="number"
        bind:value={total_length}
      />

      <label for="total-beads-input"> Total # of Beads </label>
      <input
        name="total-beads-input"
        class="h-10 bg-purple-200"
        type="number"
        bind:value={total_beads}
      />
    {/if}

    {#if struct_type != "shapeShifting"}
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
    {/if}

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
  <div class="flex-1 ml-2" id="struct-stl" />
</div>

<style>
</style>
