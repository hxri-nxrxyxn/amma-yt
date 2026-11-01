<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "$lib/components/ui/card";
  import { Input } from "$lib/components/ui/input";
  import { Badge } from "$lib/components/ui/badge";
  import { Label } from "$lib/components/ui/label";
  import { Separator } from "$lib/components/ui/separator";
  import { Switch } from "$lib/components/ui/switch";
  import { Slider } from "$lib/components/ui/slider";

  import Download from "@lucide/svelte/icons/download";
  import Copy from "@lucide/svelte/icons/copy";
  import Video from "@lucide/svelte/icons/video";
  import Smartphone from "@lucide/svelte/icons/smartphone";
  import RefreshCw from "@lucide/svelte/icons/refresh-cw";
  import Check from "@lucide/svelte/icons/check";
  import BookOpen from "@lucide/svelte/icons/book-open";
  import Type from "@lucide/svelte/icons/type";
  import SlidersHorizontal from "@lucide/svelte/icons/sliders-horizontal";
  import Sparkles from "@lucide/svelte/icons/sparkles";
  import Key from "@lucide/svelte/icons/key";
  import ChevronDown from "@lucide/svelte/icons/chevron-down";
  import ChevronUp from "@lucide/svelte/icons/chevron-up";
  import Layers from "@lucide/svelte/icons/layers";
  import Palette from "@lucide/svelte/icons/palette";
  import { Filesystem, Directory } from "@capacitor/filesystem";
  import { Share } from "@capacitor/share";

  const CANVAS_WIDTH = 1280;
  const CANVAS_HEIGHT = 720;

  const API_BASE = typeof window !== "undefined" && ((window as any).Capacitor || window.location.protocol.startsWith("capacitor") || window.location.protocol === "file:") ? "http://100.117.215.112:8000" : "";

  // Complete Kerala SCERT / NCERT Syllabus Database
  interface Chapter {
    num: number;
    title: string;
    sub: string;
    malayalam: string;
    derivations: string[];
  }

  const PLUS_ONE_CHAPTERS: Chapter[] = [
    { num: 1, title: "UNITS & MEASUREMENTS", sub: "Dimensional Analysis & Errors", malayalam: "യൂണിറ്റുകളും അളവുകളും", derivations: ["Dimensional Analysis", "Error Analysis & Significant Figures"] },
    { num: 2, title: "MOTION IN A STRAIGHT LINE", sub: "Equations of Motion & Graphs", malayalam: "നേർരേഖാ ചലനം", derivations: ["Equations of Motion (v = u + at, s = ut + ½at²)", "Relative Velocity & Velocity-Time Graphs"] },
    { num: 3, title: "MOTION IN A PLANE", sub: "Projectile Motion & Vectors", malayalam: "ഒരു പ്രതലത്തിലെ ചലനം", derivations: ["Trajectory of Projectile & Max Height", "Horizontal Range & Centripetal Acceleration"] },
    { num: 4, title: "LAWS OF MOTION", sub: "Newton's Laws & Friction", malayalam: "ചലന നിയമങ്ങൾ", derivations: ["Banking of Roads (Friction & Angle)", "Conservation of Linear Momentum & Recoil"] },
    { num: 5, title: "WORK, ENERGY & POWER", sub: "Work-Energy Theorem & Collisions", malayalam: "പ്രവൃത്തി, ഊർജ്ജം, പവർ", derivations: ["Work-Energy Theorem Derivation", "Elastic Collision in One Dimension"] },
    { num: 6, title: "SYSTEM OF PARTICLES & ROTATION", sub: "Moment of Inertia & Torque", malayalam: "ഭ്രമണചലനവും കണികകളും", derivations: ["Parallel & Perpendicular Axes Theorems", "Torque = Iα & Angular Momentum Conservation"] },
    { num: 7, title: "GRAVITATION", sub: "Kepler's Laws & Escape Speed", malayalam: "ഗുരുത്വാകർഷണം", derivations: ["Acceleration due to Gravity at Height & Depth", "Escape Speed & Orbital Velocity Derivations"] },
    { num: 8, title: "MECHANICAL PROPERTIES OF SOLIDS", sub: "Hooke's Law & Stress-Strain", malayalam: "ഖരവസ്തുക്കളുടെ ഗുണങ്ങൾ", derivations: ["Stress-Strain Curve & Young's Modulus", "Elastic Potential Energy in a Stretched Wire"] },
    { num: 9, title: "MECHANICAL PROPERTIES OF FLUIDS", sub: "Bernoulli's Theorem & Viscosity", malayalam: "ദ്രാവകങ്ങളുടെ ഗുണങ്ങൾ", derivations: ["Bernoulli's Principle & Applications", "Terminal Velocity (Stokes' Law) & Surface Tension"] },
    { num: 10, title: "THERMAL PROPERTIES OF MATTER", sub: "Calorimetry & Heat Transfer", malayalam: "ദ്രവ്യത്തിന്റെ താപഗുണങ്ങൾ", derivations: ["Newton's Law of Cooling", "Specific Heat Capacity & Thermal Conductivity"] },
    { num: 11, title: "THERMODYNAMICS", sub: "First Law & Heat Engines", malayalam: "തെർമോഡൈനാമിക്സ്", derivations: ["Mayer's Relation (Cp - Cv = R)", "Carnot Engine & Efficiency (η = 1 - T2/T1)"] },
    { num: 12, title: "KINETIC THEORY", sub: "Ideal Gas Laws & Equipartition", malayalam: "കൈനറ്റിക് തിയറി", derivations: ["Pressure Expression for Ideal Gas (P = ⅓ρv²)", "Degrees of Freedom & Law of Equipartition"] },
    { num: 13, title: "OSCILLATIONS", sub: "Simple Harmonic Motion (SHM)", malayalam: "ആന്ദോളനങ്ങൾ", derivations: ["Time Period of Simple Pendulum (T = 2π√(l/g))", "Kinetic & Potential Energy in SHM"] },
    { num: 14, title: "WAVES", sub: "Standing Waves & Beats", malayalam: "തരംഗങ്ങൾ", derivations: ["Modes of Vibration in Organ Pipes", "Beats Frequency & Doppler Effect"] }
  ];

  const PLUS_TWO_CHAPTERS: Chapter[] = [
    { num: 1, title: "ELECTRIC CHARGES & FIELDS", sub: "Gauss's Law & Dipole Field", malayalam: "വൈദ്യുത ചാർജ്ജുകളും മണ്ഡലങ്ങളും", derivations: ["Gauss's Law (Line, Plane Sheet, Shell)", "Electric Field due to Dipole (Axial & Equatorial)"] },
    { num: 2, title: "ELECTROSTATIC POTENTIAL & CAPACITANCE", sub: "Capacitors & Potential", malayalam: "പൊട്ടൻഷ്യലും കപ്പാസിറ്റൻസും", derivations: ["Parallel Plate Capacitor with Dielectric", "Energy Stored in Capacitor (U = ½CV²)"] },
    { num: 3, title: "CURRENT ELECTRICITY", sub: "Kirchhoff's Rules & Wheatstone Bridge", malayalam: "കറന്റ് ഇലക്ട്രിസിറ്റി", derivations: ["Drift Velocity & Ohm's Law Relation", "Wheatstone Bridge Principle (P/Q = R/S)"] },
    { num: 4, title: "MOVING CHARGES & MAGNETISM", sub: "Biot-Savart Law & Ampere's Law", malayalam: "ചലിക്കുന്ന ചാർജ്ജുകളും കാന്തികതയും", derivations: ["Magnetic Field on Axis of Circular Loop", "Ampere's Circuital Law & Solenoid / Toroid"] },
    { num: 5, title: "MAGNETISM & MATTER", sub: "Bar Magnet & Magnetic Materials", malayalam: "കാന്തികതയും പദാർത്ഥങ്ങളും", derivations: ["Magnetic Dipole Moment & Earth's Magnetism", "Dia, Para & Ferromagnetic Properties"] },
    { num: 6, title: "ELECTROMAGNETIC INDUCTION", sub: "Faraday's Law & Lenz's Law", malayalam: "വൈദ്യുതകാന്തിക പ്രേരണം", derivations: ["Motional EMF (e = Blv)", "Self & Mutual Inductance Derivations"] },
    { num: 7, title: "ALTERNATING CURRENT", sub: "LCR Series Circuit & Transformer", malayalam: "ആൾട്ടർനേറ്റിങ് കറന്റ്", derivations: ["LCR Series Resonance & Impedance (Z)", "Transformer Principle & Power Factor"] },
    { num: 8, title: "ELECTROMAGNETIC WAVES", sub: "Displacement Current & Spectrum", malayalam: "വൈദ്യുതകാന്തിക തരംഗങ്ങൾ", derivations: ["Displacement Current Concept", "Electromagnetic Spectrum Frequencies & Uses"] },
    { num: 9, title: "RAY OPTICS & INSTRUMENTS", sub: "Refraction, Prism & Lens Formula", malayalam: "കിരണ ഒപ്റ്റിക്സും ഉപകരണങ്ങളും", derivations: ["Lens Maker's Formula Derivation", "Refraction through Prism (Prism Formula)"] },
    { num: 10, title: "WAVE OPTICS", sub: "Huygens' Principle & Interference", malayalam: "തരംഗ ഒപ്റ്റിക്സ്", derivations: ["Young's Double Slit Fringe Width (β = λD/d)", "Huygens' Principle Laws of Reflection & Refraction"] },
    { num: 11, title: "DUAL NATURE OF RADIATION", sub: "Photoelectric Effect & de Broglie", malayalam: "വികിരണ-പദാർത്ഥ ഇരട്ടസ്വഭാവം", derivations: ["Einstein's Photoelectric Equation", "de Broglie Wavelength of Electron (λ = h/p)"] },
    { num: 12, title: "ATOMS", sub: "Bohr's Model & Energy Levels", malayalam: "ആറ്റങ്ങൾ", derivations: ["Radius of nth Bohr Orbit & Electron Energy", "Hydrogen Emission Spectrum (Lyman, Balmer)"] },
    { num: 13, title: "NUCLEI", sub: "Binding Energy & Nuclear Reactions", malayalam: "ന്യൂക്ലിയസ്സുകൾ", derivations: ["Mass Defect & Binding Energy per Nucleon", "Nuclear Fission & Fusion Energy"] },
    { num: 14, title: "SEMICONDUCTOR ELECTRONICS", sub: "PN Junction & Rectifiers", malayalam: "അർദ്ധചാലക ഇലക്ട്രോണിക്സ്", derivations: ["Half-Wave & Full-Wave Rectifier Circuits", "Energy Bands & V-I Characteristics"] }
  ];

  // App Reactive State (ALL TEXTS ARE FREE TEXT INPUTS)
  let ytUrl = $state("");
  let ytStatus = $state("");
  let isFetching = $state(false);
  let showApiKeyInput = $state(false);
  let geminiApiKey = $state(typeof window !== "undefined" ? localStorage.getItem("dhanya_gemini_key") || "" : "");

  // Text Inputs
  let selectedClass = $state("+1 PHYSICS");
  let chapterBadge = $state("CH 05");
  let selectedChapterNum = $state(5);
  let mainTitle = $state("WORK, ENERGY & POWER");
  let subtitle = $state("Work-Energy Theorem & Important Derivations");
  let partNumber = $state("PART 1");
  let tagBadge = $state("CORE DERIVATIONS");
  let channelName = $state("PHYSICS With Dhanya");
  let showChannel = $state(true);

  // Language & Title Cache
  let isMalayalamTitle = $state(false);
  let malayalamTitleCache = $state("പ്രവൃത്തി, ഊർജ്ജം, പവർ");
  let englishTitleCache = $state("WORK, ENERGY & POWER");

  // Typography & Sizing State (Supports Massive High-CTR Thumbnails!)
  let titleSize = $state(96);       // Range: 50 to 165
  let subtitleSize = $state(32);    // Range: 22 to 54
  let selectedFont = $state("inter");
  let layout = $state("editorial_left");
  let colorTheme = $state("mono_pure");
  let showWatermarkNum = $state(true);

  // Background Image & Contrast
  let bgImage: HTMLImageElement | null = $state(null);
  let bgDarknessPercent = $state(40);
  let bgDarkness = $derived(bgDarknessPercent / 100);

  // UI Controls & Feed Simulation
  let toastMessage = $state("");
  let showToast = $state(false);
  let canvasEl: HTMLCanvasElement | null = $state(null);
  let simThumbUrl = $state("");
  let showSeoSection = $state(false);
  let showChapterPresets = $state(false);

  // AI SEO State
  let isGeneratingSeo = $state(false);
  let seoData = $state<{
    title: string;
    description: string;
    tags_string: string;
    malayalam_summary: string;
    has_captions: boolean;
    captions_text: string;
  } | null>(null);

  let currentSyllabusList = $derived(selectedClass.includes("+2") ? PLUS_TWO_CHAPTERS : PLUS_ONE_CHAPTERS);
  let currentChapterObj = $derived(
    currentSyllabusList.find(c => c.num === selectedChapterNum) || currentSyllabusList[0]
  );

  function triggerToast(msg: string) {
    toastMessage = msg;
    showToast = true;
    setTimeout(() => {
      showToast = false;
    }, 2500);
  }

  function saveApiKey(key: string) {
    geminiApiKey = key.trim();
    if (typeof window !== "undefined") {
      if (geminiApiKey) {
        localStorage.setItem("dhanya_gemini_key", geminiApiKey);
        triggerToast("Saved Gemini API key!");
      } else {
        localStorage.removeItem("dhanya_gemini_key");
        triggerToast("Removed Gemini API key");
      }
    }
  }

  function selectChapterPreset(ch: Chapter) {
    selectedChapterNum = ch.num;
    chapterBadge = `CH ${ch.num < 10 ? '0' + ch.num : ch.num}`;
    englishTitleCache = ch.title;
    malayalamTitleCache = ch.malayalam;
    mainTitle = isMalayalamTitle ? ch.malayalam : ch.title;
    subtitle = ch.derivations[0] || ch.sub;
    showChapterPresets = false;
    triggerToast(`Loaded Ch ${ch.num}: ${ch.title}`);
  }

  function toggleLanguage() {
    isMalayalamTitle = !isMalayalamTitle;
    if (isMalayalamTitle) {
      englishTitleCache = mainTitle;
      mainTitle = malayalamTitleCache || currentChapterObj.malayalam || mainTitle;
      triggerToast("Switched to Malayalam (മലയാളം)");
    } else {
      malayalamTitleCache = mainTitle;
      mainTitle = englishTitleCache || currentChapterObj.title || mainTitle;
      triggerToast("Switched to English");
    }
  }

  function loadImage(src: string): Promise<boolean> {
    return new Promise((resolve) => {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        bgImage = img;
        renderCanvas();
        resolve(true);
      };
      img.onerror = () => {
        console.error("Failed to load image:", src);
        resolve(false);
      };
      img.src = src;
    });
  }

  async function fetchYouTubeThumbnail() {
    if (!ytUrl.trim()) return;
    isFetching = true;
    ytStatus = "Fetching & analyzing video details...";
    try {
      const keyParam = geminiApiKey.trim() ? `&api_key=${encodeURIComponent(geminiApiKey.trim())}` : "";
      const res = await fetch(`${API_BASE}/api/youtube-info?url=${encodeURIComponent(ytUrl.trim())}${keyParam}`);
      if (!res.ok) throw new Error("Video not found");
      const data = await res.json();
      
      let loaded = false;
      if (data.thumbnail_url) {
        const fullProxyUrl = data.thumbnail_url.startsWith("http")
          ? data.thumbnail_url
          : `${API_BASE}${data.thumbnail_url}`;
        loaded = await loadImage(fullProxyUrl);
      }

      // Fallback: If proxy image failed or was unreachable, fallback to direct YouTube CDN
      if (!loaded && data.raw_thumbnail_url) {
        loaded = await loadImage(data.raw_thumbnail_url);
      }

      // Auto-prefill text fields directly!
      if (data.detected_class) {
        selectedClass = data.detected_class;
      }
      if (data.detected_chapter) {
        chapterBadge = data.detected_chapter;
      }
      if (data.detected_chapter_num) {
        selectedChapterNum = data.detected_chapter_num;
      }
      if (data.detected_headline) {
        mainTitle = data.detected_headline;
        englishTitleCache = data.detected_headline;
      }
      if (data.detected_subtitle) {
        subtitle = data.detected_subtitle;
      }
      if (data.detected_part !== undefined) {
        partNumber = data.detected_part;
      }
      if (data.detected_tag) {
        tagBadge = data.detected_tag;
      }
      if (data.detected_malayalam) {
        malayalamTitleCache = data.detected_malayalam;
      }
      if (data.author) {
        channelName = data.author;
      }

      isMalayalamTitle = false;
      ytStatus = `Auto-filled from "${data.title}"`;
      triggerToast(data.ai_enhanced ? "✨ Gemini auto-filled thumbnail inputs!" : "Auto-filled thumbnail inputs!");
      renderCanvas();
    } catch (e) {
      console.error(e);
      ytStatus = "Could not fetch YouTube video. Please check URL.";
      triggerToast("Failed to fetch video details.");
    } finally {
      isFetching = false;
    }
  }

  async function generateSeoKit() {
    isGeneratingSeo = true;
    showSeoSection = true;
    triggerToast("Generating SEO kit with Gemini Flash...");
    try {
      const res = await fetch(`${API_BASE}/api/generate-seo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          video_id: ytUrl || "c-M2jbSHhTg",
          class_name: selectedClass,
          chapter_num: selectedChapterNum,
          chapter_title: mainTitle,
          focus_topic: subtitle,
          part: partNumber,
          malayalam_title: malayalamTitleCache || currentChapterObj.malayalam,
          api_key: geminiApiKey.trim() || undefined
        })
      });
      const data = await res.json();
      seoData = data;
      triggerToast("AI SEO kit ready!");
    } catch (e) {
      console.error(e);
      triggerToast("SEO generation failed. Please try again.");
    } finally {
      isGeneratingSeo = false;
    }
  }

  function copyText(text: string, label: string) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(() => {
        triggerToast(`Copied ${label} to clipboard!`);
      });
    }
  }

  /* =========================================================
     CANVAS ENGINE (MASSIVE HIGH-CTR BORDERLESS TYPOGRAPHY)
     ========================================================= */

  function getFont(size: number, weight = 900, forceInter = false) {
    if (isMalayalamTitle && !forceInter) {
      return `${weight} ${size}px "Noto Sans Malayalam", "LocalNotoMalayalam", sans-serif`;
    }
    if (selectedFont === "bebas" && !forceInter) {
      return `400 ${Math.round(size * 1.12)}px "Bebas Neue", "Inter", sans-serif`;
    }
    if (selectedFont === "jakarta" && !forceInter) {
      return `${weight} ${size}px "Plus Jakarta Sans", "Inter", sans-serif`;
    }
    return `${weight} ${size}px "Inter", "Inter Variable", sans-serif`;
  }

  function getThemeColors() {
    if (colorTheme === "mono_slate") {
      return {
        title: "#FFFFFF",
        sub: "#CBD5E1",
        eyebrowBg: "rgba(15, 23, 42, 0.85)",
        eyebrowText: "#F8FAFC",
        accentPillBg: "#F1F5F9",
        accentPillText: "#0F172A",
        cardBg: "rgba(15, 23, 42, 0.90)",
        gradientEnd: "#080d1a"
      };
    }
    if (colorTheme === "warm_editorial") {
      return {
        title: "#FDFBF7",
        sub: "#D6D3D1",
        eyebrowBg: "rgba(24, 24, 27, 0.88)",
        eyebrowText: "#FAFAF9",
        accentPillBg: "#F5F5F4",
        accentPillText: "#1C1917",
        cardBg: "rgba(24, 24, 27, 0.92)",
        gradientEnd: "#141210"
      };
    }
    if (colorTheme === "subtle_amber") {
      return {
        title: "#FFFFFF",
        sub: "#FDE68A",
        eyebrowBg: "rgba(0, 0, 0, 0.82)",
        eyebrowText: "#FFFFFF",
        accentPillBg: "#F59E0B",
        accentPillText: "#000000",
        cardBg: "rgba(9, 9, 11, 0.90)",
        gradientEnd: "#09090b"
      };
    }
    // Default: mono_pure
    return {
      title: "#FFFFFF",
      sub: "#E4E4E7",
      eyebrowBg: "rgba(0, 0, 0, 0.80)",
      eyebrowText: "#FFFFFF",
      accentPillBg: "#FFFFFF",
      accentPillText: "#09090B",
      cardBg: "rgba(9, 9, 11, 0.88)",
      gradientEnd: "#09090b"
    };
  }

  function roundRect(ctx: CanvasRenderingContext2D, x: number, y: number, width: number, height: number, radius: number) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  }

  function wrapText(ctx: CanvasRenderingContext2D, text: string, maxWidth: number, fontStr: string) {
    if (!text) return [];
    ctx.font = fontStr;
    const words = text.split(" ");
    const lines: string[] = [];
    let currentLine = words[0];

    for (let i = 1; i < words.length; i++) {
      const word = words[i];
      const width = ctx.measureText(currentLine + " " + word).width;
      if (width < maxWidth) {
        currentLine += " " + word;
      } else {
        lines.push(currentLine);
        currentLine = word;
      }
    }
    if (currentLine) lines.push(currentLine);
    return lines;
  }

  function drawEyebrowBadge(ctx: CanvasRenderingContext2D, x: number, y: number, text: string, bg: string, textColor: string) {
    ctx.save();
    const fontSize = 21;
    ctx.font = `800 ${fontSize}px "Inter", sans-serif`;
    const metrics = ctx.measureText(text);
    const padX = 16;
    const padY = 8;
    const w = metrics.width + (padX * 2);
    const h = fontSize + (padY * 2);
    const radius = 7;
    const topY = y - (h / 2);

    ctx.fillStyle = bg;
    roundRect(ctx, x, topY, w, h, radius);
    ctx.fill();

    ctx.fillStyle = textColor;
    ctx.textBaseline = "middle";
    ctx.fillText(text, x + padX, y);

    ctx.restore();
    return x + w;
  }

  function drawInvertedPill(ctx: CanvasRenderingContext2D, x: number, y: number, text: string, bg: string, textColor: string) {
    ctx.save();
    const fontSize = 21;
    ctx.font = `900 ${fontSize}px "Inter", sans-serif`;
    const metrics = ctx.measureText(text);
    const padX = 16;
    const padY = 8;
    const w = metrics.width + (padX * 2);
    const h = fontSize + (padY * 2);
    const radius = 7;
    const topY = y - (h / 2);

    ctx.shadowColor = "rgba(0, 0, 0, 0.4)";
    ctx.shadowBlur = 8;
    ctx.shadowOffsetY = 2;

    ctx.fillStyle = bg;
    roundRect(ctx, x, topY, w, h, radius);
    ctx.fill();

    ctx.shadowBlur = 0;
    ctx.shadowOffsetY = 0;
    ctx.fillStyle = textColor;
    ctx.textBaseline = "middle";
    ctx.fillText(text, x + padX, y);

    ctx.restore();
    return x + w;
  }

  function renderWatermarkNumeral(ctx: CanvasRenderingContext2D, posX: number, posY: number) {
    if (!showWatermarkNum) return;
    const match = (chapterBadge || "").match(/\d+/);
    const numVal = match ? parseInt(match[0], 10) : selectedChapterNum;
    if (!numVal) return;
    const numStr = numVal < 10 ? `0${numVal}` : `${numVal}`;
    ctx.save();
    ctx.font = `900 340px "Inter", "Bebas Neue", sans-serif`;
    ctx.fillStyle = "rgba(255, 255, 255, 0.08)";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(numStr, posX, posY);
    ctx.restore();
  }

  function renderChannelPill(ctx: CanvasRenderingContext2D) {
    ctx.save();
    const fontSize = 18;
    ctx.font = `800 ${fontSize}px "Inter", sans-serif`;
    const textWidth = ctx.measureText(channelName.toUpperCase()).width;
    const iconWidth = 28;
    const totalW = textWidth + iconWidth + 30;
    const totalH = 42;

    const posX = CANVAS_WIDTH - totalW - 36;
    const posY = CANVAS_HEIGHT - totalH - 28;

    ctx.fillStyle = "rgba(9, 9, 11, 0.85)";
    roundRect(ctx, posX, posY, totalW, totalH, 8);
    ctx.fill();

    const iconCenterX = posX + 18;
    const iconCenterY = posY + totalH / 2;
    
    ctx.strokeStyle = "rgba(255, 255, 255, 0.90)";
    ctx.lineWidth = 1.5;
    ctx.fillStyle = "#FFFFFF";
    ctx.beginPath();
    ctx.arc(iconCenterX, iconCenterY, 2.5, 0, Math.PI * 2);
    ctx.fill();

    ctx.beginPath();
    ctx.ellipse(iconCenterX, iconCenterY, 9, 3.5, 0, 0, Math.PI * 2);
    ctx.stroke();

    ctx.beginPath();
    ctx.ellipse(iconCenterX, iconCenterY, 9, 3.5, Math.PI / 3, 0, Math.PI * 2);
    ctx.stroke();

    ctx.beginPath();
    ctx.ellipse(iconCenterX, iconCenterY, 9, 3.5, -Math.PI / 3, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = "#FFFFFF";
    ctx.textBaseline = "middle";
    ctx.fillText(channelName.toUpperCase(), posX + 34, posY + totalH / 2);
    ctx.restore();
  }

  function renderEditorialLeft(ctx: CanvasRenderingContext2D) {
    const colors = getThemeColors();

    const panelGrad = ctx.createLinearGradient(0, 0, 960, 0);
    panelGrad.addColorStop(0, colors.gradientEnd);
    panelGrad.addColorStop(0.60, colors.gradientEnd);
    panelGrad.addColorStop(0.85, "rgba(9, 9, 11, 0.45)");
    panelGrad.addColorStop(1, "rgba(9, 9, 11, 0)");
    ctx.fillStyle = panelGrad;
    ctx.fillRect(0, 0, 980, CANVAS_HEIGHT);

    renderWatermarkNumeral(ctx, 420, 360);

    const startX = 72;
    const badgeY = titleSize > 115 ? 95 : 120;
    let badgeX = startX;

    if (selectedClass && selectedClass.trim()) {
      badgeX = drawInvertedPill(ctx, badgeX, badgeY, selectedClass.trim(), colors.accentPillBg, colors.accentPillText);
      badgeX += 12;
    }

    if (chapterBadge && chapterBadge.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, chapterBadge.trim(), colors.eyebrowBg, colors.eyebrowText);
      badgeX += 12;
    }

    if (partNumber && partNumber.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, partNumber.trim(), "rgba(255,255,255,0.18)", "#FFFFFF");
      badgeX += 12;
    }

    if (tagBadge && tagBadge.trim()) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge.trim(), "rgba(255,255,255,0.12)", "#FFFFFF");
    }

    const titleY = badgeY + 60;
    const fontStr = getFont(titleSize, 900);
    const maxWidth = 760;
    const lines = wrapText(ctx, mainTitle, maxWidth, fontStr);

    ctx.save();
    ctx.font = fontStr;
    ctx.textBaseline = "top";
    let currentY = titleY;
    const lineHeight = selectedFont === "bebas" ? titleSize * 1.02 : titleSize * 1.08;

    lines.forEach((line) => {
      ctx.shadowColor = "rgba(0, 0, 0, 0.98)";
      ctx.shadowBlur = 18;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 4;
      ctx.fillStyle = colors.title;
      ctx.fillText(line, startX, currentY);
      currentY += lineHeight;
    });
    ctx.restore();

    if (subtitle && subtitle.trim()) {
      ctx.save();
      const subSize = subtitleSize || Math.max(26, Math.floor(titleSize * 0.36));
      ctx.font = getFont(subSize, 700, true);
      ctx.textBaseline = "top";

      const subLines = wrapText(ctx, subtitle, maxWidth - 20, getFont(subSize, 700, true));
      let subY = currentY + 16;

      subLines.forEach((sLine) => {
        ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
        ctx.shadowBlur = 12;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 2;
        ctx.fillStyle = colors.sub;
        ctx.fillText(sLine, startX, subY);
        subY += subSize * 1.25;
      });
      ctx.restore();
    }
  }

  function renderHorizonBottom(ctx: CanvasRenderingContext2D) {
    const colors = getThemeColors();
    const bannerHeight = titleSize > 115 ? 380 : 340;
    const bannerY = CANVAS_HEIGHT - bannerHeight;

    const grad = ctx.createLinearGradient(0, bannerY - 60, 0, CANVAS_HEIGHT);
    grad.addColorStop(0, "rgba(9, 9, 11, 0)");
    grad.addColorStop(0.35, "rgba(9, 9, 11, 0.92)");
    grad.addColorStop(1, colors.gradientEnd);
    ctx.fillStyle = grad;
    ctx.fillRect(0, bannerY - 60, CANVAS_WIDTH, bannerHeight + 60);

    const startX = 72;
    const badgeY = bannerY + 45;
    let badgeX = startX;

    if (selectedClass && selectedClass.trim()) {
      badgeX = drawInvertedPill(ctx, badgeX, badgeY, selectedClass.trim(), colors.accentPillBg, colors.accentPillText);
      badgeX += 12;
    }
    if (chapterBadge && chapterBadge.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, chapterBadge.trim(), colors.eyebrowBg, colors.eyebrowText);
      badgeX += 12;
    }
    if (partNumber && partNumber.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, partNumber.trim(), "rgba(255,255,255,0.18)", "#FFFFFF");
      badgeX += 12;
    }
    if (tagBadge && tagBadge.trim()) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge.trim(), "rgba(255,255,255,0.12)", "#FFFFFF");
    }

    const titleY = badgeY + 55;
    ctx.save();
    const fontStr = getFont(titleSize, 900);
    ctx.font = fontStr;
    ctx.textBaseline = "top";

    const lines = wrapText(ctx, mainTitle, 1140, fontStr);
    let curY = titleY;
    const lineHeight = selectedFont === "bebas" ? titleSize * 1.02 : titleSize * 1.08;

    lines.slice(0, 2).forEach((line) => {
      ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
      ctx.shadowBlur = 16;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 4;
      ctx.fillStyle = colors.title;
      ctx.fillText(line, startX, curY);
      curY += lineHeight;
    });
    ctx.restore();

    if (subtitle && curY < CANVAS_HEIGHT - 25) {
      ctx.save();
      const subSize = subtitleSize || Math.max(26, Math.floor(titleSize * 0.36));
      ctx.font = getFont(subSize, 700, true);
      ctx.shadowColor = "rgba(0, 0, 0, 0.90)";
      ctx.shadowBlur = 10;
      ctx.shadowOffsetY = 2;
      ctx.fillStyle = colors.sub;
      ctx.textBaseline = "top";
      ctx.fillText(subtitle, startX, curY + 6);
      ctx.restore();
    }
  }

  function renderFrostedCard(ctx: CanvasRenderingContext2D) {
    const colors = getThemeColors();
    const cardX = 54;
    const cardY = 44;
    const cardW = 790;
    const cardH = CANVAS_HEIGHT - 88;

    ctx.save();
    ctx.shadowColor = "rgba(0, 0, 0, 0.6)";
    ctx.shadowBlur = 24;
    ctx.shadowOffsetY = 10;
    ctx.fillStyle = colors.cardBg;
    roundRect(ctx, cardX, cardY, cardW, cardH, 18);
    ctx.fill();
    ctx.restore();

    renderWatermarkNumeral(ctx, cardX + cardW - 140, cardY + cardH / 2);

    const startX = cardX + 46;
    const badgeY = cardY + 54;
    let badgeX = startX;

    if (selectedClass && selectedClass.trim()) {
      badgeX = drawInvertedPill(ctx, badgeX, badgeY, selectedClass.trim(), colors.accentPillBg, colors.accentPillText);
      badgeX += 12;
    }
    if (chapterBadge && chapterBadge.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, chapterBadge.trim(), colors.eyebrowBg, colors.eyebrowText);
      badgeX += 12;
    }
    if (partNumber && partNumber.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, partNumber.trim(), "rgba(255,255,255,0.18)", "#FFFFFF");
      badgeX += 12;
    }
    if (tagBadge && tagBadge.trim()) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge.trim(), "rgba(255,255,255,0.12)", "#FFFFFF");
    }

    const titleY = badgeY + 55;
    ctx.save();
    const fontStr = getFont(titleSize, 900);
    ctx.font = fontStr;
    ctx.textBaseline = "top";
    let curY = titleY;
    const lineHeight = selectedFont === "bebas" ? titleSize * 1.02 : titleSize * 1.08;

    const lines = wrapText(ctx, mainTitle, 690, fontStr);
    lines.forEach((line) => {
      ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
      ctx.shadowBlur = 14;
      ctx.shadowOffsetY = 3;
      ctx.fillStyle = colors.title;
      ctx.fillText(line, startX, curY);
      curY += lineHeight;
    });
    ctx.restore();

    if (subtitle && subtitle.trim()) {
      ctx.save();
      const subSize = subtitleSize || Math.max(26, Math.floor(titleSize * 0.36));
      ctx.font = getFont(subSize, 700, true);
      ctx.shadowColor = "rgba(0, 0, 0, 0.90)";
      ctx.shadowBlur = 10;
      ctx.shadowOffsetY = 2;
      ctx.fillStyle = colors.sub;
      ctx.textBaseline = "top";
      const subLines = wrapText(ctx, subtitle, 670, getFont(subSize, 700, true));
      let subY = curY + 14;
      subLines.forEach((sLine) => {
        ctx.fillText(sLine, startX, subY);
        subY += subSize * 1.25;
      });
      ctx.restore();
    }
  }

  function renderSwissPoster(ctx: CanvasRenderingContext2D) {
    const colors = getThemeColors();

    const panelGrad = ctx.createLinearGradient(0, 0, 880, 0);
    panelGrad.addColorStop(0, colors.gradientEnd);
    panelGrad.addColorStop(0.65, colors.gradientEnd);
    panelGrad.addColorStop(1, "rgba(9, 9, 11, 0)");
    ctx.fillStyle = panelGrad;
    ctx.fillRect(0, 0, 900, CANVAS_HEIGHT);

    renderWatermarkNumeral(ctx, 400, 360);

    const startX = 72;
    const badgeY = titleSize > 115 ? 95 : 110;
    let badgeX = startX;

    if (selectedClass && selectedClass.trim()) {
      badgeX = drawInvertedPill(ctx, badgeX, badgeY, selectedClass.trim(), colors.accentPillBg, colors.accentPillText);
      badgeX += 12;
    }
    if (chapterBadge && chapterBadge.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, chapterBadge.trim(), colors.eyebrowBg, colors.eyebrowText);
      badgeX += 12;
    }
    if (partNumber && partNumber.trim()) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, partNumber.trim(), "rgba(255,255,255,0.18)", "#FFFFFF");
      badgeX += 12;
    }
    if (tagBadge && tagBadge.trim()) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge.trim(), "rgba(255,255,255,0.10)", "#FFFFFF");
    }

    const titleY = badgeY + 55;
    ctx.save();
    const fontStr = getFont(titleSize, 900);
    ctx.font = fontStr;
    ctx.textBaseline = "top";
    let curY = titleY;
    const lineHeight = selectedFont === "bebas" ? titleSize * 1.02 : titleSize * 1.08;

    const lines = wrapText(ctx, mainTitle, 710, fontStr);
    lines.forEach((line) => {
      ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
      ctx.shadowBlur = 16;
      ctx.shadowOffsetY = 4;
      ctx.fillStyle = colors.title;
      ctx.fillText(line, startX, curY);
      curY += lineHeight;
    });
    ctx.restore();

    if (subtitle && subtitle.trim()) {
      ctx.save();
      const subSize = subtitleSize || Math.max(26, Math.floor(titleSize * 0.36));
      ctx.font = getFont(subSize, 700, true);
      ctx.shadowColor = "rgba(0, 0, 0, 0.90)";
      ctx.shadowBlur = 10;
      ctx.shadowOffsetY = 2;
      ctx.fillStyle = colors.sub;
      ctx.textBaseline = "top";
      const subLines = wrapText(ctx, subtitle, 690, getFont(subSize, 700, true));
      let subY = curY + 14;
      subLines.forEach((sLine) => {
        ctx.fillText(sLine, startX, subY);
        subY += subSize * 1.25;
      });
      ctx.restore();
    }
  }

  function renderCanvas() {
    if (!canvasEl) return;
    const ctx = canvasEl.getContext("2d");
    if (!ctx) return;

    ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // 1. Background Image or Clean Obsidian Studio Base
    if (bgImage && bgImage.complete && bgImage.naturalWidth > 0) {
      const img = bgImage;
      const imgRatio = img.width / img.height;
      const targetRatio = CANVAS_WIDTH / CANVAS_HEIGHT;
      let sx = 0, sy = 0, sw = img.width, sh = img.height;

      if (imgRatio > targetRatio) {
        sw = img.height * targetRatio;
        sx = (img.width - sw) / 2;
      } else {
        sh = img.width / targetRatio;
        sy = (img.height - sh) / 2;
      }
      ctx.drawImage(img, sx, sy, sw, sh, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    } else {
      const bgGrad = ctx.createLinearGradient(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
      bgGrad.addColorStop(0, "#0e111a");
      bgGrad.addColorStop(0.5, "#090b12");
      bgGrad.addColorStop(1, "#05060a");
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    }

    // 2. Global Dimmer
    if (bgDarkness > 0) {
      ctx.fillStyle = `rgba(0, 0, 0, ${bgDarkness})`;
      ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    }

    // 3. Layout Rendering
    if (layout === "editorial_left") {
      renderEditorialLeft(ctx);
    } else if (layout === "horizon_bottom") {
      renderHorizonBottom(ctx);
    } else if (layout === "frosted_card") {
      renderFrostedCard(ctx);
    } else if (layout === "swiss_poster") {
      renderSwissPoster(ctx);
    }

    // 4. Subtle Vignette
    const radGrad = ctx.createRadialGradient(
      CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, CANVAS_WIDTH * 0.45,
      CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, CANVAS_WIDTH * 0.8
    );
    radGrad.addColorStop(0, "rgba(0,0,0,0)");
    radGrad.addColorStop(1, "rgba(0,0,0,0.45)");
    ctx.fillStyle = radGrad;
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // 5. Channel Watermark Stamp
    if (showChannel && channelName) {
      renderChannelPill(ctx);
    }

    // 6. Mobile Preview Simulation URL
    simThumbUrl = canvasEl.toDataURL("image/jpeg", 0.70);
  }

  async function downloadThumbnail() {
    if (!canvasEl) return;
    renderCanvas();
    const safeCh = (chapterBadge || "CH").replace(/[^a-zA-Z0-9]/g, "");
    const safeClass = (selectedClass || "Physics").replace("+", "Plus").replace(/[^a-zA-Z0-9]/g, "_");
    const filename = `Dhanya_${safeClass}_${safeCh}_${Date.now()}.jpg`;
    const dataUrl = canvasEl.toDataURL("image/jpeg", 0.95);

    const isNative = typeof window !== "undefined" && (
      (window as any).Capacitor || 
      window.location.protocol.startsWith("capacitor") || 
      window.location.protocol === "file:"
    );

    if (isNative) {
      triggerToast("Preparing download... ⏳");
      try {
        const base64Data = dataUrl.substring(dataUrl.indexOf(",") + 1);

        const writeResult = await Filesystem.writeFile({
          path: filename,
          data: base64Data,
          directory: Directory.Cache
        });

        await Share.share({
          title: "Save or Share Thumbnail",
          text: "Generated physics class thumbnail",
          url: writeResult.uri,
          dialogTitle: "Save or Share Thumbnail"
        });
        
        triggerToast("Save/Share panel opened! 🎉");
      } catch (err) {
        console.error("Error saving/sharing native file:", err);
        triggerToast("Failed to save natively.");
      }
    } else {
      const link = document.createElement("a");
      link.download = filename;
      link.href = dataUrl;
      link.click();
      triggerToast("Downloaded 1280 × 720 HD Thumbnail! 🎉");
    }
  }

  function copyToClipboard() {
    if (!canvasEl) return;
    renderCanvas();
    canvasEl.toBlob((blob) => {
      if (!blob) return;
      if (navigator.clipboard && navigator.clipboard.write) {
        navigator.clipboard.write([
          new ClipboardItem({ "image/png": blob })
        ]).then(() => {
          triggerToast("Copied HD thumbnail to clipboard!");
        }).catch(() => {
          triggerToast("Clipboard copy not supported");
        });
      }
    }, "image/png");
  }

  $effect(() => {
    const _c = selectedClass;
    const _ch = chapterBadge;
    const _p = partNumber;
    const _t = tagBadge;
    const _m = mainTitle;
    const _s = subtitle;
    const _cn = channelName;
    const _sc = showChannel;
    const _l = layout;
    const _f = selectedFont;
    const _d = bgDarkness;
    const _ct = colorTheme;
    const _wn = showWatermarkNum;
    const _ts = titleSize;
    const _ss = subtitleSize;
    const _bg = bgImage;

    if (canvasEl) {
      renderCanvas();
    }
  });

  onMount(async () => {
    if (document.fonts) {
      try {
        await Promise.all([
          document.fonts.load('900 72px "Inter"'),
          document.fonts.load('400 84px "Bebas Neue"'),
          document.fonts.load('800 72px "Plus Jakarta Sans"')
        ]);
      } catch (e) {
        console.warn("Font notice", e);
      }
      await document.fonts.ready;
    }
    renderCanvas();
  });
</script>

<div class="w-full max-w-full overflow-x-hidden pb-16">
  
  <!-- ========================================================
       UNIFIED LIVE STUDIO WORKSPACE (Easy, Fast, Intuitive)
       ======================================================== -->
  <main class="w-full max-w-7xl mx-auto p-3 sm:p-5 lg:p-6">
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
      
      <!-- ====================================================
           RIGHT COLUMN ON LARGE / TOP ON MOBILE: LIVE PREVIEW
           ==================================================== -->
      <div class="lg:col-span-5 order-first lg:order-last space-y-4 lg:sticky lg:top-20 z-20">
        
        <!-- Live HD Canvas Card -->
        <Card class="w-full overflow-hidden shadow-lg border-primary/20">
          <CardHeader class="p-3 sm:p-4 pb-2">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="inline-block size-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <CardTitle class="text-sm font-semibold">Live 1280 × 720 Preview</CardTitle>
              </div>
              <Badge variant="outline" class="font-mono text-[11px]">{selectedClass}</Badge>
            </div>
          </CardHeader>
          <CardContent class="p-0">
            <div class="w-full aspect-video bg-black overflow-hidden relative group">
              <canvas
                bind:this={canvasEl}
                width={CANVAS_WIDTH}
                height={CANVAS_HEIGHT}
                class="w-full h-full object-contain block"
              ></canvas>
            </div>
          </CardContent>
          <div class="p-3 bg-muted/30 border-t flex items-center gap-2">
            <Button
              size="lg"
              class="flex-1 font-bold gap-2 shadow-sm"
              onclick={downloadThumbnail}
            >
              <Download class="size-4" />
              <span>Download HD</span>
            </Button>
            <Button
              variant="outline"
              size="lg"
              class="px-3"
              onclick={copyToClipboard}
              title="Copy to Clipboard"
            >
              <Copy class="size-4" />
            </Button>
          </div>
        </Card>

        <!-- YouTube Mobile Feed Real-world Preview -->
        <Card class="bg-muted/15 border-dashed">
          <CardHeader class="p-3 pb-1">
            <CardTitle class="text-[11px] font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-1.5">
              <Smartphone class="size-3.5" />
              Phone Screen Readability Check
            </CardTitle>
          </CardHeader>
          <CardContent class="p-3 pt-1">
            <div class="flex gap-3 items-center">
              <img
                src={simThumbUrl}
                alt="Mobile preview"
                class="w-28 aspect-video object-cover rounded bg-black shrink-0 border shadow-sm"
              />
              <div class="min-w-0 flex-1">
                <p class="text-xs font-semibold line-clamp-2 leading-snug">
                  {selectedClass} | {mainTitle} {partNumber ? `| ${partNumber}` : ''}
                </p>
                <p class="text-[10px] text-muted-foreground mt-0.5 truncate">
                  {channelName} • YouTube Mobile
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

      </div>

      <!-- ====================================================
           LEFT COLUMN: ALL TEXT INPUTS & CONTROLS (NO DROPDOWNS)
           ==================================================== -->
      <div class="lg:col-span-7 space-y-5">
        
        <!-- 1. YouTube Video Link & Prefill -->
        <Card>
          <CardHeader class="pb-3">
            <div class="flex items-center justify-between">
              <CardTitle class="text-base flex items-center gap-2">
                <Video class="size-4 text-primary" />
                YouTube Video Link
              </CardTitle>
              <Button
                variant="ghost"
                size="sm"
                class="h-7 text-xs gap-1 text-muted-foreground"
                onclick={() => showApiKeyInput = !showApiKeyInput}
              >
                <Key class="size-3.5" />
                {geminiApiKey ? "AI Key Configured" : "Add Gemini Key"}
              </Button>
            </div>
            <CardDescription class="text-xs">
              Paste your video link to automatically grab the high-resolution frame and prefill all inputs.
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-3">
            
            <div class="flex gap-2">
              <Input
                bind:value={ytUrl}
                onkeydown={(e) => e.key === 'Enter' && fetchYouTubeThumbnail()}
                placeholder="Paste YouTube link: https://youtube.com/watch?v=..."
                class="text-sm"
              />
              <Button disabled={isFetching} onclick={fetchYouTubeThumbnail} class="shrink-0 font-medium">
                {#if isFetching}
                  <RefreshCw class="size-4 animate-spin mr-1.5" />
                {/if}
                Fetch Video
              </Button>
            </div>

            {#if ytStatus}
              <p class="text-xs text-muted-foreground flex items-center gap-1.5">
                <Check class="size-3 text-emerald-500" />
                {ytStatus}
              </p>
            {/if}

            <!-- Collapsible Gemini API Key Input -->
            {#if showApiKeyInput}
              <div class="p-3 rounded-lg bg-muted/40 border space-y-2 mt-2">
                <div class="flex items-center justify-between">
                  <Label class="text-xs font-semibold flex items-center gap-1.5">
                    <Key class="size-3 text-primary" />
                    Gemini API Key (Optional)
                  </Label>
                  {#if geminiApiKey}
                    <Badge variant="outline" class="text-[10px] text-emerald-500">Active</Badge>
                  {/if}
                </div>
                <div class="flex gap-2">
                  <Input
                    type="password"
                    placeholder="AIzaSy..."
                    value={geminiApiKey}
                    onchange={(e) => saveApiKey((e.target as HTMLInputElement).value)}
                    class="text-xs font-mono"
                  />
                  <Button
                    size="sm"
                    variant="secondary"
                    onclick={() => saveApiKey(geminiApiKey)}
                    class="text-xs shrink-0"
                  >
                    Save
                  </Button>
                </div>
                <p class="text-[11px] text-muted-foreground">
                  Saved securely in your browser to unlock Gemini Flash automated extraction.
                </p>
              </div>
            {/if}

            <!-- Quick Sample Video Button -->
            <div class="flex items-center gap-2 pt-1">
              <Button
                variant="outline"
                size="sm"
                class="text-xs h-7"
                onclick={() => {
                  ytUrl = "https://www.youtube.com/watch?v=c-M2jbSHhTg";
                  fetchYouTubeThumbnail();
                }}
              >
                Load Sample: +1 Chapter 5 Video
              </Button>
            </div>

          </CardContent>
        </Card>

        <!-- 2. Primary Thumbnail Texts (ALL FREE TEXT INPUTS) -->
        <Card>
          <CardHeader class="pb-3">
            <div class="flex items-center justify-between">
              <CardTitle class="text-base flex items-center gap-2">
                <Type class="size-4 text-primary" />
                Thumbnail Texts (Free Inputs)
              </CardTitle>
              <div class="flex items-center gap-1.5">
                <Button
                  variant="outline"
                  size="sm"
                  class="h-7 text-xs font-medium"
                  onclick={toggleLanguage}
                >
                  {isMalayalamTitle ? "English" : "മലയാളം"}
                </Button>
              </div>
            </div>
            <CardDescription class="text-xs">
              Every field is a plain text input. Edit or type anything you want.
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            
            <!-- Category / Class Badge Input -->
            <div class="space-y-1.5">
              <Label class="text-xs font-semibold">Category / Class Badge</Label>
              <Input
                bind:value={selectedClass}
                placeholder="e.g. +1 PHYSICS, +2 PHYSICS, NEET"
                class="font-medium"
              />
              <div class="flex flex-wrap gap-1.5 pt-0.5">
                <button
                  type="button"
                  class="text-[11px] px-2.5 py-0.5 rounded-full border bg-muted/40 hover:bg-muted transition font-medium"
                  onclick={() => selectedClass = "+1 PHYSICS"}
                >
                  +1 PHYSICS
                </button>
                <button
                  type="button"
                  class="text-[11px] px-2.5 py-0.5 rounded-full border bg-muted/40 hover:bg-muted transition font-medium"
                  onclick={() => selectedClass = "+2 PHYSICS"}
                >
                  +2 PHYSICS
                </button>
                <button
                  type="button"
                  class="text-[11px] px-2.5 py-0.5 rounded-full border bg-muted/40 hover:bg-muted transition font-medium"
                  onclick={() => selectedClass = "NEET PHYSICS"}
                >
                  NEET PHYSICS
                </button>
                <button
                  type="button"
                  class="text-[11px] px-2.5 py-0.5 rounded-full border bg-muted/40 hover:bg-muted transition font-medium"
                  onclick={() => selectedClass = "KEAM / ENTRANCE"}
                >
                  KEAM
                </button>
              </div>
            </div>

            <!-- Chapter Badge Input -->
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <Label class="text-xs font-semibold">Chapter Tag / Label</Label>
                <button
                  type="button"
                  class="text-xs text-primary hover:underline font-medium flex items-center gap-1"
                  onclick={() => showChapterPresets = !showChapterPresets}
                >
                  <BookOpen class="size-3" />
                  {showChapterPresets ? "Hide Syllabus Chapters" : "Quick Syllabus Chapters"}
                  {#if showChapterPresets}
                    <ChevronUp class="size-3" />
                  {:else}
                    <ChevronDown class="size-3" />
                  {/if}
                </button>
              </div>
              <Input
                bind:value={chapterBadge}
                placeholder="e.g. CH 05 or CHAPTER 5"
                class="font-medium"
              />

              <!-- Collapsible Syllabus Quick Picker -->
              {#if showChapterPresets}
                <div class="p-2.5 rounded-lg border bg-muted/30 space-y-2 animate-in fade-in duration-150">
                  <p class="text-[11px] font-medium text-muted-foreground">
                    Click any chapter to prefill title & derivations (still 100% editable):
                  </p>
                  <div class="grid grid-cols-2 sm:grid-cols-3 gap-1.5 max-h-48 overflow-y-auto p-1">
                    {#each currentSyllabusList as ch (ch.num)}
                      <button
                        type="button"
                        class="text-left text-xs p-1.5 rounded border bg-card hover:bg-accent transition truncate"
                        onclick={() => selectChapterPreset(ch)}
                      >
                        <span class="font-bold text-primary mr-1">Ch {ch.num}:</span>
                        <span>{ch.title}</span>
                      </button>
                    {/each}
                  </div>
                </div>
              {/if}
            </div>

            <!-- Main Headline Text Input (Huge Thumbnail Headline) -->
            <div class="space-y-1.5">
              <div class="flex items-center justify-between">
                <Label class="text-xs font-semibold">Main Headline Text (Big Impact)</Label>
                <span class="text-[11px] text-muted-foreground">Keep to 3-5 punchy words</span>
              </div>
              <Input
                bind:value={mainTitle}
                placeholder="e.g. WORK, ENERGY & POWER"
                class="font-bold text-base sm:text-lg"
              />
            </div>

            <!-- Subtitle / Key Derivation Input -->
            <div class="space-y-1.5">
              <Label class="text-xs font-semibold">Subtitle / Topic / Derivation</Label>
              <Input
                bind:value={subtitle}
                placeholder="e.g. Work-Energy Theorem & Important Derivations"
              />
              <!-- Derivation suggestion chips -->
              {#if currentChapterObj && currentChapterObj.derivations}
                <div class="flex flex-wrap gap-1.5 pt-0.5">
                  {#each currentChapterObj.derivations as dev, idx (dev + idx)}
                    <button
                      type="button"
                      class="text-[11px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted transition truncate max-w-[280px]"
                      onclick={() => subtitle = dev}
                      title={dev}
                    >
                      {dev}
                    </button>
                  {/each}
                </div>
              {/if}
            </div>

            <!-- Video Part & Exam Tag in 2 Columns -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              
              <!-- Video Part Input -->
              <div class="space-y-1.5">
                <Label class="text-xs font-semibold">Video Part</Label>
                <Input
                  bind:value={partNumber}
                  placeholder="e.g. PART 1 (or leave empty)"
                />
                <div class="flex flex-wrap gap-1 pt-0.5">
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => partNumber = ""}
                  >
                    Clear
                  </button>
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => partNumber = "PART 1"}
                  >
                    Part 1
                  </button>
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => partNumber = "PART 2"}
                  >
                    Part 2
                  </button>
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => partNumber = "PART 3"}
                  >
                    Part 3
                  </button>
                </div>
              </div>

              <!-- Exam Focus Tag Input -->
              <div class="space-y-1.5">
                <Label class="text-xs font-semibold">Exam Badge Tag</Label>
                <Input
                  bind:value={tagBadge}
                  placeholder="e.g. CORE DERIVATIONS"
                />
                <div class="flex flex-wrap gap-1 pt-0.5">
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => tagBadge = ""}
                  >
                    None
                  </button>
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => tagBadge = "CORE DERIVATIONS"}
                  >
                    Derivations
                  </button>
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => tagBadge = "ONE SHOT REVISION"}
                  >
                    One Shot
                  </button>
                  <button
                    type="button"
                    class="text-[10px] px-2 py-0.5 rounded border bg-muted/40 hover:bg-muted"
                    onclick={() => tagBadge = "EXAM ESSENTIALS"}
                  >
                    Essentials
                  </button>
                </div>
              </div>

            </div>

            <!-- Channel Name Input -->
            <div class="space-y-1.5 pt-1">
              <Label class="text-xs font-semibold">Channel Badge Name</Label>
              <Input
                bind:value={channelName}
                placeholder="PHYSICS With Dhanya"
              />
            </div>

          </CardContent>
        </Card>

        <!-- 3. High-Impact Typography & Visual Styling -->
        <Card>
          <CardHeader class="pb-3">
            <CardTitle class="text-base flex items-center gap-2">
              <SlidersHorizontal class="size-4 text-primary" />
              Thumbnail Size & Style Controls
            </CardTitle>
            <CardDescription class="text-xs">
              Make text as big as you want so it punches out vividly on student smartphone feeds.
            </CardDescription>
          </CardHeader>
          <CardContent class="space-y-4">
            
            <!-- Headline Font Size (Supports Up to 165px!) -->
            <div class="space-y-2">
              <div class="flex items-center justify-between text-xs">
                <Label class="font-semibold">Headline Text Size (Impact Scale)</Label>
                <span class="font-mono font-bold text-primary bg-primary/10 px-2 py-0.5 rounded">{titleSize}px</span>
              </div>
              
              <!-- Quick Preset Buttons -->
              <div class="grid grid-cols-4 gap-1.5 pb-1">
                <Button
                  variant={titleSize === 76 ? "default" : "outline"}
                  size="sm"
                  class="h-7 text-xs"
                  onclick={() => titleSize = 76}
                >
                  Normal (76px)
                </Button>
                <Button
                  variant={titleSize === 96 ? "default" : "outline"}
                  size="sm"
                  class="h-7 text-xs"
                  onclick={() => titleSize = 96}
                >
                  Bold (96px)
                </Button>
                <Button
                  variant={titleSize === 120 ? "default" : "outline"}
                  size="sm"
                  class="h-7 text-xs"
                  onclick={() => titleSize = 120}
                >
                  Huge (120px)
                </Button>
                <Button
                  variant={titleSize === 145 ? "default" : "outline"}
                  size="sm"
                  class="h-7 text-xs"
                  onclick={() => titleSize = 145}
                >
                  Mega (145px)
                </Button>
              </div>

              <Slider
                type="single"
                bind:value={titleSize}
                min={50}
                max={165}
                step={2}
              />
            </div>

            <!-- Subtitle Font Size Slider -->
            <div class="space-y-2">
              <div class="flex items-center justify-between text-xs">
                <Label class="font-semibold">Subtitle Text Size</Label>
                <span class="font-mono font-medium text-muted-foreground">{subtitleSize}px</span>
              </div>
              <Slider
                type="single"
                bind:value={subtitleSize}
                min={22}
                max={54}
                step={2}
              />
            </div>

            <!-- Background Dimmer Slider -->
            <div class="space-y-2">
              <div class="flex items-center justify-between text-xs">
                <Label class="font-semibold">Background Dimmer (Handwriting & Contrast)</Label>
                <span class="font-mono font-medium text-muted-foreground">{bgDarknessPercent}%</span>
              </div>
              <Slider
                type="single"
                bind:value={bgDarknessPercent}
                min={10}
                max={80}
                step={5}
              />
            </div>

            <Separator />

            <!-- Font Family Buttons -->
            <div class="space-y-2">
              <Label class="text-xs font-semibold">Designer Font Family</Label>
              <div class="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  class="p-2.5 rounded-lg border text-left transition {selectedFont === 'inter' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => selectedFont = "inter"}
                >
                  <p class="font-bold text-xs">Inter</p>
                  <p class="text-[10px] text-muted-foreground">Swiss Modern</p>
                </button>
                <button
                  type="button"
                  class="p-2.5 rounded-lg border text-left transition {selectedFont === 'bebas' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => selectedFont = "bebas"}
                >
                  <p class="font-bold text-xs uppercase tracking-wider">Bebas Neue</p>
                  <p class="text-[10px] text-muted-foreground">Bold Display</p>
                </button>
                <button
                  type="button"
                  class="p-2.5 rounded-lg border text-left transition {selectedFont === 'jakarta' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => selectedFont = "jakarta"}
                >
                  <p class="font-bold text-xs">Plus Jakarta</p>
                  <p class="text-[10px] text-muted-foreground">Clean Modern</p>
                </button>
              </div>
            </div>

            <!-- Layout Structure Selection -->
            <div class="space-y-2">
              <Label class="text-xs font-semibold">Thumbnail Layout</Label>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {layout === 'editorial_left' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => layout = "editorial_left"}
                >
                  <p class="font-semibold text-xs">Studio Left</p>
                  <p class="text-[10px] text-muted-foreground">Recommended</p>
                </button>
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {layout === 'horizon_bottom' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => layout = "horizon_bottom"}
                >
                  <p class="font-semibold text-xs">Horizon</p>
                  <p class="text-[10px] text-muted-foreground">Lower Third</p>
                </button>
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {layout === 'frosted_card' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => layout = "frosted_card"}
                >
                  <p class="font-semibold text-xs">Studio Card</p>
                  <p class="text-[10px] text-muted-foreground">Frosted</p>
                </button>
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {layout === 'swiss_poster' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => layout = "swiss_poster"}
                >
                  <p class="font-semibold text-xs">Swiss Poster</p>
                  <p class="text-[10px] text-muted-foreground">Minimalist</p>
                </button>
              </div>
            </div>

            <!-- Contrast Color Theme Selection -->
            <div class="space-y-2">
              <Label class="text-xs font-semibold">Contrast Palette</Label>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {colorTheme === 'mono_pure' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => colorTheme = "mono_pure"}
                >
                  <div class="size-3 rounded-full bg-white border mb-1"></div>
                  <p class="font-semibold text-xs">Pure Mono</p>
                </button>
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {colorTheme === 'mono_slate' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => colorTheme = "mono_slate"}
                >
                  <div class="size-3 rounded-full bg-slate-300 border mb-1"></div>
                  <p class="font-semibold text-xs">Studio Slate</p>
                </button>
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {colorTheme === 'warm_editorial' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => colorTheme = "warm_editorial"}
                >
                  <div class="size-3 rounded-full bg-stone-200 border mb-1"></div>
                  <p class="font-semibold text-xs">Warm Ivory</p>
                </button>
                <button
                  type="button"
                  class="p-2 rounded-lg border text-left transition {colorTheme === 'subtle_amber' ? 'border-primary bg-primary/10' : 'bg-muted/30 hover:bg-muted'}"
                  onclick={() => colorTheme = "subtle_amber"}
                >
                  <div class="size-3 rounded-full bg-amber-400 border mb-1"></div>
                  <p class="font-semibold text-xs">Amber Accent</p>
                </button>
              </div>
            </div>

            <!-- Toggles -->
            <div class="flex items-center justify-between pt-2">
              <div class="space-y-0.5">
                <Label class="text-xs font-medium">Ghost Chapter Numeral</Label>
                <p class="text-[11px] text-muted-foreground">Stylized faint background numeral</p>
              </div>
              <Switch bind:checked={showWatermarkNum} />
            </div>

            <div class="flex items-center justify-between">
              <div class="space-y-0.5">
                <Label class="text-xs font-medium">Channel Name Stamp</Label>
                <p class="text-[11px] text-muted-foreground">Physics with Dhanya bottom badge</p>
              </div>
              <Switch bind:checked={showChannel} />
            </div>

          </CardContent>
        </Card>

        <!-- 4. AI SEO & YouTube Publishing Kit (Expandable) -->
        <Card>
          <CardHeader class="pb-3">
            <div class="flex items-center justify-between">
              <CardTitle class="text-base flex items-center gap-2">
                <Sparkles class="size-4 text-primary" />
                AI SEO & Publishing Kit (Gemini Flash)
              </CardTitle>
              <Button
                variant="outline"
                size="sm"
                class="h-7 text-xs"
                disabled={isGeneratingSeo}
                onclick={generateSeoKit}
              >
                {#if isGeneratingSeo}
                  <RefreshCw class="size-3 animate-spin mr-1" />
                  Generating...
                {:else}
                  <Sparkles class="size-3 mr-1" />
                  {seoData ? "Regenerate" : "Generate SEO Kit"}
                {/if}
              </Button>
            </div>
            <CardDescription class="text-xs">
              Channel-standardized titles, bilingual descriptions, and 15 high-CTR exam search tags.
            </CardDescription>
          </CardHeader>
          
          {#if showSeoSection}
            <CardContent class="space-y-4 pt-1">
              {#if isGeneratingSeo}
                <div class="py-10 flex flex-col items-center justify-center text-center space-y-2">
                  <RefreshCw class="size-6 animate-spin text-primary" />
                  <p class="text-xs font-medium">Analyzing video with Gemini Flash...</p>
                  <p class="text-[11px] text-muted-foreground">Extracting Kerala syllabus tags & structuring description</p>
                </div>
              {:else if seoData}
                
                <!-- Standardized Video Title -->
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between">
                    <Label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                      Channel-Standardized Video Title
                    </Label>
                    <Button variant="ghost" size="sm" class="h-6 text-xs" onclick={() => copyText(seoData!.title, "Title")}>
                      <Copy class="size-3 mr-1" />
                      Copy Title
                    </Button>
                  </div>
                  <div class="p-2.5 bg-muted/40 rounded-md border font-medium text-xs">
                    {seoData.title}
                  </div>
                </div>

                <!-- YouTube SEO Description -->
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between">
                    <Label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                      SEO Description (Malayalam + English)
                    </Label>
                    <Button variant="ghost" size="sm" class="h-6 text-xs" onclick={() => copyText(seoData!.description, "Description")}>
                      <Copy class="size-3 mr-1" />
                      Copy Description
                    </Button>
                  </div>
                  <div class="p-2.5 bg-muted/40 rounded-md border text-xs whitespace-pre-wrap max-h-48 overflow-y-auto leading-relaxed">
                    {seoData.description}
                  </div>
                </div>

                <!-- YouTube Search Tags -->
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between">
                    <Label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                      High-CTR YouTube Search Tags
                    </Label>
                    <Button variant="ghost" size="sm" class="h-6 text-xs" onclick={() => copyText(seoData!.tags_string, "Tags")}>
                      <Copy class="size-3 mr-1" />
                      Copy All Tags
                    </Button>
                  </div>
                  <div class="p-2 bg-muted/40 rounded-md border flex flex-wrap gap-1">
                    {#each seoData.tags_string.split(", ") as tag, idx (tag + idx)}
                      <Badge variant="secondary" class="text-[11px] font-normal">{tag}</Badge>
                    {/each}
                  </div>
                </div>

                <!-- Malayalam Exam Points -->
                {#if seoData.malayalam_summary}
                  <div class="space-y-1.5">
                    <Label class="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                      Malayalam Study Notes (മലയാളം)
                    </Label>
                    <div class="p-2.5 bg-muted/40 rounded-md border text-xs leading-relaxed">
                      {seoData.malayalam_summary}
                    </div>
                  </div>
                {/if}

                <!-- Spoken Malayalam Captions / Transcript -->
                {#if seoData.has_captions}
                  <div class="p-3 bg-muted/20 rounded-lg border flex items-center justify-between gap-2">
                    <div class="space-y-0.5">
                      <p class="text-xs font-medium">Spoken Malayalam Audio Subtitles</p>
                      <p class="text-[10px] text-muted-foreground">Auto-generated transcript available</p>
                    </div>
                    <div class="flex items-center gap-1.5">
                      <Button variant="outline" size="sm" class="h-7 text-xs" onclick={() => copyText(seoData!.captions_text, "Captions")}>
                        <Copy class="size-3 mr-1" />
                        Copy
                      </Button>
                      <Button variant="secondary" size="sm" class="h-7 text-xs" href={`${API_BASE}/api/download-captions?video_id=${ytUrl || "c-M2jbSHhTg"}`} target="_blank">
                        <Download class="size-3 mr-1" />
                        .txt
                      </Button>
                    </div>
                  </div>
                {/if}

              {/if}
            </CardContent>
          {/if}
        </Card>

      </div>

    </div>
  </main>

  <!-- Toast Notification -->
  {#if showToast}
    <div class="fixed top-16 right-6 z-50 bg-foreground text-background font-medium text-xs py-2 px-3.5 rounded-md shadow-lg flex items-center gap-2 animate-in fade-in duration-150">
      <Check class="size-3.5" />
      <span>{toastMessage}</span>
    </div>
  {/if}

</div>
