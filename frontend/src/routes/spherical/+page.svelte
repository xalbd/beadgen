<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";
  import DownloadButton from "$lib/DownloadButton.svelte";
  import UpdateButton from "$lib/UpdateButton.svelte";
  import AngleEditor from "$lib/AngleEditor.svelte";
  import ModeSelect from "$lib/ModeSelect.svelte";

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
  let angles = [0, 45];
  let copies = 1;

  const bead_types = {
    simple: "Simple",
    normal: "Normal",
    multi: "Multi-Angle",
  };

  let api_path: string;
  function updateAPIPath() {
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

    loadSTL(loader, scene, material, api_path);
  }

  onMount(() => {
    updateAPIPath();
    createViewer(scene, "sphere-stl");
  });
</script>

<svelte:head>
  <title>Bead Generation (Spheres)</title>
  <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
</svelte:head>

<div class="flex flex-row flex-1 p-2">
  <div class="flex flex-col w-1/5">
    <ModeSelect
      label="Sphere Type:"
      bind:binding={bead_type}
      values={bead_types}
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

    {#if bead_type == "normal"}
      <label for="effective-angle-input"> Effective Angle </label>
      <input
        name="effective-angle-input"
        class="h-10 bg-purple-100"
        type="number"
        bind:value={effective_angle}
      />
    {/if}

    {#if bead_type == "multi"}
      <AngleEditor {current_angle_input} bind:angles />
    {/if}

    <label for="copies-input"> Copies </label>
    <input
      name="copies-input"
      class="h-10 bg-purple-200"
      type="number"
      bind:value={copies}
    />

    <UpdateButton on:requestUpdate={updateAPIPath} />
    <DownloadButton {api_path} />
  </div>
  <div class="flex-1 ml-2" id="sphere-stl" />
</div>

<style>
</style>
