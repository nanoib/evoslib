import * as OBC from "@thatopen/components";

(function() {
    async function loadIfcFromFile(filename) {
    const container = document.getElementById("container");
    const components = new OBC.Components();

    // Group all components.get calls together
    const worlds = components.get(OBC.Worlds);
    const fragmentIfcLoader = components.get(OBC.IfcLoader);
    const fragmentBbox = components.get(OBC.BoundingBoxer);

    // Create and set up the world
    const world = worlds.create(
        OBC.SimpleScene,
        OBC.OrthoPerspectiveCamera,
        OBC.SimpleRenderer
    );
    world.scene = new OBC.SimpleScene(components);
    world.renderer = new OBC.SimpleRenderer(components, container);
    world.camera = new OBC.OrthoPerspectiveCamera(components);

    // Initialize components and set up the scene
    components.init();
    world.scene.setup();
    world.camera.controls.setLookAt(1, 1, -1, 0, 0, 0);
    world.camera.projection.set("Orthographic");
    world.scene.three.background = null;

    // Set up IFC loader
    await fragmentIfcLoader.setup();
    fragmentIfcLoader.settings.webIfc.COORDINATE_TO_ORIGIN = true;

    // Load and process the IFC file
    const buffer = await fetch(filename).then(response => response.arrayBuffer());
    const model = await fragmentIfcLoader.load(new Uint8Array(buffer));
    model.name = "example";
    world.scene.three.add(model);

    // Add bounding box and fit camera
    fragmentBbox.add(model);
    const bbox = fragmentBbox.getMesh();
    world.camera.controls.fitToSphere(bbox, true);
    }

    window.loadIfcFromFile = loadIfcFromFile;

})();