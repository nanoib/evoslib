import"./web-ifc-api-BAs6yRon.js";import{d as i,l as m,x as d,Y as l,r as f,F as w,m as p}from"./index-crgZK0po.js";async function u(r="./jsscripts/assets/1_simple.ifc"){const s=await(await fetch(r)).arrayBuffer(),c=new Uint8Array(s),n=await a.load(c);return n.name="example",e.scene.three.add(n),n}const g=document.getElementById("container"),t=new i,h=t.get(m),e=h.create();e.scene=new d(t);e.renderer=new l(t,g);e.camera=new f(t);t.init();e.camera.controls.setLookAt(1,1,-1,0,0,0);e.scene.setup();e.camera.projection.set("Orthographic");e.scene.three.background=null;const a=t.get(w);await a.setup();a.settings.webIfc.COORDINATE_TO_ORIGIN=!0;const I=await u(),o=t.get(p);o.add(I);const b=o.getMesh();e.camera.controls.fitToSphere(b,!0);
