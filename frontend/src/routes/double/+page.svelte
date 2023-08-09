<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";
  import DownloadButton from "$lib/DownloadButton.svelte";
  import UpdateButton from "$lib/UpdateButton.svelte";

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
  let length = 5;
  let top_cone_tip_angle = 90;
  let bottom_cone_tip_angle = 90;
  let top_sphere_angles = [0];
  let top_current_angle_input = 45;

  let api_path: string;
  $: {
    api_path = `http://localhost:8000/api/double_sided?radius=${radius}&hole_radius=${hole_radius}&length=${length}`;
    if (top_type == "cone") {
      api_path += `&top_tip_angle=${top_cone_tip_angle}`;
    } else {
      top_sphere_angles.forEach((angle) => {
        api_path += `&top_sphere_angles=${angle}`;
      });
    }
    if (bottom_type == "cone") {
      api_path += `&bottom_tip_angle=${bottom_cone_tip_angle}`;
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

<div class="flex flex-row h-screen p-2">
  <div class="flex flex-col w-1/5">
    <div class="flex flex-row">
      <label for="result-type" class="pr-3"> Generation Type: </label>
      <select
        name="result-type"
        class="outline outline-slate-600 rounded-lg"
        bind:value={bead_type}
      >
        <option value="single">Single</option>
        <option value="matching">Matching Pair</option>
      </select>
    </div>

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

    <label for="length-input"> Length </label>
    <input
      name="length-input"
      class="h-10 bg-purple-200"
      type="number"
      bind:value={length}
    />

    <div class="mt-3 outline-1 outline flex-col flex bg-red-200">
      <label for="top-type"> Top Interface </label>
      <select name="top-type" bind:value={top_type}>
        <option value="cone">Cone</option>
        <option value="sphere">Sphere</option>
      </select>

      {#if top_type == "cone"}
        <label for="top-tip-angle-input"> Tip Angle </label>
        <input
          name="top-tip-angle-input"
          class="h-10 bg-purple-100"
          type="number"
          bind:value={top_cone_tip_angle}
        />
      {/if}

      {#if top_type == "sphere"}
        <label for="angle-input"> Angle Editor </label>
        <div class="flex flex-row">
          <input
            name="angle-input"
            class="flex-1 h-10 min-w-0 bg-purple-100"
            type="number"
            bind:value={top_current_angle_input}
          />
          <button
            class="h-10 rounded-full w-1/4 bg-rose-300"
            on:click={() => {
              if (!top_sphere_angles.includes(top_current_angle_input)) {
                top_sphere_angles.push(top_current_angle_input);
                top_sphere_angles = top_sphere_angles;
              }
            }}
          >
            Add
          </button>
          <button
            class="h-10 rounded-full w-1/4 bg-rose-500"
            on:click={() => {
              top_sphere_angles = [0];
            }}
          >
            Reset
          </button>
        </div>
        <p>
          Current Angles: {top_sphere_angles}
        </p>
      {/if}
    </div>

    <div class="my-3 outline-1 outline flex-col flex bg-orange-100">
      <label for="bottom-type"> Bottom Interface </label>
      <select name="bottom-type" bind:value={bottom_type}>
        <option value="cone">Cone</option>
        <option value="sphere">Sphere</option>
      </select>

      {#if bottom_type == "cone"}
        <label for="bottom-tip-angle-input"> Tip Angle </label>
        <input
          name="top-tip-angle-input"
          class="h-10 bg-purple-100"
          type="number"
          bind:value={bottom_cone_tip_angle}
        />
      {/if}
    </div>

    <UpdateButton {loader} {scene} {material} {api_path} />
    <DownloadButton {api_path} />
  </div>
  <div class="relative flex-1 ml-2" id="bead-stl" />
</div>

<style>
</style>
