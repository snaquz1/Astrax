const container = document.getElementById("space-bg");

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 2000);
  camera.position.z = 6;

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  function makeStars(count, spread, size, opacity) {
    const geo = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      positions[i3 + 0] = (Math.random() - 0.5) * spread;
      positions[i3 + 1] = (Math.random() - 0.5) * spread;
      positions[i3 + 2] = (Math.random() - 0.5) * spread;
    }

    geo.setAttribute("position", new THREE.BufferAttribute(positions, 3));

    const mat = new THREE.PointsMaterial({
      size,
      transparent: true,
      opacity,
      depthWrite: false
    });

    return new THREE.Points(geo, mat);
  }

  const starsNear = makeStars(1200, 80, 0.02, 0.28);
  const starsFar  = makeStars(1800, 160, 0.015, 0.18);
  scene.add(starsNear, starsFar);

  function makeNebula(x, y, z, scale, opacity) {
    const canvas = document.createElement("canvas");
    canvas.width = canvas.height = 256;
    const ctx = canvas.getContext("2d");

    const g = ctx.createRadialGradient(128, 128, 10, 128, 128, 120);
    g.addColorStop(0, "rgba(140,90,255,1)");
    g.addColorStop(0.5, "rgba(0,180,255,0.55)");
    g.addColorStop(1, "rgba(0,0,0,0)");

    ctx.fillStyle = g;
    ctx.fillRect(0, 0, 256, 256);

    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true, opacity, depthWrite: false });
    const sprite = new THREE.Sprite(mat);
    sprite.position.set(x, y, z);
    sprite.scale.set(scale, scale, 1);
    return sprite;
  }

  const neb1 = makeNebula(-2.2,  1.0, -6, 8, 0.08);
  const neb2 = makeNebula( 2.0, -1.2, -9, 10, 0.06);
  scene.add(neb1, neb2);

  let targetX = 0, targetY = 0;
  window.addEventListener("mousemove", (e) => {
    const nx = (e.clientX / window.innerWidth) * 2 - 1;
    const ny = (e.clientY / window.innerHeight) * 2 - 1;
    targetX = nx * 0.25;
    targetY = ny * 0.18;
  });

  function animate() {
    requestAnimationFrame(animate);

    starsNear.rotation.y += 0.00022;
    starsFar.rotation.y  += 0.00012;

    camera.position.x += (targetX - camera.position.x) * 0.02;
    camera.position.y += (-targetY - camera.position.y) * 0.02;

    renderer.render(scene, camera);
  }
  animate();

  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });