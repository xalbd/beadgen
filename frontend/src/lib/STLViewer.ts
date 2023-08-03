import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import type { STLLoader } from "three/examples/jsm/loaders/STLLoader.js";

export function createViewer(scene: THREE.Scene, id_name: string) {
  // get appropriate place to insert stl viewer -- element with "model" id
  const elem = document.getElementById(id_name);
  if (elem == null) {
    return;
  }

  // initialize and insert renderer
  let renderer = new THREE.WebGLRenderer({ antialias: true });
  const styles = window.getComputedStyle(elem);
  renderer.setSize(
    elem.clientWidth - 2 * parseFloat(styles.paddingLeft),
    elem.clientHeight - 2 * parseFloat(styles.paddingTop)
  );
  elem.appendChild(renderer.domElement);
  window.addEventListener(
    "resize",
    () => {
      const height = elem.clientHeight - 2 * parseFloat(styles.paddingTop);
      const width = elem.clientWidth - 2 * parseFloat(styles.paddingLeft);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
      renderer.render(scene, camera);
    },
    false
  );

  // add camera and light in [0]
  let camera = new THREE.PerspectiveCamera(
    50,
    elem.clientWidth / elem.clientHeight
  );
  scene.add(camera);
  camera.add(new THREE.PointLight(0xffffff, 1));

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
      // removes pre-existing mesh/axis
      scene.remove(scene.children[1]);
      scene.remove(scene.children[1]);

      // add mesh in [1]
      let mesh = new THREE.Mesh(geometry, material);
      scene.add(mesh);

      // compute middle of model and extract largest dimension for placement
      let middle = new THREE.Vector3();
      geometry.computeBoundingBox();
      geometry.boundingBox.getCenter(middle);
      mesh.geometry.applyMatrix4(
        new THREE.Matrix4().makeTranslation(-middle.x, -middle.y, -middle.z)
      );
      var largestDimension = Math.max(
        geometry.boundingBox.max.x,
        geometry.boundingBox.max.y,
        geometry.boundingBox.max.z
      );

      // add axis to [2] and position camera
      scene.add(new THREE.AxesHelper(largestDimension * 1.5));
      scene.children[0].position.y = -largestDimension * 3;
      scene.children[0].position.x = 0;
      scene.children[0].position.z = largestDimension * 2;
    },
    (xhr) => {
      console.log((xhr.loaded / xhr.total) * 100 + "% loaded");
    },
    (error) => {
      console.log(error);
    }
  );
}
