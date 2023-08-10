<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
  import { loadSTL, createViewer } from "$lib/STLViewer";
  import DownloadButton from "$lib/DownloadButton.svelte";
  import UpdateButton from "$lib/UpdateButton.svelte";
  import ModeSelect from "$lib/ModeSelect.svelte";

  const material = new THREE.MeshPhongMaterial({
    color: 0x9e8db9,
    specular: 100,
    shininess: 100,
  });

  let loader = new STLLoader();
  let scene = new THREE.Scene();

  let result_type = "bead";
  let length = 15;
  let segments = 4;
  let flatten_top = false;
  let flatten_bottom = false;

  function calculateFlattenValue() {
    // pass in 0 for normal bead, 1 to flatten bottom, 2 to flatten top, 3 to flatten both
    let output = 0;
    if (flatten_bottom) output++;
    if (flatten_top) output += 2;

    return output;
  }

  const result_types = { bead: "Bead", line: "Line" };

  let api_path: string;
  function updateAPIPath() {
    if (result_type == "bead") {
      api_path = `http://localhost:8000/api/bead?length=${length}&flatten=${calculateFlattenValue()}`;
    } else if (result_type == "line") {
      api_path = `http://localhost:8000/api/bead_line?segments=${segments}&length=${length}&flatten=${calculateFlattenValue()}`;
    }

    loadSTL(loader, scene, material, api_path);
  }

  onMount(() => {
    updateAPIPath();
    createViewer(scene, "bead-stl");
  });
</script>

<div class="flex flex-row flex-1 w-1/2 p-2">
  <div class="flex flex-col w-1/4">
    <ModeSelect
      label="Output Type:"
      bind:binding={result_type}
      values={result_types}
    />

    <div class="block">
      <label for="top-toggle" class="pr-1"> Flatten Top? </label>
      <input name="top-toggle" type="checkbox" bind:checked={flatten_top} />
    </div>

    <div class="block">
      <label for="bottom-toggle" class="pr-1"> Flatten Bottom? </label>
      <input
        name="bottom-toggle"
        type="checkbox"
        bind:checked={flatten_bottom}
      />
    </div>

    <label for="length-input"> Length </label>
    <input
      name="length-input"
      class="h-10 bg-blue-400"
      type="number"
      bind:value={length}
    />

    {#if result_type == "line"}
      <label for="segments-input"> Segments </label>
      <input
        name="length-input"
        class="h-10 bg-blue-300"
        type="number"
        bind:value={segments}
      />
    {/if}

    <UpdateButton on:requestUpdate={updateAPIPath} />
    <DownloadButton {api_path} />
  </div>
  <div class="flex-1 ml-2" id="bead-stl" />
</div>

<style></style>
