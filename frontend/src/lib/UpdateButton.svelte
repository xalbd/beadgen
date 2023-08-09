<script lang="ts">
  import { loadSTL } from "./STLViewer";
  import type { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";

  export let loader: STLLoader;
  export let scene: THREE.Scene;
  export let material: THREE.Material;
  export let api_path: string;
</script>

<button
  class="h-10 rounded-full bg-green-400 mt-2 flex flex-row items-center justify-center"
  on:click={() => {
    loadSTL(loader, scene, material, api_path);
  }}
>
  <svg
    class="fill-current w-4 h-4 mr-2"
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 20 20"
    ><path
      d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"
    /></svg
  >Refresh Preview
</button>
