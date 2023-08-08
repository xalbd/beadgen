<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";

  const material = new THREE.MeshPhongMaterial({
    color: 0x66ff66,
    specular: 100,
    shininess: 100,
  });

  let loader = new STLLoader();
  let scene = new THREE.Scene();

  let bead_type = "single";
  let bottom_type = "cone";
  let top_type = "sphere";
  let radius = 5;
  let hole_radius = 0.5;
  let top_cone_tip_angle = 90;
  let bottom_cone_tip_angle = 90;
  let top_sphere_angles = [0];
  let bottom_sphere_angles = [0];
  let current_angle_input = 45;
  let copies = 1;

  let api_path: string;
  $: {
    api_path = `http://localhost:8000/api/double_sided?radius=${radius}&hole_radius=${hole_radius}&top=${top_type}&bottom=${bottom_type}`;
    if (top_type == "cone") {
      api_path += `&top_angle=${top_cone_tip_angle}`;
    }
    if (bottom_type == "cone") {
      api_path += `&bottom_angle=${bottom_cone_tip_angle}`;
    }
  }

  onMount(() => {
    loadSTL(loader, scene, material, api_path);
    createViewer(scene, "bead-stl");
  });
</script>

<svelte:head>
  <title>Bead Generation (Double-Sided)</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<div class="flex flex-row h-screen">
  <div class="flex flex-col w-1/5">
    <label for="result-type"> Generation Type </label>
    <select name="result-type" bind:value={bead_type}>
      <option value="single">Single</option>
      <option value="matching">Matching Pair</option>
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

    <label for="top-type"> Top Interface </label>
    <select name="top-type" bind:value={top_type}>
      <option value="cone">Cone</option>
      <option value="sphere">Sphere</option>
    </select>

    {#if top_type == "cone"}
      <label for="top-tip-angle-input"> Top Cone Tip Angle </label>
      <input
        name="top-tip-angle-input"
        class="h-10 bg-purple-100"
        type="number"
        bind:value={top_cone_tip_angle}
      />
    {/if}

    <label for="bottom-type"> Bottom Interface </label>
    <select name="bottom-type" bind:value={bottom_type}>
      <option value="cone">Cone</option>
      <option value="sphere">Sphere</option>
    </select>

    {#if bottom_type == "cone"}
      <label for="bottom-tip-angle-input"> Bottom Cone Tip Angle </label>
      <input
        name="top-tip-angle-input"
        class="h-10 bg-purple-100"
        type="number"
        bind:value={bottom_cone_tip_angle}
      />
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
  <div class="relative flex-1 p-2 bg-slate-200" id="bead-stl" />
</div>

<style>
</style>
