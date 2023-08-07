<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";

  const material = new THREE.MeshPhongMaterial({
    color: 0xff5533,
    specular: 100,
    shininess: 100,
  });

  let loader = new STLLoader();
  let scene = new THREE.Scene();

  let tip_type = "cone";
  let radius = 2;
  let hole_radius = 0.5;
  let tip_angle = 90;

  let api_path: string;
  $: {
    if (tip_type == "cone") {
      api_path = `http://localhost:8000/api/cone_tip?radius=${radius}&hole_radius=${hole_radius}&tip_angle=${tip_angle}`;
    } else if (tip_type == "sphere") {
      api_path = `http://localhost:8000/api/sphere_tip?radius=${radius}&hole_radius=${hole_radius}`;
    }
    console.log(api_path);
  }

  onMount(() => {
    loadSTL(loader, scene, material, api_path);
    createViewer(scene, "tip-stl");
  });
</script>

<div class="flex flex-row flex-1">
  <div class="flex flex-col">
    <label for="tip-type"> Tip Type </label>
    <select name="tip-type" bind:value={tip_type}>
      <option value="cone">Cone</option>
      <option value="sphere">Sphere</option>
    </select>

    <label for="radius-input"> Radius </label>
    <input
      name="radius-input"
      class="h-10 bg-green-200"
      type="number"
      bind:value={radius}
    />

    <label for="hole-radius-input"> Hole Radius </label>
    <input
      name="hole-radius-input"
      class="h-10 bg-green-300"
      type="number"
      bind:value={hole_radius}
    />

    {#if !tip_type || tip_type == "Cone"}
      <label for="tip-angle-input"> Tip Angle </label>
      <input
        name="tip-angle-input"
        class="h-10 bg-green-400"
        type="number"
        bind:value={tip_angle}
      />
    {/if}

    <button
      class="h-10 rounded-full bg-green-500"
      on:click={() => {
        loadSTL(loader, scene, material, api_path);
      }}
    >
      Update Tip
    </button>
  </div>
  <div class="relative flex-1 p-2 bg-slate-200" id="tip-stl" />
</div>

<style></style>
