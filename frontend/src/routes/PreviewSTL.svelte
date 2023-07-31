<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";

  let loader = new STLLoader();
  let scene = new THREE.Scene();
  let mesh = new THREE.Mesh();

  const material = new THREE.MeshPhongMaterial({
    color: 0xff5533,
    specular: 100,
    shininess: 100,
  });

  let radius = 1;
  let hole_radius = 0.5;
  let tip_angle = 90;

  function createViewer() {
    let elem = document.getElementById("model");
    if (elem == null) {
      return;
    }

    let renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(elem.clientWidth, elem.clientHeight);
    elem.appendChild(renderer.domElement);
    window.addEventListener(
      "resize",
      () => {
        camera.aspect = elem?.clientWidth / elem?.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(elem.clientWidth, elem.clientHeight);
      },
      false
    );
    renderer.setSize(elem.offsetHeight, elem.offsetWidth);
    let camera = new THREE.PerspectiveCamera(
      50,
      elem.clientHeight / elem.clientWidth
    );

    const light = new THREE.PointLight(0xffffff, 1);
    scene.add(camera);
    camera.add(light);
    scene.add(new THREE.AxesHelper(5));

    const controls = new OrbitControls(camera, elem);

    camera.position.y = -5;
    camera.position.z = 2;
    function animate() {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }

    window.addEventListener(
      "resize",
      () => {
        camera.aspect = elem.clientHeight / elem.clientWidth;
        camera.updateProjectionMatrix();
        renderer.setSize(elem.clientHeight, elem.clientWidth);
        render();
      },
      false
    );

    animate();
  }

  function loadSTL() {
    loader.load(
      `http://localhost:8000/api/cone?radius=${radius}&hole_radius=${hole_radius}&tip_angle=${tip_angle}`,
      function (geometry) {
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

  onMount(() => {
    loadSTL();
    createViewer();
  });
</script>

<section class="flex flex-row flex-nowrap bg-green-100 w-screen">
  <div class="flex flex-col">
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
    <button
      class="w-40 h-10 rounded-full bg-green-800"
      on:click={() => {
        loader = new STLLoader();
        loadSTL();
      }}
    >
      Generate STL
    </button>
  </div>

  <div class="relative aspect-square flex-1 min-w-0" id="model" />
</section>
