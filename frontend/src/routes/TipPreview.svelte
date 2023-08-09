<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";
  import UpdateButton from "$lib/UpdateButton.svelte";

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

<div class="flex flex-row flex-1 p-2">
  <div class="flex flex-col w-1/4">
    <div class="flex flex-row">
      <label for="tip-type" class="pr-3"> Tip Type: </label>
      <select
        name="tip-type"
        class="outline outline-slate-600 rounded-lg"
        bind:value={tip_type}
      >
        <option value="cone">Cone</option>
        <option value="sphere">Sphere</option>
      </select>
    </div>

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

    {#if tip_type == "cone"}
      <label for="tip-angle-input"> Tip Angle </label>
      <input
        name="tip-angle-input"
        class="h-10 bg-green-400"
        type="number"
        bind:value={tip_angle}
      />
    {/if}

    <UpdateButton {loader} {scene} {material} {api_path} />
  </div>
  <div class="relative flex-1 ml-2 max-h-full" id="tip-stl" />
</div>

<style></style>
