(function() {

const THREE = window.THREE;

function drawRoundedRect(ctx, x, y, width, height, radius) {
  const r = Math.min(radius, width / 2, height / 2);
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + width - r, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + r);
  ctx.lineTo(x + width, y + height - r);
  ctx.quadraticCurveTo(x + width, y + height, x + width - r, y + height);
  ctx.lineTo(x + r, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function createLabel(text, fill, color = "#081421") {
  const canvas = document.createElement("canvas");
  canvas.width = 320;
  canvas.height = 96;
  const ctx = canvas.getContext("2d");
  ctx.fillStyle = fill;
  drawRoundedRect(ctx, 10, 10, 300, 76, 20);
  ctx.fill();
  ctx.fillStyle = color;
  ctx.font = '600 26px "Trebuchet MS", sans-serif';
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text, 160, 48);
  const sprite = new THREE.Sprite(
    new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(canvas), transparent: true, depthWrite: false })
  );
  sprite.scale.set(2.9, 0.86, 1);
  return sprite;
}

function createRenderer(canvas) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(canvas.clientWidth || canvas.width || 1, canvas.clientHeight || canvas.height || 1, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  return renderer;
}

function createControls(camera, canvas, target, options = {}) {
  const controls = new THREE.OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.enableRotate = options.enableRotate ?? true;
  controls.enablePan = options.enablePan ?? false;
  controls.enableZoom = options.enableZoom ?? true;
  controls.rotateSpeed = options.rotateSpeed ?? 0.7;
  controls.zoomSpeed = options.zoomSpeed ?? 0.8;
  controls.minDistance = options.minDistance ?? 3;
  controls.maxDistance = options.maxDistance ?? 24;
  controls.target.copy(target);
  controls.update();
  return controls;
}

function resizeRenderer(renderer, camera, canvas) {
  const width = canvas.clientWidth || canvas.width || 1;
  const height = canvas.clientHeight || canvas.height || 1;
  renderer.setSize(width, height, false);
  camera.aspect = width / Math.max(height, 1);
  camera.updateProjectionMatrix();
}

function getEnvironmentPalette(environment) {
  if (environment === "stadium") {
    return { background: 0x86c5ff, ground: 0x1b8a5a, platform: 0xdb6b2f, accent: 0xffdf64, fog: 0xd9eefc };
  }
  if (environment === "lab") {
    return { background: 0xd7eef8, ground: 0xd8e2ea, platform: 0x8ca3b3, accent: 0x3a86ff, fog: 0xf1f8ff };
  }
  return { background: 0x8bc6ff, ground: 0x4d9f63, platform: 0x334b8c, accent: 0xffc857, fog: 0xe7f5ff };
}

function makeFallback(canvas, title, message, accent = "#7dd3fc") {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  if (!ctx) return;
  const width = canvas.width || 960;
  const height = canvas.height || 640;
  const g = ctx.createLinearGradient(0, 0, width, height);
  g.addColorStop(0, "#071427");
  g.addColorStop(1, "#153b68");
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, width, height);
  ctx.fillStyle = accent;
  ctx.font = '700 28px "Segoe UI", sans-serif';
  ctx.fillText(title, 36, 56);
  ctx.fillStyle = "#f8fbff";
  ctx.font = '500 20px "Segoe UI", sans-serif';
  (message.match(/.{1,58}(\s|$)/g) || [message]).slice(0, 5).forEach((line, i) => {
    ctx.fillText(line.trim(), 36, 108 + i * 34);
  });
}

function createTutorStage(canvas) {
  if (!canvas) return null;

  const renderer = createRenderer(canvas);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x071427);
  scene.fog = new THREE.Fog(0x071427, 7, 18);
  const camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
  camera.position.set(0, 1.8, 5.8);
  const controls = createControls(camera, canvas, new THREE.Vector3(0, 1.2, 0), { minDistance: 3.8, maxDistance: 10, enablePan: false });

  scene.add(
    new THREE.HemisphereLight(0xe9f7ff, 0x1c314b, 1.35),
    (() => { const l = new THREE.DirectionalLight(0xffffff, 1.7); l.position.set(6, 10, 5); return l; })(),
    (() => { const l = new THREE.PointLight(0x7dd3fc, 1.4, 30); l.position.set(0, 5, -5); return l; })()
  );

  const avatar = new THREE.Group();
  const torso = new THREE.Mesh(new THREE.CapsuleGeometry(1.05, 1.7, 8, 16), new THREE.MeshStandardMaterial({ color: 0xff7f50, roughness: 0.86 }));
  torso.position.y = -0.35;
  avatar.add(torso);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.86, 40, 40), new THREE.MeshStandardMaterial({ color: 0xf4d1b4, roughness: 0.82 }));
  head.position.y = 1.55;
  avatar.add(head);
  const portraitMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0, depthWrite: false });
  const portraitPlane = new THREE.Mesh(new THREE.PlaneGeometry(1.9, 2.35), portraitMaterial);
  portraitPlane.position.set(0, 1.05, 0.92);
  portraitPlane.visible = false;
  avatar.add(portraitPlane);
  const halo = new THREE.Mesh(new THREE.TorusGeometry(1.28, 0.03, 16, 90), new THREE.MeshBasicMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.22 }));
  halo.rotation.x = Math.PI / 2;
  halo.position.set(0, 1.02, -0.4);
  avatar.add(halo);

  const armMaterial = new THREE.MeshStandardMaterial({ color: 0xf4d1b4, roughness: 0.82 });
  const armL = new THREE.Mesh(new THREE.CapsuleGeometry(0.35, 1.4, 8, 16), armMaterial);
  armL.position.set(-1.45, 0.2, 0);
  avatar.add(armL);
  const armR = new THREE.Mesh(new THREE.CapsuleGeometry(0.35, 1.4, 8, 16), armMaterial);
  armR.position.set(1.45, 0.2, 0);
  avatar.add(armR);

  scene.add(avatar);

  const stage = new THREE.Mesh(new THREE.CylinderGeometry(2.7, 3.4, 0.34, 48), new THREE.MeshStandardMaterial({ color: 0x13203a, roughness: 0.92 }));
  stage.position.y = -1.48;
  scene.add(stage);
  const grid = new THREE.GridHelper(8, 18, 0x324a6d, 0x1a2942);
  grid.position.y = -1.32;
  scene.add(grid);

  let currentBehavior = "idle";
  let targetColor = new THREE.Color(0x071427);
  let currentPortraitUrl = "";
  const portraitLoader = new THREE.TextureLoader();
  const portraitCache = new Map();

  function applyPortrait(url) {
    const nextUrl = (url || "").trim();
    if (!nextUrl) {
      currentPortraitUrl = "";
      portraitPlane.visible = false;
      portraitMaterial.map = null;
      portraitMaterial.opacity = 0;
      head.material.transparent = false;
      head.material.opacity = 1;
      return;
    }

    currentPortraitUrl = nextUrl;
    portraitPlane.visible = true;
    portraitMaterial.opacity = 1;
    head.material.transparent = true;
    head.material.opacity = 0.12;
    if (portraitCache.has(nextUrl)) {
      portraitMaterial.map = portraitCache.get(nextUrl);
      portraitMaterial.needsUpdate = true;
      return;
    }

    portraitLoader.load(
      nextUrl,
      (texture) => {
        if (texture && "colorSpace" in texture && THREE.SRGBColorSpace) {
          texture.colorSpace = THREE.SRGBColorSpace;
        }
        portraitCache.set(nextUrl, texture);
        if (currentPortraitUrl === nextUrl) {
          portraitMaterial.map = texture;
          portraitMaterial.needsUpdate = true;
        }
      },
      undefined,
      () => {
        if (currentPortraitUrl === nextUrl) {
          portraitPlane.visible = false;
          portraitMaterial.map = null;
          portraitMaterial.opacity = 0;
        }
      }
    );
  }

  function updateAppearance(detail) {
    const visuals = (detail && detail.visuals) || {};
    head.material.color.set(visuals.skin || "#f4d1b4");
    armL.material.color.set(visuals.skin || "#f4d1b4");
    armR.material.color.set(visuals.skin || "#f4d1b4");
    torso.material.color.set(visuals.outfit || "#ff7f50");
    halo.material.color.set((detail && detail.avatar && detail.avatar.accent) || "#7dd3fc");
    applyPortrait(detail && detail.avatar && detail.avatar.portrait_url);
    
    // Check behavior update
    currentBehavior = (detail && detail.behavior) || "idle";
    
    let bgColor = (detail && detail.avatar && detail.avatar.stageBackground) || 0x071427;
    if (currentBehavior === "coach") bgColor = 0x240905;
    else if (currentBehavior === "lounge") bgColor = 0x071b26;
    else if (currentBehavior === "focus") bgColor = 0x051d18;
    
    targetColor.set(bgColor);
  }

  function animate(time) {
    resizeRenderer(renderer, camera, canvas);
    const t = time * 0.001;
    
    scene.background.lerp(targetColor, 0.02);
    scene.fog.color.lerp(targetColor, 0.02);

    let bBobble = Math.sin(t * 1.4) * 0.04;
    let bRotY = Math.sin(t * 0.7) * 0.2;
    let haloRot = 0.002;
    let pitch = 0;

    let armLRotZ = 0.2;
    let armRRotZ = -0.2;
    let armRotX = Math.sin(t * 1.5) * 0.05;

    if (currentBehavior === "coach") {
      bBobble = Math.abs(Math.sin(t * 2.5)) * 0.08 - 0.05;
      bRotY = Math.sin(t * 3) * 0.1;
      pitch = 0.15; // Leaning forward
      haloRot = 0.01;
      armLRotZ = 0.5 + Math.sin(t * 5) * 0.1;
      armRRotZ = -0.5 - Math.sin(t * 5) * 0.1;
      armRotX = -0.4;
    } else if (currentBehavior === "lounge") {
      bBobble = Math.sin(t * 0.8) * 0.03 - 0.1;
      bRotY = Math.sin(t * 0.4) * 0.15;
      pitch = -0.1; // Leaning back relaxed
      haloRot = 0.001;
      armLRotZ = 0.15;
      armRRotZ = -0.15;
      armRotX = 0;
    } else if (currentBehavior === "focus") {
      bBobble = 0.0;
      bRotY = 0.0;
      pitch = 0.05;
      haloRot = 0.005;
      armLRotZ = 0.1;
      armRRotZ = -0.1;
      armRotX = -0.2;
    }

    // Lerp transform to smooth transitions
    avatar.rotation.y += (bRotY - avatar.rotation.y) * 0.1;
    avatar.rotation.x += (pitch - avatar.rotation.x) * 0.1;
    avatar.position.y += (bBobble - avatar.position.y) * 0.1;
    halo.rotation.z += haloRot;

    armL.rotation.z += (armLRotZ - armL.rotation.z) * 0.1;
    armR.rotation.z += (armRRotZ - armR.rotation.z) * 0.1;
    armL.rotation.x += (armRotX - armL.rotation.x) * 0.1;
    armR.rotation.x += (armRotX - armR.rotation.x) * 0.1;

    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);
  return { updateAppearance, refresh: () => { resizeRenderer(renderer, camera, canvas); controls.update(); renderer.render(scene, camera); } };
}

function createConceptStage(canvas) {
  if (!canvas) return null;

  const renderer = createRenderer(canvas);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a1a33);
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(8.5, 4.8, 9.5);
  const controls = createControls(camera, canvas, new THREE.Vector3(0, 1.7, 0), { minDistance: 4.4, maxDistance: 22, enablePan: true });

  scene.add(
    new THREE.HemisphereLight(0xe9f7ff, 0x1c314b, 1.2),
    (() => { const l = new THREE.DirectionalLight(0xffffff, 1.55); l.position.set(8, 10, 6); return l; })(),
    (() => { const l = new THREE.PointLight(0x7dd3fc, 1.2, 40); l.position.set(0, 6, -6); return l; })()
  );

  const ground = new THREE.Mesh(new THREE.CircleGeometry(26, 64), new THREE.MeshStandardMaterial({ color: 0x17304f, roughness: 0.96 }));
  ground.rotation.x = -Math.PI / 2;
  scene.add(ground);
  const rings = new THREE.Group();
  for (let radius = 4; radius <= 20; radius += 4) {
    const pts = [];
    for (let i = 0; i < 48; i += 1) {
      const theta = (i / 48) * Math.PI * 2;
      pts.push(new THREE.Vector3(Math.cos(theta) * radius, 0.02, Math.sin(theta) * radius));
    }
    rings.add(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.14 })));
  }
  scene.add(rings);

  const skyline = new THREE.Group();
  for (let i = 0; i < 8; i += 1) {
    const h = 2.2 + i * 0.36;
    const tower = new THREE.Mesh(new THREE.BoxGeometry(1 + (i % 2) * 0.28, h, 1), new THREE.MeshStandardMaterial({ color: 0xa3b6cb, transparent: true, opacity: 0.36 }));
    tower.position.set(-8 + i * 2, h / 2, -7 - (i % 3));
    skyline.add(tower);
  }
  scene.add(skyline);

  const state = {
    mode: "idle",
    startTime: 0,
    caughtAt: 0,
    motionScale: 0.22,
    baseHeight: 4.8,
    sceneTitle: "3D Concept Space",
    sceneScenario: "Ask for a real-life scenario and rotate it with your mouse.",
    sceneHint: "Drag to inspect from every angle",
    velocity: 18,
    angle: 42,
    launcherHeight: 8,
    environment: "rooftop",
    characters: { thrower: { name: "Sky Runner", palette: "sunrise" }, catcher: { name: "Coach Nova", palette: "teal" } },
    objects: {},
  };

  const idleGroup = new THREE.Group();
  const palette = [0xff8fab, 0x7dd3fc, 0xfecf6a, 0x86efac, 0xc4b5fd, 0xf9a8d4];
  const idleMeta = [];
  [
    { x: -2.8, y: 1.2, z: -0.35, r: 0.38, c: palette[0] },
    { x: -1.25, y: 2.15, z: 0.42, r: 0.28, c: palette[1] },
    { x: 0, y: 1.45, z: -0.18, r: 0.46, c: palette[2] },
    { x: 1.35, y: 2.45, z: 0.18, r: 0.31, c: palette[3] },
    { x: 2.9, y: 1.3, z: -0.28, r: 0.36, c: palette[4] },
    { x: 0.85, y: 0.88, z: 0.48, r: 0.24, c: palette[5] },
  ].forEach((item, index) => {
    const node = new THREE.Mesh(new THREE.SphereGeometry(item.r, 28, 28), new THREE.MeshStandardMaterial({ color: item.c, roughness: 0.24, metalness: 0.1, emissive: item.c, emissiveIntensity: 0.16 }));
    node.position.set(item.x, item.y, item.z);
    idleGroup.add(node);
    idleMeta.push({ baseX: item.x, baseY: item.y, baseZ: item.z, phase: index * 0.8, amplitude: 0.16 + (index % 3) * 0.04 });
  });
  const idleCore = new THREE.Mesh(new THREE.SphereGeometry(0.95, 40, 40), new THREE.MeshStandardMaterial({ color: 0x2d7dff, emissive: 0x5fb3ff, emissiveIntensity: 0.42, roughness: 0.18 }));
  idleCore.position.set(0, 1.55, 0);
  idleGroup.add(idleCore);
  const idleRing = new THREE.Mesh(new THREE.TorusGeometry(3.4, 0.05, 18, 120), new THREE.MeshBasicMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.26 }));
  idleRing.rotation.x = Math.PI / 2.2;
  idleRing.position.y = 1.55;
  idleGroup.add(idleRing);
  const idleLabel = makeLabel("3D Concept Space", "#0f1c33", "#edf4ff");
  idleLabel.position.set(0, 4.2, 0);
  idleLabel.scale.set(3.2, 0.92, 1);
  idleGroup.add(idleLabel);
  const idleScenario = makeLabel("Ask for a real-life scenario and rotate it with your mouse.", "#dbeafe");
  idleScenario.position.set(0, 3.15, 0);
  idleScenario.scale.set(3.5, 0.84, 1);
  idleGroup.add(idleScenario);
  const idleHint = makeLabel("Drag to inspect from every angle", "#ccfbf1");
  idleHint.position.set(0, 0.42, -3.2);
  idleHint.scale.set(2.8, 0.72, 1);
  idleGroup.add(idleHint);
  scene.add(idleGroup);

  function clearDynamicScene() {
    Object.values(state.objects || {}).forEach((value) => {
      if (Array.isArray(value)) {
        value.forEach((item) => item && scene.remove(item));
      } else if (value) {
        scene.remove(value);
      }
    });
    state.objects = {};
  }

  function getPalette(environment) {
    if (environment === "stadium") return { background: 0x86c5ff, ground: 0x1b8a5a, platform: 0xdb6b2f, accent: 0xffdf64, fog: 0xd9eefc };
    if (environment === "lab") return { background: 0xd7eef8, ground: 0xd8e2ea, platform: 0x8ca3b3, accent: 0x3a86ff, fog: 0xf1f8ff };
    return { background: 0x8bc6ff, ground: 0x4d9f63, platform: 0x334b8c, accent: 0xffc857, fog: 0xe7f5ff };
  }

  function computeLanding() {
    const radians = THREE.MathUtils.degToRad(state.angle);
    const vx = state.velocity * Math.cos(radians);
    const vy = state.velocity * Math.sin(radians);
    const flightTime = (vy + Math.sqrt(vy * vy + 2 * 9.8 * state.launcherHeight)) / 9.8;
    return { time: flightTime, x: vx * flightTime };
  }

  function createCharacter(name, paletteName) {
    const palettes = { sunrise: { skin: 0xf4c7a1, cloth: 0xff7a59, accent: "#fff3d9" }, teal: { skin: 0xf2c6a2, cloth: 0x168aad, accent: "#dcfff9" }, default: { skin: 0xf4c7a1, cloth: 0x344e41, accent: "#edf6f9" } };
    const p = palettes[paletteName] || palettes.default;
    const group = new THREE.Group();
    const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.16, 0.7, 6, 12), new THREE.MeshStandardMaterial({ color: p.cloth, roughness: 0.7 }));
    body.position.y = 0.65;
    group.add(body);
    const head = new THREE.Mesh(new THREE.SphereGeometry(0.2, 20, 20), new THREE.MeshStandardMaterial({ color: p.skin, roughness: 0.9 }));
    head.position.y = 1.42;
    group.add(head);
    const armMaterial = new THREE.MeshStandardMaterial({ color: p.skin, roughness: 0.85 });
    const armL = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.42, 4, 8), armMaterial);
    armL.position.set(-0.22, 0.96, 0);
    armL.rotation.z = 0.18;
    group.add(armL);
    const armR = armL.clone();
    armR.position.x = 0.22;
    armR.rotation.z = -0.18;
    group.add(armR);
    const badge = makeLabel(name, p.accent);
    badge.position.set(0, 2.15, 0);
    group.add(badge);
    group.userData = { armL, armR };
    return group;
  }

  function buildProjectileScene() {
    clearDynamicScene();
    const p = getPalette(state.environment);
    scene.background = new THREE.Color(p.background);
    scene.fog = new THREE.Fog(p.fog, 18, 40);
    ground.material.color.setHex(p.ground);

    const landing = computeLanding();
    const scale = Math.max(0.16, Math.min(0.28, 7.5 / Math.max(landing.x || 1, 1)));
    const baseHeight = Math.max(4.4, state.launcherHeight * scale * 0.9 + 2.8);
    state.motionScale = scale;
    state.baseHeight = baseHeight;

    const group = new THREE.Group();
    scene.add(group);
    const building = new THREE.Mesh(new THREE.BoxGeometry(3.6, baseHeight + 0.9, 3.4), new THREE.MeshStandardMaterial({ color: p.platform, roughness: 0.82, metalness: 0.08, emissive: p.platform, emissiveIntensity: 0.04 }));
    building.position.set(0, (baseHeight + 0.9) / 2, 0);
    group.add(building);
    const roof = new THREE.Mesh(new THREE.BoxGeometry(4.1, 0.18, 3.9), new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.7 }));
    roof.position.set(0, baseHeight + 0.48, 0);
    group.add(roof);

    const title = makeLabel(state.sceneTitle || "Projectile Motion", "#fff7cc");
    title.position.set(0, baseHeight + 3.15, 0);
    const story = makeLabel(state.sceneScenario || "A ball thrown from a roof to a catcher below.", "#dbeafe");
    story.position.set(0, baseHeight + 2.35, 0);
    story.scale.set(3.25, 0.84, 1);
    const hint = makeLabel(state.sceneHint || "Drag with mouse to rotate and inspect the full flight path.", "#ccfbf1");
    hint.position.set(-2.55, baseHeight + 0.2, 2.2);
    hint.scale.set(2.55, 0.7, 1);
    group.add(title, story, hint);

    const thrower = createCharacter(state.characters.thrower.name, state.characters.thrower.palette);
    thrower.position.set(-1.05, baseHeight + 0.62, 0);
    thrower.rotation.y = Math.PI * 0.12;
    group.add(thrower);
    const catcher = createCharacter(state.characters.catcher.name, state.characters.catcher.palette);
    group.add(catcher);

    const ball = new THREE.Mesh(new THREE.SphereGeometry(0.18, 22, 22), new THREE.MeshStandardMaterial({ color: p.accent, emissive: p.accent, emissiveIntensity: 0.18, roughness: 0.35 }));
    group.add(ball);
    const targetMarker = new THREE.Mesh(new THREE.TorusGeometry(0.52, 0.05, 16, 64), new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.1 }));
    targetMarker.rotation.x = Math.PI / 2;
    group.add(targetMarker);

    const points = [];
    const radians = THREE.MathUtils.degToRad(state.angle);
    for (let t = 0; t <= landing.time; t += 0.05) {
      const x = state.velocity * Math.cos(radians) * t * scale;
      const y = baseHeight + state.velocity * Math.sin(radians) * t * scale - 4.9 * t * t * scale;
      points.push(new THREE.Vector3(x, y, 0));
    }
    const path = new THREE.Line(new THREE.BufferGeometry().setFromPoints(points), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 }));
    group.add(path);
    const trail = [];
    points.filter((_, i) => i % 5 === 0).forEach((pt) => {
      const glow = new THREE.Mesh(new THREE.SphereGeometry(0.05, 10, 10), new THREE.MeshBasicMaterial({ color: 0xfff1b3, transparent: true, opacity: 0.4 }));
      glow.position.copy(pt);
      trail.push(glow);
      group.add(glow);
    });

    catcher.position.set(landing.x * scale, 0, 0);
    targetMarker.position.set(landing.x * scale, 0.08, 0);
    ball.position.set(-0.5, baseHeight + 1.05, 0);
    camera.position.set(10.5, Math.max(5.8, baseHeight * 0.95), 12.5);
    controls.target.set(landing.x * scale * 0.45, Math.max(1.8, baseHeight * 0.55), 0);
    controls.update();
    state.startTime = 0;
    state.caughtAt = 0;
    state.objects = { group, building, roof, thrower, catcher, ball, targetMarker, path, trail, title, story, hint };
  }

  function buildFieldLinesScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x050c18);
    ground.material.color.setHex(0x0a1626);
    
    const group = new THREE.Group();
    scene.add(group);
    
    const posCharge = new THREE.Mesh(new THREE.SphereGeometry(0.8, 32, 32), new THREE.MeshStandardMaterial({ color: 0xff3b30, emissive: 0xff453a, emissiveIntensity: 0.6, roughness: 0.1 }));
    posCharge.position.set(-3, 2, 0);
    const negCharge = new THREE.Mesh(new THREE.SphereGeometry(0.8, 32, 32), new THREE.MeshStandardMaterial({ color: 0x0a84ff, emissive: 0x0a84ff, emissiveIntensity: 0.6, roughness: 0.1 }));
    negCharge.position.set(3, 2, 0);
    group.add(posCharge, negCharge);
    
    const title = makeLabel(state.sceneTitle || "Electrostatics", "#050c18", "#ff453a");
    title.position.set(0, 5.5, 0);
    group.add(title);
    
    const particles = [];
    for(let i=0; i<150; i++) {
        const p = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffcc00, transparent: true, opacity: 0.8 }));
        p.position.set((Math.random()-0.5)*10, 0.5 + Math.random()*3, (Math.random()-0.5)*10);
        group.add(p);
        particles.push(p);
    }
    
    camera.position.set(0, 4, 12);
    controls.target.set(0, 2, 0);
    controls.update();

    state.objects = { group, posCharge, negCharge, particles, title };
  }

  function buildProbabilityBagScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x111827);
    ground.material.color.setHex(0x1f2937);

    const group = new THREE.Group();
    scene.add(group);

    const bag = new THREE.Mesh(new THREE.CylinderGeometry(2.5, 2, 3, 32, 1, true), new THREE.MeshStandardMaterial({ color: 0xf3f4f6, transparent: true, opacity: 0.2, side: THREE.DoubleSide }));
    bag.position.set(0, 1.5, 0);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(2, 2, 0.2, 32), new THREE.MeshStandardMaterial({ color: 0xf3f4f6, roughness: 0.8 }));
    base.position.set(0, 0, 0);
    group.add(bag, base);

    const title = makeLabel(state.sceneTitle || "Probability Bag", "#111827", "#10b981");
    title.position.set(0, 4.5, 0);
    group.add(title);

    const balls = [];
    const colors = [0xef4444, 0xef4444, 0xef4444, 0x3b82f6, 0x3b82f6, 0x10b981];
    colors.forEach((c, i) => {
        const b = new THREE.Mesh(new THREE.SphereGeometry(0.4, 32, 32), new THREE.MeshStandardMaterial({ color: c, roughness: 0.4 }));
        b.position.set((Math.random()-0.5)*2, 0.5 + Math.random()*2, (Math.random()-0.5)*2);
        b.userData = { vy: 0, bounceOffset: Math.random() * Math.PI * 2 };
        group.add(b);
        balls.push(b);
    });

    camera.position.set(0, 4, 9);
    controls.target.set(0, 1.5, 0);
    controls.update();

    state.objects = { group, bag, base, balls, title };
  }

  function buildShopPercentagesScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x0f172a);
    ground.material.color.setHex(0x1e293b);

    const group = new THREE.Group();
    scene.add(group);

    const title = makeLabel(state.sceneTitle || "Shop Percentages", "#0f172a", "#f59e0b");
    title.position.set(0, 5, 0);
    group.add(title);

    const bars = [];
    const barData = [
       { h: 3.0, c: 0x64748b, x: -3, t: "Cost Price" },
       { h: 4.5, c: 0xeab308, x: 0, t: "Markup" },
       { h: 3.8, c: 0x10b981, x: 3, t: "Selling Price" }
    ];
    barData.forEach(d => {
       const bar = new THREE.Mesh(new THREE.BoxGeometry(1.5, d.h, 1.5), new THREE.MeshStandardMaterial({ color: d.c, roughness: 0.5 }));
       bar.position.set(d.x, d.h/2, 0);
       group.add(bar);
       const lbl = makeLabel(d.t, "#1e293b", "#ffffff");
       lbl.position.set(d.x, d.h + 0.6, 0);
       lbl.scale.set(2, 0.6, 1);
       group.add(lbl);
       bars.push({ mesh: bar, label: lbl, tgtH: d.h });
    });

    camera.position.set(0, 4, 10);
    controls.target.set(0, 2, 0);
    controls.update();

    state.objects = { group, bars, title };
  }

  function buildConceptFlowScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x0f1c33);
    scene.fog = new THREE.Fog(0x0f1c33, 10, 36);
    ground.material.color.setHex(0x1c3358);

    const group = new THREE.Group();
    scene.add(group);

    const title = makeLabel(state.sceneTitle || "Concept Bridge", "#0f1c33", "#edf4ff");
    title.position.set(0, 5.2, 0);
    group.add(title);

    const scenario = makeLabel(state.sceneScenario || "Turn the idea into a cause, rule, and effect chain.", "#dbeafe");
    scenario.position.set(0, 4.35, 0);
    scenario.scale.set(3.35, 0.84, 1);
    group.add(scenario);

    const hint = makeLabel(state.sceneHint || "Rotate the scene to inspect the full reasoning flow.", "#ccfbf1");
    hint.position.set(0, 3.45, 0);
    hint.scale.set(3.0, 0.74, 1);
    group.add(hint);

    const nodes = [
      { label: "Cause", x: -3.2, color: 0x60a5fa },
      { label: "Rule", x: 0, color: 0x7dd3fc },
      { label: "Effect", x: 3.2, color: 0xfbbf24 },
    ];
    const nodeMeshes = [];
    nodes.forEach((node, index) => {
      const mesh = new THREE.Mesh(
        new THREE.SphereGeometry(0.72, 32, 32),
        new THREE.MeshStandardMaterial({ color: node.color, emissive: node.color, emissiveIntensity: 0.24, roughness: 0.28 })
      );
      mesh.position.set(node.x, 1.55, 0);
      mesh.userData = { pulseOffset: index * 0.8 };
      group.add(mesh);
      nodeMeshes.push(mesh);

      const label = makeLabel(node.label, "#10213d", "#edf4ff");
      label.position.set(node.x, 2.8, 0);
      label.scale.set(1.9, 0.58, 1);
      group.add(label);
    });

    const connectorPoints = [
      new THREE.Vector3(-2.4, 1.55, 0),
      new THREE.Vector3(-0.35, 1.55, 0),
      new THREE.Vector3(0.35, 1.55, 0),
      new THREE.Vector3(2.4, 1.55, 0),
    ];
    const connector = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(connectorPoints),
      new THREE.LineBasicMaterial({ color: 0xdbeafe, transparent: true, opacity: 0.72 })
    );
    group.add(connector);

    const arrows = [];
    [
      { x: -1.55, label: "Why it starts", color: 0x7dd3fc },
      { x: 1.55, label: "Why it changes", color: 0xfbbf24 },
    ].forEach((item, index) => {
      const arrow = new THREE.Mesh(
        new THREE.ConeGeometry(0.14, 0.42, 20),
        new THREE.MeshStandardMaterial({ color: item.color, emissive: item.color, emissiveIntensity: 0.16, roughness: 0.26 })
      );
      arrow.rotation.z = Math.PI / 2;
      arrow.position.set(item.x, 1.55, 0);
      group.add(arrow);
      arrows.push(arrow);

      const badge = makeLabel(item.label, "#13233f", "#edf4ff");
      badge.position.set(item.x, 0.65 - index * 0.05, 0);
      badge.scale.set(2.2, 0.6, 1);
      group.add(badge);
    });

    camera.position.set(0, 4.5, 11);
    controls.target.set(0, 1.7, 0);
    controls.update();

    state.objects = { group, title, scenario, hint, nodeMeshes, connector, arrows };
  }

  function updateVisual(visual) {
    const animation = visual && visual.animation ? visual.animation : null;
    if (!animation) {
      state.mode = "idle";
      clearDynamicScene();
      scene.background = new THREE.Color(0x0a1a33);
      ground.material.color.setHex(0x1f3558);
      camera.position.set(7.8, 4.9, 8.8);
      camera.lookAt(0, 1.8, 0);
      controls.target.set(0, 1.8, 0);
      controls.update();
      idleGroup.visible = true;
      return;
    }

    idleGroup.visible = false;
    const config = (visual && visual.scene_config) || {};
    if (animation.type === "projectile") {
      const launch = config.launch || {};
      state.mode = "projectile";
      state.sceneTitle = visual.title || "Projectile Motion Scene";
      state.sceneScenario = visual.scenario || "A ball being thrown from the roof to a person below.";
      state.sceneHint = config.interaction_hint || "Drag with mouse to rotate and inspect the full flight path.";
      state.velocity = Number(launch.velocity || 18);
      state.angle = Number(launch.angle || 42);
      state.launcherHeight = Number(launch.height || 8);
      state.environment = config.environment || "rooftop";
      state.characters = config.characters || state.characters;
      buildProjectileScene();
      return;
    }

    if (animation.type === "field_lines") {
      state.mode = "field_lines";
      state.sceneTitle = visual.title || "Electric Field Lines";
      buildFieldLinesScene();
      return;
    }

    if (animation.type === "probability_bag") {
      state.mode = "probability_bag";
      state.sceneTitle = visual.title || "Probability & Sample Space";
      buildProbabilityBagScene();
      return;
    }

    if (animation.type === "shop_percentages") {
      state.mode = "shop_percentages";
      state.sceneTitle = visual.title || "Percentage Margins";
      buildShopPercentagesScene();
      return;
    }

    if (animation.type === "concept_flow") {
      state.mode = "concept_flow";
      state.sceneTitle = visual.title || "Concept Bridge";
      state.sceneScenario = visual.scenario || "Turn the idea into a cause, rule, and effect chain.";
      state.sceneHint = (visual.scene_config && visual.scene_config.interaction_hint) || "Rotate the scene to inspect the reasoning chain.";
      buildConceptFlowScene();
      return;
    }

    state.mode = "idle";
    clearDynamicScene();
    scene.background = new THREE.Color(0x0a1a33);
    ground.material.color.setHex(0x1f3558);
    const status = makeLabel(visual.title || "Scene ready", "#0f1c33", "#edf4ff");
    status.position.set(0, 2.5, 0);
    scene.add(status);
    state.objects = { status };
  }

  function animate(time) {
    resizeRenderer(renderer, camera, canvas);
    const t = time * 0.001;
    if (state.mode === "projectile" && state.objects.ball && state.objects.thrower && state.objects.catcher) {
      if (!state.startTime) state.startTime = time;
      const elapsed = (time - state.startTime) / 1000;
      const landing = computeLanding();
      const radians = THREE.MathUtils.degToRad(state.angle);
      const vx = state.velocity * Math.cos(radians);
      const vy = state.velocity * Math.sin(radians);
      const scale = state.motionScale || 0.22;
      const baseHeight = state.baseHeight || 4.8;
      state.objects.thrower.userData.armL.rotation.z = 0.48 + Math.sin(time * 0.004) * 0.08;
      state.objects.thrower.userData.armR.rotation.z = -0.82;
      if (!state.caughtAt) {
        const x = vx * elapsed * scale;
        const y = baseHeight + vy * elapsed * scale - 4.9 * elapsed * elapsed * scale;
        state.objects.ball.position.set(x, y, 0);
        if (elapsed >= landing.time) state.caughtAt = time;
      } else {
        state.objects.ball.position.set(landing.x * scale, 1.1, 0);
        if (time - state.caughtAt > 1200) {
          state.startTime = time;
          state.caughtAt = 0;
        }
      }
      state.objects.targetMarker.rotation.z += 0.014;
    } else if (state.mode === "field_lines" && state.objects.particles) {
      // Simulate field line flow
      const q1 = state.objects.posCharge.position;
      const q2 = state.objects.negCharge.position;
      state.objects.particles.forEach(p => {
         const d1 = new THREE.Vector3().subVectors(p.position, q1);
         const d2 = new THREE.Vector3().subVectors(q2, p.position);
         const f1 = d1.normalize().multiplyScalar(0.04 / Math.max(0.1, d1.lengthSq()));
         const f2 = d2.normalize().multiplyScalar(0.04 / Math.max(0.1, d2.lengthSq()));
         p.position.add(f1).add(f2);
         if (p.position.distanceTo(q2) < 0.8 || p.position.distanceTo(q1) > 8 || p.position.y < 0) {
            p.position.set(q1.x + (Math.random()-0.5)*1.2, q1.y + (Math.random()-0.5)*1.2, q1.z + (Math.random()-0.5)*1.2);
         }
      });
      state.objects.group.rotation.y = Math.sin(t * 0.2) * 0.3;
    } else if (state.mode === "probability_bag" && state.objects.balls) {
      state.objects.balls.forEach(b => {
         b.position.y = 0.6 + Math.abs(Math.sin((t * 2) + b.userData.bounceOffset)) * 1.8;
      });
      state.objects.group.rotation.y = t * 0.3;
    } else if (state.mode === "shop_percentages" && state.objects.bars) {
      state.objects.bars.forEach((b, i) => {
         const h = b.tgtH + Math.sin(t * 1.5 + i) * 0.5;
         b.mesh.scale.y = h;
         b.mesh.position.y = h / 2;
         b.label.position.y = h + 0.6;
      });
      state.objects.group.rotation.y = Math.sin(t * 0.5) * 0.2;
    } else if (state.mode === "concept_flow" && state.objects.nodeMeshes) {
      state.objects.nodeMeshes.forEach((node, index) => {
        const pulse = 1 + Math.sin(t * 2 + index) * 0.05;
        node.scale.setScalar(pulse);
      });
      if (state.objects.connector) {
        state.objects.connector.rotation.y = Math.sin(t * 0.6) * 0.08;
      }
      if (state.objects.arrows) {
        state.objects.arrows.forEach((arrow, index) => {
          arrow.position.y = 1.55 + Math.sin(t * 2.2 + index) * 0.08;
        });
      }
      state.objects.group.rotation.y = Math.sin(t * 0.25) * 0.18;
    } else if (state.mode === "idle") {
      idleGroup.rotation.y = t * 0.16;
      idleCore.rotation.y += 0.01;
      idleGroup.children.forEach((node, index) => {
        if (idleMeta[index]) {
          const meta = idleMeta[index];
          node.position.x = meta.baseX + Math.sin(t * 0.9 + meta.phase) * 0.16;
          node.position.y = meta.baseY + Math.sin(t * 1.4 + meta.phase) * meta.amplitude;
          node.position.z = meta.baseZ + Math.cos(t * 1.1 + meta.phase) * 0.14;
        }
      });
      idleRing.rotation.z += 0.004;
    }
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  requestAnimationFrame(animate);
  updateVisual(null);
  return { updateVisual, refresh: () => { resizeRenderer(renderer, camera, canvas); controls.update(); renderer.render(scene, camera); } };
}

const tutorCanvas = document.getElementById("threeTutorCanvas");
const conceptCanvas = document.getElementById("threeConceptCanvas");
const ENABLE_THREE_STUDIO = window.ASTRA_ENABLE_THREE_STUDIO === true;
let tutorStage = null;
let conceptStage = null;

if (ENABLE_THREE_STUDIO) {
  try {
    tutorStage = createTutorStage(tutorCanvas);
  } catch (error) {
    console.error("3D tutor stage failed to initialize:", error);
    makeFallback(tutorCanvas, "3D Tutor Stage", "The tutor scene could not initialize yet. Refresh once more after the page fully loads.", "#f9a8d4");
  }

  try {
    conceptStage = createConceptStage(conceptCanvas);
  } catch (error) {
    console.error("3D concept stage failed to initialize:", error);
    makeFallback(conceptCanvas, "3D Concept Stage", "The concept scene could not initialize yet. Refresh once more after the page fully loads.", "#facc15");
  }
}

window.addEventListener("alt:tutor-appearance", (event) => {
  if (tutorStage) tutorStage.updateAppearance(event.detail || null);
});
window.addEventListener("alt:tutor-behavior", (event) => {
  if (tutorStage) {
    const detail = event.detail || {};
    // Retrieve latest appearance to maintain colors but override behavior
    tutorStage.updateAppearance({ behavior: detail.behavior });
  }
});
window.addEventListener("alt:concept-visual", (event) => {
  if (conceptStage) conceptStage.updateVisual(event.detail || null);
});
window.addEventListener("alt:studio-pane-changed", (event) => {
  const paneId = event && event.detail ? event.detail.paneId : "";
  window.setTimeout(() => {
    if (paneId === "threeConceptPanel" && conceptStage) conceptStage.refresh();
    if (paneId === "threeTutorPanel" && tutorStage) tutorStage.refresh();
  }, 60);
});
window.addEventListener("resize", () => {
  if (tutorStage) tutorStage.refresh();
  if (conceptStage) conceptStage.refresh();
});
window.setTimeout(() => {
  if (conceptStage) conceptStage.refresh();
  if (tutorStage) tutorStage.refresh();
}, 120);

document.addEventListener("click", (e) => {
  const btn = e.target.closest(".tab-button, .sidebar-link");
  if (btn) {
    const tabId = btn.dataset.tabTarget || btn.id || btn.dataset.tabKey || "";
    let behavior = "idle";
    if (tabId.includes("tutor")) behavior = "coach";
    if (tabId.includes("lounge")) behavior = "lounge";
    if (tabId.includes("practice") || tabId.includes("guide") || tabId.includes("lastminute")) behavior = "focus";
    window.dispatchEvent(new CustomEvent("alt:tutor-behavior", { detail: { behavior } }));
  }
});

})();
