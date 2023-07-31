import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import type { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";

export function createViewer(scene: THREE.Scene) {
  // get appropriate place to insert stl viewer -- element with "model" id
  const elem = document.getElementById("model");
  if (elem == null) {
    return;
  }

  // initialize and insert renderer
  let renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(elem.clientWidth, elem.clientHeight);
  elem.appendChild(renderer.domElement);
  window.addEventListener(
    "resize",
    () => {
      camera.aspect = elem.clientWidth / elem.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(elem.clientWidth, elem.clientHeight);
      renderer.render(scene, camera);
    },
    false
  );

  // set camera location and add light
  let camera = new THREE.PerspectiveCamera(
    50,
    elem.clientWidth / elem.clientHeight
  );
  scene.add(camera);
  camera.add(new THREE.PointLight(0xffffff, 1));
  camera.position.y = -5;
  camera.position.z = 2;

  // allow for movement + animate
  const controls = new OrbitControls(camera, elem);
  function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
  }

  // run
  animate();
}

export function loadSTL(
  loader: STLLoader,
  scene: THREE.Scene,
  material: THREE.Material,
  api_path: string
) {
  loader.load(
    api_path,
    function (geometry) {
      scene.remove(scene.children[1]); // removes pre-existing mesh, if necessary
      scene.add(new THREE.Mesh(geometry, material));
    },
    (xhr) => {
      console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
    },
    (error) => {
      console.log(error);
    }
  );
}
