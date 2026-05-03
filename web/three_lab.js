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

function createRenderer(canvas) {
  const renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: false,
    powerPreference: "high-performance",
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(canvas.clientWidth || canvas.width || 1, canvas.clientHeight || canvas.height || 1, false);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.08;
  return renderer;
}

function drawCanvasFallback(canvas, title, message, accent = "#7dd3fc") {
  if (!canvas) {
    return;
  }
  const width = canvas.width || 960;
  const height = canvas.height || 640;
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    return;
  }
  ctx.clearRect(0, 0, width, height);
  const gradient = ctx.createLinearGradient(0, 0, width, height);
  gradient.addColorStop(0, "#0b1b34");
  gradient.addColorStop(1, "#183f69");
  ctx.fillStyle = gradient;
  ctx.fillRect(0, 0, width, height);

  ctx.fillStyle = accent;
  ctx.font = '700 28px "Segoe UI", sans-serif';
  ctx.fillText(title, 36, 56);

  ctx.fillStyle = "#f8fbff";
  ctx.font = '500 20px "Segoe UI", sans-serif';
  const lines = message.match(/.{1,58}(\s|$)/g) || [message];
  lines.slice(0, 5).forEach((line, index) => {
    ctx.fillText(line.trim(), 36, 108 + index * 34);
  });
}

function createOrbitControls(camera, canvas, target, options = {}) {
  const controls = new THREE.OrbitControls(camera, canvas);
  controls.enableDamping = true;
  controls.dampingFactor = 0.06;
  controls.enableRotate = options.enableRotate ?? true;
  controls.enablePan = options.enablePan ?? false;
  controls.enableZoom = options.enableZoom ?? true;
  controls.rotateSpeed = options.rotateSpeed ?? 0.72;
  controls.zoomSpeed = options.zoomSpeed ?? 0.8;
  controls.minDistance = options.minDistance ?? 3;
  controls.maxDistance = options.maxDistance ?? 20;
  controls.minPolarAngle = options.minPolarAngle ?? 0.25;
  controls.maxPolarAngle = options.maxPolarAngle ?? Math.PI / 2.02;
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

function createLabelSprite(text, background, color = "#081421") {
  const canvas = document.createElement("canvas");
  canvas.width = 320;
  canvas.height = 96;
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = background;
  drawRoundedRect(ctx, 10, 10, 300, 76, 22);
  ctx.fill();

  ctx.fillStyle = color;
  ctx.font = '600 26px "Trebuchet MS", sans-serif';
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(text, 160, 48);

  const texture = new THREE.CanvasTexture(canvas);
  const sprite = new THREE.Sprite(
    new THREE.SpriteMaterial({
      map: texture,
      transparent: true,
      depthWrite: false,
    })
  );
  sprite.scale.set(2.8, 0.82, 1);
  return sprite;
}

function addStudioLights(scene) {
  const ambient = new THREE.HemisphereLight(0xe9f7ff, 0x6c8a57, 1.35);
  const key = new THREE.DirectionalLight(0xffffff, 1.7);
  key.position.set(7, 10, 6);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  const fill = new THREE.DirectionalLight(0xffecd1, 0.8);
  fill.position.set(-5, 4, 6);
  const rim = new THREE.PointLight(0x93c5fd, 1.2, 30);
  rim.position.set(0, 5, -6);
  scene.add(ambient, key, fill, rim);
}

function createTutorStage(canvas) {
  if (!canvas) {
    return null;
  }

  const renderer = createRenderer(canvas);
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0b1320);
  scene.fog = new THREE.Fog(0x0b1320, 8, 18);
  const camera = new THREE.PerspectiveCamera(35, 1, 0.1, 100);
  camera.position.set(0, 1.7, 5.5);
  const controls = createOrbitControls(camera, canvas, new THREE.Vector3(0, 1.25, 0), {
    minDistance: 3.5,
    maxDistance: 10,
    enablePan: false,
  });
  addStudioLights(scene);

  const stage = new THREE.Mesh(
    new THREE.CylinderGeometry(2.8, 3.5, 0.36, 48),
    new THREE.MeshStandardMaterial({ color: 0x14213d, roughness: 0.92, metalness: 0.08 })
  );
  stage.position.y = -1.55;
  scene.add(stage);

  const grid = new THREE.GridHelper(8, 18, 0x324a6d, 0x1a2942);
  grid.position.y = -1.36;
  scene.add(grid);

  const backdrop = new THREE.Mesh(
    new THREE.CylinderGeometry(5.6, 5.8, 6.8, 36, 1, true),
    new THREE.MeshStandardMaterial({
      color: 0x13233a,
      side: THREE.BackSide,
      roughness: 1,
      metalness: 0,
    })
  );
  backdrop.position.y = 1.5;
  scene.add(backdrop);

  const bust = new THREE.Group();
  scene.add(bust);

  const torso = new THREE.Mesh(
    new THREE.CapsuleGeometry(1.1, 1.8, 8, 16),
    new THREE.MeshStandardMaterial({ color: 0xff7f50, roughness: 0.88, metalness: 0.05 })
  );
  torso.position.set(0, -0.45, 0);
  bust.add(torso);

  const neck = new THREE.Mesh(
    new THREE.CylinderGeometry(0.26, 0.3, 0.42, 24),
    new THREE.MeshStandardMaterial({ color: 0xf4d1b4, roughness: 0.9 })
  );
  neck.position.set(0, 0.78, 0.05);
  bust.add(neck);

  const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.88, 40, 40),
    new THREE.MeshStandardMaterial({ color: 0xf4d1b4, roughness: 0.82, metalness: 0.03 })
  );
  head.position.set(0, 1.62, 0.05);
  bust.add(head);

  const hair = new THREE.Mesh(
    new THREE.SphereGeometry(0.92, 40, 40, 0, Math.PI * 2, 0, Math.PI * 0.62),
    new THREE.MeshStandardMaterial({ color: 0x3b2a22, roughness: 0.78, metalness: 0.06 })
  );
  hair.position.set(0, 1.84, 0.02);
  hair.rotation.x = -0.12;
  bust.add(hair);

  const eyeMaterial = new THREE.MeshStandardMaterial({ color: 0x1f2937, roughness: 0.35 });
  const leftEye = new THREE.Mesh(new THREE.SphereGeometry(0.06, 18, 18), eyeMaterial);
  const rightEye = leftEye.clone();
  leftEye.position.set(-0.22, 1.68, 0.78);
  rightEye.position.set(0.22, 1.68, 0.78);
  bust.add(leftEye, rightEye);

  const smile = new THREE.Mesh(
    new THREE.TorusGeometry(0.14, 0.018, 12, 50, Math.PI),
    new THREE.MeshStandardMaterial({ color: 0x7b2b3c, roughness: 0.6 })
  );
  smile.position.set(0, 1.38, 0.8);
  smile.rotation.z = Math.PI;
  bust.add(smile);

  const shoulders = new THREE.Mesh(
    new THREE.BoxGeometry(2.4, 0.55, 1.5),
    new THREE.MeshStandardMaterial({ color: 0xff7f50, roughness: 0.9 })
  );
  shoulders.position.set(0, 0.18, 0);
  shoulders.rotation.z = 0.02;
  bust.add(shoulders);

  const halo = new THREE.Mesh(
    new THREE.TorusGeometry(1.3, 0.03, 16, 90),
    new THREE.MeshBasicMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.2 })
  );
  halo.rotation.x = Math.PI / 2;
  halo.position.set(0, 1.05, -0.45);
  scene.add(halo);

  function updateAppearance(detail) {
    const visuals = (detail && detail.visuals) || {};
    const avatar = (detail && detail.avatar) || {};
    head.material.color.set(visuals.skin || "#f4d1b4");
    neck.material.color.set(visuals.skin || "#f4d1b4");
    hair.material.color.set(visuals.hair || "#3b2a22");
    leftEye.material.color.set(visuals.eyes || "#2a2017");
    rightEye.material.color.set(visuals.eyes || "#2a2017");
    torso.material.color.set(visuals.outfit || avatar.accent || "#ff7f50");
    shoulders.material.color.set(visuals.outfit || avatar.accent || "#ff7f50");
    halo.material.color.set(avatar.accent || "#7dd3fc");
    scene.background = new THREE.Color(avatar.stageBackground || 0x0b1320);
  }

  function animate(time) {
    resizeRenderer(renderer, camera, canvas);
    const t = time * 0.001;
    bust.rotation.y = Math.sin(t * 0.7) * 0.18;
    bust.position.y = Math.sin(t * 1.4) * 0.04;
    halo.rotation.z += 0.002;
    controls.update();
    renderer.render(scene, camera);
    requestAnimationFrame(animate);
  }

  updateAppearance(null);
  requestAnimationFrame(animate);
  return {
    updateAppearance,
    refresh() {
      resizeRenderer(renderer, camera, canvas);
      controls.update();
      renderer.render(scene, camera);
    },
  };
}

function getEnvironmentPalette(environment) {
  if (environment === "stadium") {
    return {
      background: 0x86c5ff,
      ground: 0x1b8a5a,
      platform: 0xdb6b2f,
      accent: 0xffdf64,
      fog: 0xd9eefc,
    };
  }

  if (environment === "lab") {
    return {
      background: 0xd7eef8,
      ground: 0xd8e2ea,
      platform: 0x8ca3b3,
      accent: 0x3a86ff,
      fog: 0xf1f8ff,
    };
  }

  return {
    background: 0x8bc6ff,
    ground: 0x4d9f63,
    platform: 0x334b8c,
    accent: 0xffc857,
    fog: 0xe7f5ff,
  };
}

function createCharacter(name, paletteName) {
  const palettes = {
    sunrise: { skin: 0xf4c7a1, cloth: 0xff7a59, accent: "#fff3d9" },
    teal: { skin: 0xf2c6a2, cloth: 0x168aad, accent: "#dcfff9" },
    default: { skin: 0xf4c7a1, cloth: 0x344e41, accent: "#edf6f9" },
  };
  const palette = palettes[paletteName] || palettes.default;

  const group = new THREE.Group();
  const body = new THREE.Mesh(
    new THREE.CapsuleGeometry(0.16, 0.7, 6, 12),
    new THREE.MeshStandardMaterial({ color: palette.cloth, roughness: 0.7 })
  );
  body.position.y = 0.65;
  group.add(body);

  const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.2, 20, 20),
    new THREE.MeshStandardMaterial({ color: palette.skin, roughness: 0.9 })
  );
  head.position.y = 1.42;
  group.add(head);

  const armMaterial = new THREE.MeshStandardMaterial({ color: palette.skin, roughness: 0.85 });
  const armL = new THREE.Mesh(new THREE.CapsuleGeometry(0.05, 0.42, 4, 8), armMaterial);
  armL.position.set(-0.22, 0.96, 0);
  armL.rotation.z = 0.18;
  group.add(armL);

  const armR = armL.clone();
  armR.position.x = 0.22;
  armR.rotation.z = -0.18;
  group.add(armR);

  const legMaterial = new THREE.MeshStandardMaterial({ color: 0x24343f, roughness: 0.9 });
  const legL = new THREE.Mesh(new THREE.CapsuleGeometry(0.06, 0.5, 4, 8), legMaterial);
  legL.position.set(-0.08, 0.16, 0);
  group.add(legL);

  const legR = legL.clone();
  legR.position.x = 0.08;
  group.add(legR);

  const badge = createLabelSprite(name, palette.accent);
  badge.position.set(0, 2.15, 0);
  group.add(badge);

  group.userData = { armL, armR };
  return group;
}

function createConceptStage(canvas) {
  if (!canvas) {
    return null;
  }

  const renderer = createRenderer(canvas);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
  camera.position.set(9, 5, 10);
  camera.lookAt(0, 2, 0);
  const controls = createOrbitControls(camera, canvas, new THREE.Vector3(0, 1.7, 0), {
    minDistance: 5,
    maxDistance: 28,
    enablePan: true,
  });
  addStudioLights(scene);

  const ground = new THREE.Mesh(
    new THREE.CircleGeometry(30, 64),
    new THREE.MeshStandardMaterial({ color: 0x4d9f63, roughness: 0.96, metalness: 0.02 })
  );
  ground.rotation.x = -Math.PI / 2;
  ground.receiveShadow = true;
  scene.add(ground);

  const rings = new THREE.Group();
  for (let radius = 4; radius <= 20; radius += 4) {
    const points = [];
    for (let i = 0; i < 48; i += 1) {
      const theta = (i / 48) * Math.PI * 2;
      points.push(new THREE.Vector3(Math.cos(theta) * radius, 0.02, Math.sin(theta) * radius));
    }
    rings.add(
      new THREE.LineLoop(
        new THREE.BufferGeometry().setFromPoints(points),
        new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.12 })
      )
    );
  }
  scene.add(rings);

  const skyline = new THREE.Group();
  for (let i = 0; i < 8; i += 1) {
    const height = 2.2 + i * 0.35;
    const tower = new THREE.Mesh(
      new THREE.BoxGeometry(1 + (i % 2) * 0.25, height, 1),
      new THREE.MeshStandardMaterial({ color: 0xa3b6cb, transparent: true, opacity: 0.44 })
    );
    tower.position.set(-8 + i * 2, height / 2, -7 - (i % 3));
    skyline.add(tower);
  }
  scene.add(skyline);

  const guideGrid = new THREE.GridHelper(26, 26, 0x89c2ff, 0x284664);
  guideGrid.position.y = 0.02;
  guideGrid.material.transparent = true;
  guideGrid.material.opacity = 0.28;
  scene.add(guideGrid);

  const state = {
    mode: "idle",
    startTime: 0,
    caughtAt: 0,
    motionScale: 0.22,
    baseHeight: 4.8,
    sceneTitle: "Concept Space",
    sceneScenario: "Ask for a concept and the real-life scene will appear here.",
    sceneHint: "Drag with your mouse to rotate and inspect the scene from every side.",
    velocity: 18,
    angle: 42,
    launcherHeight: 8,
    environment: "rooftop",
    characters: {
      thrower: { name: "Sky Runner", palette: "sunrise" },
      catcher: { name: "Coach Nova", palette: "teal" },
    },
    objects: {},
  };

  const genericNodes = new THREE.Group();
  const idlePalette = [0xff8fab, 0x7dd3fc, 0xfecf6a, 0x86efac, 0xc4b5fd, 0xf9a8d4];
  const idleBallMeta = [];
  [
    { x: -2.8, y: 1.2, z: -0.35, r: 0.38, c: idlePalette[0] },
    { x: -1.25, y: 2.15, z: 0.42, r: 0.28, c: idlePalette[1] },
    { x: 0, y: 1.45, z: -0.18, r: 0.46, c: idlePalette[2] },
    { x: 1.35, y: 2.45, z: 0.18, r: 0.31, c: idlePalette[3] },
    { x: 2.9, y: 1.3, z: -0.28, r: 0.36, c: idlePalette[4] },
    { x: 0.85, y: 0.88, z: 0.48, r: 0.24, c: idlePalette[5] },
  ].forEach((item, index) => {
    const node = new THREE.Mesh(
      new THREE.SphereGeometry(item.r, 28, 28),
      new THREE.MeshStandardMaterial({
        color: item.c,
        roughness: 0.24,
        metalness: 0.1,
        emissive: item.c,
        emissiveIntensity: 0.16,
      })
    );
    node.position.set(item.x, item.y, item.z);
    genericNodes.add(node);
    idleBallMeta.push({
      baseX: item.x,
      baseY: item.y,
      baseZ: item.z,
      phase: index * 0.8,
      amplitude: 0.16 + (index % 3) * 0.04,
    });
  });

  const idleCore = new THREE.Mesh(
    new THREE.SphereGeometry(0.95, 40, 40),
    new THREE.MeshStandardMaterial({
      color: 0x2d7dff,
      emissive: 0x5fb3ff,
      emissiveIntensity: 0.42,
      roughness: 0.18,
      metalness: 0.12,
    })
  );
  idleCore.position.set(0, 1.55, 0);
  genericNodes.add(idleCore);

  const idleRing = new THREE.Mesh(
    new THREE.TorusGeometry(3.4, 0.05, 18, 120),
    new THREE.MeshBasicMaterial({ color: 0x7dd3fc, transparent: true, opacity: 0.26 })
  );
  idleRing.rotation.x = Math.PI / 2.2;
  idleRing.position.y = 1.55;
  genericNodes.add(idleRing);

  const idleLabel = createLabelSprite("3D Concept Space", "#fff6cf");
  idleLabel.position.set(0, 4.2, 0);
  idleLabel.scale.set(3.2, 0.92, 1);
  genericNodes.add(idleLabel);

  const idleScenario = createLabelSprite("Ask for a real-life scenario and rotate it with your mouse.", "#dbeafe");
  idleScenario.position.set(0, 3.15, 0);
  idleScenario.scale.set(3.5, 0.84, 1);
  genericNodes.add(idleScenario);

  const idleHint = createLabelSprite("Drag to inspect from every angle", "#ccfbf1");
  idleHint.position.set(0, 0.42, -3.2);
  idleHint.scale.set(2.8, 0.72, 1);
  genericNodes.add(idleHint);
  scene.add(genericNodes);

  function computeLanding() {
    const radians = THREE.MathUtils.degToRad(state.angle);
    const vx = state.velocity * Math.cos(radians);
    const vy = state.velocity * Math.sin(radians);
    const flightTime = (vy + Math.sqrt(vy * vy + 2 * 9.8 * state.launcherHeight)) / 9.8;
    return {
      time: flightTime,
      x: vx * flightTime,
    };
  }

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

  function buildProjectileScene() {
    clearDynamicScene();
    const palette = getEnvironmentPalette(state.environment);
    scene.background = new THREE.Color(palette.background);
    scene.fog = new THREE.Fog(palette.fog, 18, 40);
    ground.material.color.setHex(palette.ground);

    const landing = computeLanding();
    const displayScale = Math.max(0.16, Math.min(0.3, 7.5 / Math.max(landing.x || 1, 1)));
    const baseHeight = Math.max(4.4, state.launcherHeight * displayScale * 0.9 + 2.8);
    state.motionScale = displayScale;
    state.baseHeight = baseHeight;
    const projectileGroup = new THREE.Group();
    scene.add(projectileGroup);

    const building = new THREE.Mesh(
      new THREE.BoxGeometry(3.6, baseHeight + 0.9, 3.4),
      new THREE.MeshStandardMaterial({
        color: palette.platform,
        roughness: 0.82,
        metalness: 0.08,
        emissive: palette.platform,
        emissiveIntensity: state.environment === "lab" ? 0.13 : 0.04,
      })
    );
    building.position.set(0, (baseHeight + 0.9) / 2, 0);
    building.castShadow = true;
    building.receiveShadow = true;
    projectileGroup.add(building);

    const roof = new THREE.Mesh(
      new THREE.BoxGeometry(4.1, 0.18, 3.9),
      new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.7 })
    );
    roof.position.set(0, baseHeight + 0.48, 0);
    projectileGroup.add(roof);

    const title = createLabelSprite(state.sceneTitle || "Projectile Motion", "#fff7cc");
    title.position.set(0, baseHeight + 3.2, 0);
    const story = createLabelSprite(state.sceneScenario || "A ball thrown from a roof to a catcher below.", "#dbeafe");
    story.position.set(0, baseHeight + 2.38, 0);
    story.scale.set(3.2, 0.84, 1);
    const hint = createLabelSprite(state.sceneHint || "Drag with mouse to rotate and inspect the full flight path.", "#ccfbf1");
    hint.position.set(-2.55, baseHeight + 0.2, 2.2);
    hint.scale.set(2.45, 0.68, 1);
    projectileGroup.add(title, story, hint);

    const thrower = createCharacter(state.characters.thrower.name, state.characters.thrower.palette);
    thrower.position.set(-1.05, baseHeight + 0.62, 0);
    thrower.rotation.y = Math.PI * 0.12;
    projectileGroup.add(thrower);

    const catcher = createCharacter(state.characters.catcher.name, state.characters.catcher.palette);
    projectileGroup.add(catcher);

    const ball = new THREE.Mesh(
      new THREE.SphereGeometry(0.18, 22, 22),
      new THREE.MeshStandardMaterial({
        color: palette.accent,
        emissive: palette.accent,
        emissiveIntensity: 0.18,
        roughness: 0.35,
      })
    );
    projectileGroup.add(ball);

    const targetMarker = new THREE.Mesh(
      new THREE.TorusGeometry(0.52, 0.05, 16, 64),
      new THREE.MeshStandardMaterial({ color: 0xffffff, emissive: 0xffffff, emissiveIntensity: 0.1 })
    );
    targetMarker.rotation.x = Math.PI / 2;
    projectileGroup.add(targetMarker);

    const points = [];
    const radians = THREE.MathUtils.degToRad(state.angle);
    for (let t = 0; t <= landing.time; t += 0.05) {
      const x = state.velocity * Math.cos(radians) * t * displayScale;
      const y = baseHeight + state.velocity * Math.sin(radians) * t * displayScale - 4.9 * t * t * displayScale;
      points.push(new THREE.Vector3(x, y, 0));
    }

    const trajectoryLine = new THREE.Line(
      new THREE.BufferGeometry().setFromPoints(points),
      new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 })
    );
    projectileGroup.add(trajectoryLine);

    const trail = [];
    points.filter((_, index) => index % 5 === 0).forEach((point) => {
      const glow = new THREE.Mesh(
        new THREE.SphereGeometry(0.05, 10, 10),
        new THREE.MeshBasicMaterial({ color: 0xfff1b3, transparent: true, opacity: 0.4 })
      );
      glow.position.copy(point);
      trail.push(glow);
      projectileGroup.add(glow);
    });

    catcher.position.set(landing.x * displayScale, 0, 0);
    targetMarker.position.set(landing.x * displayScale, 0.08, 0);
    ball.position.set(-0.5, baseHeight + 1.05, 0);
    camera.position.set(10.5, Math.max(5.8, baseHeight * 0.95), 12.5);
    controls.target.set(landing.x * displayScale * 0.45, Math.max(1.8, baseHeight * 0.55), 0);
    controls.update();
    state.startTime = 0;
    state.caughtAt = 0;
    state.objects = { projectileGroup, building, roof, thrower, catcher, ball, targetMarker, trajectoryLine, trail, title, story, hint };
  }

  function buildProbabilityScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x0e2038);
    scene.fog = new THREE.Fog(0x132944, 16, 34);
    ground.material.color.setHex(0x27364d);
    camera.position.set(7, 4.8, 8.5);
    camera.lookAt(0, 1.8, 0);
    controls.target.set(0, 1.8, 0);
    controls.update();

    const bag = new THREE.Mesh(
      new THREE.CylinderGeometry(1.2, 0.95, 2.2, 28, 1, true),
      new THREE.MeshPhysicalMaterial({
        color: 0xc7d2fe,
        transparent: true,
        opacity: 0.2,
        roughness: 0.08,
        transmission: 0.88,
      })
    );
    bag.position.y = 1.5;
    scene.add(bag);

    const base = new THREE.Mesh(
      new THREE.CylinderGeometry(1.08, 1.08, 0.18, 28),
      new THREE.MeshStandardMaterial({ color: 0x21314f, roughness: 0.85 })
    );
    base.position.y = 0.45;
    scene.add(base);

    const colors = [0xef4444, 0x2563eb, 0x16a34a, 0xf59e0b, 0xa855f7];
    const balls = [];
    for (let i = 0; i < 9; i += 1) {
      const ball = new THREE.Mesh(
        new THREE.SphereGeometry(0.24, 20, 20),
        new THREE.MeshStandardMaterial({ color: colors[i % colors.length], roughness: 0.35, metalness: 0.08 })
      );
      ball.position.set(-0.55 + (i % 3) * 0.55, 0.88 + Math.floor(i / 3) * 0.38, -0.2 + (i % 2) * 0.22);
      balls.push(ball);
      scene.add(ball);
    }

    const selectedBall = balls[0];
    const title = createLabelSprite(state.sceneTitle || "Probability Scene", "#fff7cc");
    title.position.set(0, 3.55, 0);
    const story = createLabelSprite(state.sceneScenario || "Picking one outcome from a bag of outcomes.", "#dbeafe");
    story.position.set(0, 2.7, 0);
    story.scale.set(3.0, 0.84, 1);
    const hint = createLabelSprite(state.sceneHint || "Rotate to inspect every angle and each outcome.", "#ccfbf1");
    hint.position.set(0, 0.32, 2.45);
    hint.scale.set(2.5, 0.68, 1);
    const label = createLabelSprite("Favorable / Total", "#fff7cc");
    label.position.set(0, 3.2, 0);
    scene.add(title, story, hint, label);
    state.objects = { bag, base, balls, selectedBall, title, story, hint, label };
  }

  function buildShopScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x12243c);
    scene.fog = new THREE.Fog(0x1b3150, 16, 34);
    ground.material.color.setHex(0x314155);
    camera.position.set(8, 5, 8.5);
    camera.lookAt(0, 2.1, 0);
    controls.target.set(0, 2.1, 0);
    controls.update();

    const shelf = new THREE.Mesh(
      new THREE.BoxGeometry(5.5, 0.2, 1.6),
      new THREE.MeshStandardMaterial({ color: 0x6b4f3a, roughness: 0.86 })
    );
    shelf.position.y = 1.25;
    scene.add(shelf);

    const bars = [];
    const heights = [1.1, 1.7, 1.35];
    const colors = [0x38bdf8, 0xf97316, 0xfacc15];
    heights.forEach((height, index) => {
      const bar = new THREE.Mesh(
        new THREE.BoxGeometry(0.9, height, 0.9),
        new THREE.MeshStandardMaterial({ color: colors[index], roughness: 0.4 })
      );
      bar.position.set(-1.8 + index * 1.8, 0.55 + height / 2, 0);
      bars.push(bar);
      scene.add(bar);
    });

    const tag = createLabelSprite("CP -> Discount -> SP", "#e0f2fe");
    tag.position.set(0, 3.3, 0);
    const title = createLabelSprite(state.sceneTitle || "Percentages Scene", "#fff7cc");
    title.position.set(0, 4.0, 0);
    const story = createLabelSprite(state.sceneScenario || "A shop price changes with discount and profit", "#dbeafe");
    story.position.set(0, 3.15, 0);
    story.scale.set(3.2, 0.84, 1);
    const hint = createLabelSprite(state.sceneHint || "Rotate to inspect the price flow from every side.", "#ccfbf1");
    hint.position.set(0, 0.36, 2.35);
    hint.scale.set(2.55, 0.68, 1);
    scene.add(title, story, hint, tag);
    state.objects = { shelf, bars, title, story, hint, tag };
  }

  function buildFieldScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x0c1424);
    scene.fog = new THREE.Fog(0x12203a, 20, 38);
    ground.material.color.setHex(0x1a2638);
    camera.position.set(7.5, 5, 9);
    camera.lookAt(0, 1.8, 0);
    controls.target.set(0, 1.8, 0);
    controls.update();

    const positive = new THREE.Mesh(
      new THREE.SphereGeometry(0.52, 28, 28),
      new THREE.MeshStandardMaterial({ color: 0xfb7185, emissive: 0xfb7185, emissiveIntensity: 0.18 })
    );
    positive.position.set(-1.8, 1.6, 0);
    scene.add(positive);

    const negative = new THREE.Mesh(
      new THREE.SphereGeometry(0.52, 28, 28),
      new THREE.MeshStandardMaterial({ color: 0x60a5fa, emissive: 0x60a5fa, emissiveIntensity: 0.18 })
    );
    negative.position.set(1.8, 1.6, 0);
    scene.add(negative);

    const lines = [];
    for (let i = -2; i <= 2; i += 1) {
      const points = [];
      for (let step = 0; step <= 20; step += 1) {
        const x = -1.8 + (step / 20) * 3.6;
        const y = 1.6 + Math.sin((step / 20) * Math.PI) * (1.2 + Math.abs(i) * 0.25) + i * 0.12;
        const z = i * 0.28;
        points.push(new THREE.Vector3(x, y, z));
      }
      const line = new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(points),
        new THREE.LineBasicMaterial({ color: 0xf8fafc, transparent: true, opacity: 0.7 })
      );
      lines.push(line);
      scene.add(line);
    }

    const probe = new THREE.Mesh(
      new THREE.SphereGeometry(0.14, 18, 18),
      new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0xfacc15, emissiveIntensity: 0.22 })
    );
    probe.position.set(0, 3.15, 0);
    scene.add(probe);

    const tag = createLabelSprite("Field Strength Changes With Distance", "#dbeafe");
    tag.position.set(0, 4.1, 0);
    const title = createLabelSprite(state.sceneTitle || "Field Visualization", "#fff7cc");
    title.position.set(0, 4.55, 0);
    const story = createLabelSprite(state.sceneScenario || "Charges create influence across space.", "#dbeafe");
    story.position.set(0, 3.65, 0);
    story.scale.set(3.1, 0.84, 1);
    const hint = createLabelSprite(state.sceneHint || "Drag to inspect the field from every side.", "#ccfbf1");
    hint.position.set(0, 0.34, 2.65);
    hint.scale.set(2.55, 0.68, 1);
    scene.add(title, story, hint, tag);
    state.objects = { positive, negative, lines, probe, title, story, hint, tag };
  }

  function buildConceptFlowScene() {
    clearDynamicScene();
    scene.background = new THREE.Color(0x0e2034);
    scene.fog = new THREE.Fog(0x122840, 16, 34);
    ground.material.color.setHex(0x23364a);
    camera.position.set(8, 4.5, 8.5);
    camera.lookAt(0, 1.6, 0);
    controls.target.set(0, 1.6, 0);
    controls.update();

    const nodes = [];
    const positions = [
      [-2.8, 1.1, 0],
      [0, 2.2, 0],
      [2.8, 1.1, 0],
    ];
    const colors = [0x22c55e, 0x38bdf8, 0xf59e0b];
    positions.forEach(([x, y, z], index) => {
      const node = new THREE.Mesh(
        new THREE.BoxGeometry(1.1, 1.1, 1.1),
        new THREE.MeshStandardMaterial({ color: colors[index], roughness: 0.3, metalness: 0.08 })
      );
      node.position.set(x, y, z);
      nodes.push(node);
      scene.add(node);
    });

    const connectors = [];
    [[positions[0], positions[1]], [positions[1], positions[2]]].forEach(([from, to]) => {
      const points = [new THREE.Vector3(...from), new THREE.Vector3(...to)];
      const line = new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(points),
        new THREE.LineBasicMaterial({ color: 0xe2e8f0, transparent: true, opacity: 0.7 })
      );
      connectors.push(line);
      scene.add(line);
    });

    const tag = createLabelSprite("Cause -> Change -> Result", "#dcfce7");
    tag.position.set(0, 3.8, 0);
    const title = createLabelSprite(state.sceneTitle || "Concept Bridge", "#fff7cc");
    title.position.set(0, 4.35, 0);
    const story = createLabelSprite(state.sceneScenario || "A concept becomes easier when shown as cause and effect.", "#dbeafe");
    story.position.set(0, 3.5, 0);
    story.scale.set(3.35, 0.84, 1);
    const hint = createLabelSprite(state.sceneHint || "Rotate to connect the pieces.", "#ccfbf1");
    hint.position.set(0, 0.34, 2.65);
    hint.scale.set(2.55, 0.68, 1);
    scene.add(title, story, hint, tag);
    state.objects = { nodes, connectors, title, story, hint, tag };
  }

  function updateVisual(visual) {
    const animation = visual && visual.animation ? visual.animation : null;
    if (!animation) {
      state.mode = "idle";
      clearDynamicScene();
      scene.background = new THREE.Color(0x0a1a33);
      scene.fog = null;
      ground.material.color.setHex(0x1f3558);
      camera.position.set(7.8, 4.9, 8.8);
      camera.lookAt(0, 1.8, 0);
      controls.target.set(0, 1.8, 0);
      controls.update();
      genericNodes.visible = true;
      return;
    }

    genericNodes.visible = false;
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

    if (animation.type === "probability_bag") {
      state.mode = "probability_bag";
      state.sceneTitle = visual.title || "Probability Scene";
      state.sceneScenario = visual.scenario || "A bag of mixed balls shows favorable versus total outcomes.";
      state.sceneHint = config.interaction_hint || "Rotate to inspect every angle and each outcome.";
      buildProbabilityScene();
      return;
    }

    if (animation.type === "shop_percentages") {
      state.mode = "shop_percentages";
      state.sceneTitle = visual.title || "Percentages Scene";
      state.sceneScenario = visual.scenario || "A shop price changes as discount and profit are applied.";
      state.sceneHint = config.interaction_hint || "Rotate to inspect the price flow from every side.";
      buildShopScene();
      return;
    }

    if (animation.type === "field_lines") {
      state.mode = "field_lines";
      state.sceneTitle = visual.title || "Field Visualization";
      state.sceneScenario = visual.scenario || "Charges shape the field around them in space.";
      state.sceneHint = config.interaction_hint || "Drag to inspect the field from every side.";
      buildFieldScene();
      return;
    }

    state.mode = "concept_flow";
    state.sceneTitle = visual.title || "Concept Bridge";
    state.sceneScenario = visual.scenario || "Track the concept as a cause, rule, and effect story.";
    state.sceneHint = config.interaction_hint || "Rotate to connect the pieces.";
    buildConceptFlowScene();
  }

  function animate(time) {
    resizeRenderer(renderer, camera, canvas);
    const t = time * 0.001;

    if (state.mode === "projectile" && state.objects.ball && state.objects.thrower && state.objects.catcher) {
      if (!state.startTime) {
        state.startTime = time;
      }
      const elapsed = (time - state.startTime) / 1000;
      const landing = computeLanding();
      const radians = THREE.MathUtils.degToRad(state.angle);
      const vx = state.velocity * Math.cos(radians);
      const vy = state.velocity * Math.sin(radians);

      state.objects.thrower.userData.armL.rotation.z = 0.48 + Math.sin(time * 0.004) * 0.08;
      state.objects.thrower.userData.armR.rotation.z = -0.82;

      if (!state.caughtAt) {
        const x = vx * elapsed * (state.motionScale || 0.22);
        const y = (state.baseHeight || 4.8) + vy * elapsed * (state.motionScale || 0.22) - 4.9 * elapsed * elapsed * (state.motionScale || 0.22);
        state.objects.ball.position.set(x, y, 0);
        state.objects.catcher.userData.armL.rotation.z = -0.12;
        state.objects.catcher.userData.armR.rotation.z = 0.12;
        if (elapsed >= landing.time) {
          state.caughtAt = time;
        }
      } else {
        state.objects.ball.position.set(landing.x * (state.motionScale || 0.22), 1.1, 0);
        state.objects.catcher.userData.armL.rotation.z = -1.1;
        state.objects.catcher.userData.armR.rotation.z = 1.1;
        if (time - state.caughtAt > 1200) {
          state.startTime = time;
          state.caughtAt = 0;
        }
      }

      state.objects.targetMarker.rotation.z += 0.014;
    } else if (state.mode === "probability_bag" && state.objects.balls) {
      state.objects.balls.forEach((ball, index) => {
        ball.position.y += Math.sin(t * 1.5 + index) * 0.0022;
      });
      if (state.objects.selectedBall) {
        state.objects.selectedBall.position.y = 1.85 + Math.sin(t * 2.2) * 0.28;
        state.objects.selectedBall.position.x = Math.sin(t * 0.9) * 0.12;
      }
    } else if (state.mode === "shop_percentages" && state.objects.bars) {
      state.objects.bars.forEach((bar, index) => {
        const scale = 0.9 + Math.sin(t * 1.6 + index) * 0.12;
        bar.scale.y = Math.max(0.75, scale);
      });
    } else if (state.mode === "field_lines" && state.objects.lines) {
      state.objects.positive.position.y = 1.6 + Math.sin(t * 1.3) * 0.1;
      state.objects.negative.position.y = 1.6 + Math.cos(t * 1.3) * 0.1;
      state.objects.probe.position.x = Math.sin(t * 1.2) * 2.1;
      state.objects.probe.position.y = 2.9 + Math.sin(t * 2) * 0.22;
      state.objects.lines.forEach((line, index) => {
        line.material.opacity = 0.4 + (Math.sin(t * 1.8 + index) + 1) * 0.2;
      });
    } else if (state.mode === "concept_flow" && state.objects.nodes) {
      state.objects.nodes.forEach((node, index) => {
        node.rotation.x += 0.01;
        node.rotation.y += 0.012;
        node.position.y = [1.1, 2.2, 1.1][index] + Math.sin(t * 1.6 + index) * 0.14;
      });
    } else {
      genericNodes.rotation.y = t * 0.16;
      genericNodes.children.forEach((node, index) => {
        if (idleBallMeta[index]) {
          const meta = idleBallMeta[index];
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

  updateVisual(null);
  requestAnimationFrame(animate);
  return {
    updateVisual,
    refresh() {
      resizeRenderer(renderer, camera, canvas);
      controls.update();
      renderer.render(scene, camera);
    },
  };
}

const tutorCanvas = document.getElementById("threeTutorCanvas");
const conceptCanvas = document.getElementById("threeConceptCanvas");

let tutorStage = null;
let conceptStage = null;

try {
  tutorStage = createTutorStage(tutorCanvas);
} catch (error) {
  console.error("3D tutor stage failed to initialize:", error);
  drawCanvasFallback(
    tutorCanvas,
    "3D Tutor Stage",
    "The tutor scene could not initialize yet. Refresh once more after the page fully loads.",
    "#f9a8d4"
  );
}

try {
  conceptStage = createConceptStage(conceptCanvas);
} catch (error) {
  console.error("3D concept stage failed to initialize:", error);
  drawCanvasFallback(
    conceptCanvas,
    "3D Concept Stage",
    "The concept scene could not initialize yet. Refresh once more after the page fully loads.",
    "#facc15"
  );
}

window.addEventListener("alt:tutor-appearance", (event) => {
  if (tutorStage) {
    tutorStage.updateAppearance(event.detail || null);
  }
});

window.addEventListener("alt:concept-visual", (event) => {
  if (conceptStage) {
    conceptStage.updateVisual(event.detail || null);
  }
});

window.addEventListener("alt:studio-pane-changed", (event) => {
  const paneId = event && event.detail ? event.detail.paneId : "";
  window.setTimeout(() => {
    if (paneId === "threeConceptPanel" && conceptStage) {
      conceptStage.refresh();
    }
    if (paneId === "threeTutorPanel" && tutorStage) {
      tutorStage.refresh();
    }
  }, 60);
});

window.addEventListener("resize", () => {
  if (tutorStage) {
    tutorStage.refresh();
  }
  if (conceptStage) {
    conceptStage.refresh();
  }
});

window.setTimeout(() => {
  if (conceptStage) {
    conceptStage.refresh();
  }
  if (tutorStage) {
    tutorStage.refresh();
  }
}, 120);
