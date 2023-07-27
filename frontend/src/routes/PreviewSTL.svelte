<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";

  let loader = new STLLoader();
  let scene = new THREE.Scene();
  let mesh = new THREE.Mesh();

  let radius = 1;
  let hole_radius = 0.5;
  let tip_angle = 90;

  function createViewer() {
    let elem = document.getElementById("model");
    if (elem == null) {
      return;
    }

    let renderer = new THREE.WebGLRenderer({ antialias: true });
    let camera = new THREE.PerspectiveCamera(
      75,
      elem.clientWidth / elem.clientHeight,
      0.1,
      1000
    );

    renderer.setSize(elem.clientWidth, elem.clientHeight);
    elem.appendChild(renderer.domElement);
    const light = new THREE.SpotLight();
    light.position.set(20, 20, 20);
    scene.add(light);
    scene.add(new THREE.AxesHelper(5));

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    camera.position.y = 5;
    function animate() {
      requestAnimationFrame(animate);

      controls.update();

      render();
    }

    function render() {
      renderer.render(scene, camera);
    }

    animate();
  }

  onMount(() => {
    loadSTL();
    createViewer();
  });

  function loadSTL() {
    loader.load(
      `http://localhost:8000/api/cone?radius=${radius}&hole_radius=${hole_radius}&tip_angle=${tip_angle}`,
      function (geometry) {
        var material = new THREE.MeshPhongMaterial({
          color: 0xff5533,
          specular: 100,
          shininess: 100,
        });
        scene.remove(mesh);
        mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
      },
      (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
      },
      (error) => {
        console.log(error);
      }
    );
  }
</script>

<div id="model" style="width: 500px; height: 500px" />
<input class="h-10 bg-green-200" type="number" bind:value={radius} />
<input class="h-10 bg-green-300" type="number" bind:value={hole_radius} />
<input class="h-10 bg-green-400" type="number" bind:value={tip_angle} />

<button
  class="w-40 h-10 rounded-full bg-green-800"
  on:click={() => {
    loader = new STLLoader();
    loadSTL();
  }}
>
  generate stl
</button>
