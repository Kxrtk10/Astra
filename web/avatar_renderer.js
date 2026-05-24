class AvatarRenderer {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.scene = null;
    this.camera = null;
    this.renderer = null;
    this.avatar = null;
    this.mixer = null;
    this.morphTargets = {};
    this.isSpeaking = false;
    this.usingFallback = false;
    this.fallbackImage = null;
    this.headMesh = null;
    this.clock = new THREE.Clock();
    this._frameCount = 0;
    this._fpsWindowStart = performance.now();
    this._qualityReduced = false;
  }

  async init() {
    if (!this.canvas) {
      throw new Error("Avatar canvas not found.");
    }
    if (!window.THREE) {
      throw new Error("Three.js is unavailable.");
    }
    if (this.renderer) {
      return this;
    }

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x0d1117);

    this.camera = new THREE.PerspectiveCamera(
      35,
      (this.canvas.clientWidth || this.canvas.width || 400) / Math.max(this.canvas.clientHeight || this.canvas.height || 500, 1),
      0.1,
      100
    );
    this.camera.position.set(0, 1.6, 2.2);
    this.camera.lookAt(0, 1.45, 0);

    this.renderer = new THREE.WebGLRenderer({
      canvas: this.canvas,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance",
    });
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
    this.renderer.setSize(this.canvas.clientWidth || this.canvas.width || 400, this.canvas.clientHeight || this.canvas.height || 500, false);
    this.renderer.shadowMap.enabled = true;
    if ("outputEncoding" in this.renderer && THREE.sRGBEncoding) {
      this.renderer.outputEncoding = THREE.sRGBEncoding;
    }

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.65);
    const keyLight = new THREE.DirectionalLight(0xffffff, 0.95);
    keyLight.position.set(1, 2, 2);
    const fillLight = new THREE.DirectionalLight(0x8899ff, 0.28);
    fillLight.position.set(-1, 1, 1);

    this.scene.add(ambientLight, keyLight, fillLight);
    this.animate();
    return this;
  }

  _removeFallback2D() {
    const existing = this.canvas?.parentElement?.querySelector("#avatar-fallback-img");
    if (existing) {
      existing.remove();
    }
    if (this.canvas) {
      this.canvas.style.display = "block";
    }
    this.usingFallback = false;
    this.fallbackImage = null;
  }

  _clearAvatar() {
    if (this.avatar && this.scene) {
      this.scene.remove(this.avatar);
    }
    this.avatar = null;
    this.headMesh = null;
    this.morphTargets = {};
    this.mixer = null;
  }

  async loadAvatar(glbUrl) {
    if (!this.scene) {
      await this.init();
    }
    if (!glbUrl) {
      throw new Error("Avatar GLB URL is missing.");
    }

    this._clearAvatar();
    this._removeFallback2D();

    const { GLTFLoader } = await import("https://cdn.jsdelivr.net/npm/three@0.128.0/examples/jsm/loaders/GLTFLoader.js");
    const loader = new GLTFLoader();

    return new Promise((resolve, reject) => {
      loader.load(
        glbUrl,
        (gltf) => {
          this.avatar = gltf.scene;
          this.avatar.position.set(0, 0, 0);
          this.avatar.scale.set(1, 1, 1);
          this.avatar.traverse((node) => {
            if (node.isMesh && node.morphTargetDictionary) {
              this.headMesh = node;
              this.morphTargets = node.morphTargetDictionary || {};
            }
          });
          if (gltf.animations && gltf.animations.length > 0) {
            this.mixer = new THREE.AnimationMixer(this.avatar);
          }
          this.scene.add(this.avatar);
          resolve(this.avatar);
        },
        undefined,
        (error) => {
          reject(error || new Error("Could not load avatar GLB."));
        }
      );
    });
  }

  useFallback2D(imageUrl) {
    if (!this.canvas || !this.canvas.parentElement) {
      return;
    }

    this._removeFallback2D();
    this.canvas.style.display = "none";

    const img = document.createElement("img");
    img.src = imageUrl;
    img.className = "avatar-fallback-2d";
    img.id = "avatar-fallback-img";
    img.alt = "Tutor avatar fallback";
    this.canvas.parentElement.appendChild(img);
    this.fallbackImage = img;
    this.usingFallback = true;
  }

  setViseme(viseme, weight) {
    if (!this.headMesh || !this.morphTargets || !this.headMesh.morphTargetInfluences) {
      return;
    }

    const visemeMap = {
      sil: "mouthClose",
      PP: "viseme_PP",
      FF: "viseme_FF",
      TH: "viseme_TH",
      DD: "viseme_DD",
      kk: "viseme_kk",
      CH: "viseme_CH",
      SS: "viseme_SS",
      nn: "viseme_nn",
      RR: "viseme_RR",
      aa: "viseme_aa",
      E: "viseme_E",
      I: "viseme_I",
      O: "viseme_O",
      U: "viseme_U",
    };

    const morphName = visemeMap[viseme];
    if (!morphName) {
      return;
    }

    const morphIndex = this.morphTargets[morphName];
    if (morphIndex === undefined) {
      return;
    }

    this.headMesh.morphTargetInfluences[morphIndex] = weight;
  }

  startSpeakingAnimation() {
    this.isSpeaking = true;
    this.speakingStartTime = Date.now();
    if (this.usingFallback && this.fallbackImage) {
      this.fallbackImage.classList.add("speaking");
    }
  }

  stopSpeakingAnimation() {
    this.isSpeaking = false;
    if (this.usingFallback && this.fallbackImage) {
      this.fallbackImage.classList.remove("speaking");
    }
    this.setViseme("aa", 0);
    this.setViseme("O", 0);
    this.setViseme("I", 0);
  }

  addIdleMotion() {
    if (!this.avatar) {
      return;
    }
    const time = performance.now() * 0.001;
    this.avatar.rotation.y = Math.sin(time * 0.6) * 0.025;
    this.avatar.position.y = Math.sin(time * 1.2) * 0.01;
    if (this.headMesh) {
      this.headMesh.rotation.z = Math.sin(time * 0.45) * 0.02;
    }
  }

  updateSpeakingMouth() {
    if (!this.isSpeaking || !this.headMesh || this.usingFallback) {
      return;
    }

    const time = performance.now() * 0.001;
    const mouthOpen = Math.abs(Math.sin(time * 8)) * 0.6;
    const vowelCycle = Math.floor(time * 3) % 3;

    if (vowelCycle === 0) {
      this.setViseme("aa", mouthOpen);
      this.setViseme("O", 0);
      this.setViseme("I", 0);
    } else if (vowelCycle === 1) {
      this.setViseme("aa", 0);
      this.setViseme("O", mouthOpen * 0.7);
      this.setViseme("I", 0);
    } else {
      this.setViseme("aa", 0);
      this.setViseme("O", 0);
      this.setViseme("I", mouthOpen * 0.5);
    }
  }

  animate() {
    requestAnimationFrame(() => this.animate());

    if (!this.renderer || !this.scene || !this.camera) {
      return;
    }

    const deltaTime = this.clock.getDelta();
    if (this.mixer) {
      this.mixer.update(deltaTime);
    }

    this.addIdleMotion(deltaTime);
    this.updateSpeakingMouth(deltaTime);
    this.renderer.render(this.scene, this.camera);

    this._frameCount += 1;
    const now = performance.now();
    if (now - this._fpsWindowStart >= 2000) {
      const fps = (this._frameCount * 1000) / Math.max(now - this._fpsWindowStart, 1);
      if (fps < 30 && !this._qualityReduced) {
        this._qualityReduced = true;
        this.renderer.setPixelRatio(1);
        this.renderer.shadowMap.enabled = false;
      } else if (fps > 45 && this._qualityReduced) {
        this._qualityReduced = false;
        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
        this.renderer.shadowMap.enabled = true;
      }
      this._fpsWindowStart = now;
      this._frameCount = 0;
    }
  }

  playNodGesture() {
    if (this.usingFallback && this.fallbackImage) {
      if (typeof this.fallbackImage.animate === "function") {
        this.fallbackImage.animate(
          [
            { transform: "translateY(0px)" },
            { transform: "translateY(-2px)" },
            { transform: "translateY(0px)" },
          ],
          { duration: 450, easing: "ease-out" }
        );
      }
      return;
    }

    if (!this.avatar) {
      return;
    }

    let progress = 0;
    const nod = setInterval(() => {
      progress += 0.1;
      if (this.avatar) {
        this.avatar.rotation.x = Math.sin(progress * Math.PI) * 0.15;
      }
      if (progress >= 1) {
        clearInterval(nod);
        if (this.avatar) {
          this.avatar.rotation.x = 0;
        }
      }
    }, 30);
  }

  resize(width, height) {
    if (!this.camera || !this.renderer) {
      return;
    }
    this.camera.aspect = width / Math.max(height, 1);
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(width, height, false);
  }
}

window.AvatarRenderer = AvatarRenderer;
