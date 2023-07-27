<script lang="ts">
  import { onMount } from "svelte";
  import * as THREE from "three";

  let camera: THREE.PerspectiveCamera;
  let scene: THREE.Scene;
  let renderer: THREE.WebGLRenderer;
  let cube: THREE.Mesh<THREE.BoxGeometry, THREE.MeshBasicMaterial>;

  function createViewer() {
    let elem = document.getElementById("model");
    if (elem == null) {
      return;
    }

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(
      75,
      elem.clientWidth / elem.clientHeight,
      1,
      1000
    );

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(elem.clientWidth, elem.clientHeight);
    elem.appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry(1, 1, 1);
    const material = new THREE.MeshBasicMaterial({ color: 0xffffff });
    cube = new THREE.Mesh(geometry, material);
    scene.add(cube);

    camera.position.z = 5;
    camera.position.y = -1;
    camera.position.x = 2;
    renderer.clear();
    renderer.render(scene, camera);
  }

  onMount(() => {
    createViewer();
  });
</script>

<div id="model" style="width: 500px; height: 500px" />
