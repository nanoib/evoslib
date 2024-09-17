import * as OBC from "@thatopen/components";

declare global {
  interface Window {
    loadIfcFromFile: () => Promise<void>;
  }
}

// Function to load the IFC file from the same directory
(async function() {
  async function loadIfcFromFile() {
    async function loadIfcFromFileInner(filenameInner: string='1_simple.ifc') {
      const response = await fetch(filenameInner);
      const data = await response.arrayBuffer();
      const buffer = new Uint8Array(data);
      const model = await fragmentIfcLoader.load(buffer);
      // model.name = "example";
      world.scene.three.add(model);
      return model;
    }
    
    // Creating a simple scene with a camera and a renderer
    const container = document.getElementById("container")!;
    const components = new OBC.Components();
    const worlds = components.get(OBC.Worlds);
    const world = worlds.create<
      OBC.SimpleScene,
      OBC.OrthoPerspectiveCamera,
      OBC.SimpleRenderer
    >();
    world.scene = new OBC.SimpleScene(components);
    world.renderer = new OBC.SimpleRenderer(components, container);
    // Using orthographic camera, it's cooler
    // world.camera = new OBC.SimpleCamera(components);
    world.camera = new OBC.OrthoPerspectiveCamera(components);
    components.init();
    world.camera.controls.setLookAt(1, 1, -1, 0, 0, 0);
    world.scene.setup();
    world.camera.projection.set("Orthographic");
    
    // Make the background of the scene transparent
    world.scene.three.background = null;
    
    // Convert IFC to a geometry called Fragments. 
    // Fragments are a lightweight representation of geometry built on top of 
    // THREE.js `InstancedMesh` to make it easy to work with BIM data efficiently
    const fragmentIfcLoader = components.get(OBC.IfcLoader);
    // Configure the path of the WASM files. Getting them from unpkg
    await fragmentIfcLoader.setup();
    // Configure the conversion using the `webIfc` object. 
    // In this example, we will make the IFC model go to the origin of the scene:
    fragmentIfcLoader.settings.webIfc.COORDINATE_TO_ORIGIN = true;
    
    // Load the IFC file when the script runs
    const model = await loadIfcFromFileInner();
    
    
    // Add a bounding box and fit the model to screen
    const fragmentBbox = components.get(OBC.BoundingBoxer);
    fragmentBbox.add(model);
    const bbox = fragmentBbox.getMesh();
    world.camera.controls.fitToSphere(bbox, true);
  }

  (window as any).loadIfcFromFile = loadIfcFromFile;
})();