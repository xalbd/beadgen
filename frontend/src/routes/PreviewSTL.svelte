<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";
  import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
  import { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";

  function createViewer() {
    let elem = document.getElementById("model");
    if (elem == null) {
      return;
    }

    let camera = new THREE.PerspectiveCamera(
      75,
      elem.clientWidth / elem.clientHeight,
      0.1,
      1000
    );
    let scene = new THREE.Scene();
    let renderer = new THREE.WebGLRenderer({ antialias: true });

    renderer.setSize(elem.clientWidth, elem.clientHeight);
    elem.appendChild(renderer.domElement);
    const light = new THREE.SpotLight();
    light.position.set(20, 20, 20);
    scene.add(light);
    scene.add(new THREE.AxesHelper(5));

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const loader = new STLLoader();
    loader.load(
      "http://localhost:8000/api/cone?radius=1&hole_radius=0.5&tip_angle=90",
      function (geometry) {
        var material = new THREE.MeshPhongMaterial({
          color: 0xff5533,
          specular: 100,
          shininess: 100,
        });
        var mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);
      },
      (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
      },
      (error) => {
        console.log(error);
      }
    );

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
    createViewer();
  });
</script>

<div id="model" style="width: 500px; height: 500px" />
