<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";
  import DownloadButton from "$lib/DownloadButton.svelte";
  import UpdateButton from "$lib/UpdateButton.svelte";
  import AngleEditor from "$lib/AngleEditor.svelte";
  import ModeSelect from "$lib/ModeSelect.svelte";

  const material = new THREE.MeshStandardMaterial({
    color: 0x66ff66,
    roughness: 0.7,
    metalness: 0.2,
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

  const generation_types = { single: "Single", matching: "Matching" };
  const bead_types = { cone: "Cone", sphere: "Sphere" };

  let api_path: string;
  function updateAPIPath() {
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

    loadSTL(loader, scene, material, api_path);
  }

  onMount(() => {
    updateAPIPath();
    createViewer(scene, "bead-stl");
  });
</script>

<svelte:head>
  <title>Bead Generation (Double-Sided)</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<div class="flex flex-row flex-1 p-2">
  <div class="flex flex-col w-1/5">
    <ModeSelect
      label="Generation Type:"
      bind:binding={bead_type}
      values={generation_types}
    />

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

    <div
      class="mt-3 p-2 border border-gray-600 rounded-lg flex-col flex bg-red-200"
    >
      <ModeSelect
        label="Top Interface:"
        bind:binding={top_type}
        values={bead_types}
      />

      {#if top_type == "cone"}
        <label for="top-tip-angle-input"> Tip Angle </label>
        <input
          name="top-tip-angle-input"
          class="h-10 bg-purple-300"
          type="number"
          bind:value={top_cone_tip_angle}
        />
      {/if}

      {#if top_type == "sphere"}
        <AngleEditor
          current_angle_input={top_current_angle_input}
          bind:angles={top_sphere_angles}
        />
      {/if}
    </div>

    <div
      class="my-3 p-2 border border-gray-600 rounded-lg flex-col flex bg-orange-100"
    >
      <ModeSelect
        label="Bottom Interface:"
        bind:binding={bottom_type}
        values={bead_types}
      />

      {#if bottom_type == "cone"}
        <label for="bottom-tip-angle-input"> Tip Angle </label>
        <input
          name="top-tip-angle-input"
          class="h-10 bg-purple-300"
          type="number"
          bind:value={bottom_cone_tip_angle}
        />
      {/if}
    </div>

    <UpdateButton on:requestUpdate={updateAPIPath} />
    <DownloadButton {api_path} />
  </div>
  <div class="flex-1 ml-2" id="bead-stl" />
</div>

<style>
</style>
