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
  let mesh = new THREE.Mesh();

  let tip_type: string = "Cone";
  let radius = 2;
  let hole_radius = 0.5;
  let tip_angle = 90;

  let api_path = `http://localhost:8000/api/tip?type=${
    tip_type == "Cone" ? "0" : "1"
  }&radius=${radius}&hole_radius=${hole_radius}&tip_angle=${tip_angle}`;

  onMount(() => {
    loadSTL(loader, mesh, scene, material, api_path);
    createViewer(scene);
    console.log("done");
  });
</script>

<div class="flex flex-row w-screen">
  <div class="flex flex-col">
    <label for="tip-type"> Tip Type </label>
    <select
      name="tip-type"
      bind:value={tip_type}
      on:change={() => {
        console.log(tip_type);
      }}
    >
      <option> Cone </option>
      <option> Sphere </option>
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

    <label for="tip-angle-input"> Tip Angle </label>
    <input
      name="tip-angle-input"
      class="h-10 bg-green-400"
      type="number"
      bind:value={tip_angle}
    />
  </div>
  <div class="relative w-fill flex-1 min-w-0 bg-slate-500" id="model" />
</div>

<style></style>
