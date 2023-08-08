<script lang="ts">
    import { onMount } from "svelte";
    import * as THREE from "three";
    import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";
    import { loadSTL, createViewer } from "$lib/STLViewer";
  
    const material = new THREE.MeshPhongMaterial({
      color: 0xa345bf,
      specular: 100,
      shininess: 100,
    });
  
    let loader = new STLLoader();
    let scene = new THREE.Scene();
  
    let struct_type = "polygon";
    let corner_type = "large-sphere";
    let side_length = 50;
    let beads_per_side = 5;
    let hole_radius = 1;
    let num_sides = 5;
  
    let api_path: string;
    $: {
      if (struct_type == "square") {
        api_path = `http://localhost:8000/api/square-struct?side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}`;
      } else if (struct_type == "triangle") {
        api_path = `http://localhost:8000/api/triangle-struct?side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}`;
      } else if (struct_type == "polygon") {
        api_path = `http://localhost:8000/api/polygon-struct?num_sides=${side_length}&side_length=${side_length}&beads_per_side=${beads_per_side}&hole_radius=${hole_radius}`;
      } 
    }
  
    onMount(() => {
      loadSTL(loader, scene, material, api_path);
      createViewer(scene, "struct-stl");
    });
  </script>
  
  <svelte:head>
    <title>Structure Generation </title>
    <meta name="description" content="Automatic Wire-Jamming Bead Generation" />
  </svelte:head>
  
  <div class="flex flex-row h-screen">
    <div class="flex flex-col w-1/5">
      <label for="result-type"> Structure Type </label>
      <select name="result-type" bind:value={struct_type}>
        <option value="square">Square</option>
        <option value="triangle">Triangle</option>
        <option value="polygon">Polygon</option>
      </select>

      <label for="corner-type"> Corner Type </label>
      <select name="corner-type" bind:value={corner_type}>
        <option value="large-sphere">Large Sphere</option>
      </select>
  
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
    <div class="relative flex-1 p-2 bg-slate-200" id="struct-stl" />
  </div>
  
  <style>
  </style>
  