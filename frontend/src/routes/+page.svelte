<script lang="ts">
  import { onMount } from "svelte";
  import { Button } from "$lib/components/ui/button";
  import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "$lib/components/ui/card";
  import { Input } from "$lib/components/ui/input";
  import { Badge } from "$lib/components/ui/badge";
  import { Label } from "$lib/components/ui/label";
  import { Separator } from "$lib/components/ui/separator";
  import { Switch } from "$lib/components/ui/switch";
  import { Slider } from "$lib/components/ui/slider";
  import { Select, SelectContent, SelectGroup, SelectGroupHeading, SelectItem, SelectTrigger, SelectValue } from "$lib/components/ui/select";

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
  import ChevronRight from "@lucide/svelte/icons/chevron-right";
  import ChevronLeft from "@lucide/svelte/icons/chevron-left";

  const CANVAS_WIDTH = 1280;
  const CANVAS_HEIGHT = 720;

  // Navigation State
  let activePage = $state<"input" | "preview">("input");
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

  // App Reactive State
  let ytUrl = $state("");
  let ytStatus = $state("");
  let isFetching = $state(false);

  // Background Image starts empty (no pre-existing preview image)
  let bgImage: HTMLImageElement | null = $state(null);
  let bgDarknessPercent = $state(40);
  let bgDarkness = $derived(bgDarknessPercent / 100);

  // Typography & Design Presets
  let selectedFont = $state("inter");
  let layout = $state("editorial_left");
  let colorTheme = $state("mono_pure");
  let showWatermarkNum = $state(true);

  let selectedClass = $state("+1");
  let selectedChapterNum = $state(5);
  let selectedChapterStr = $state("5");
  let isMalayalamTitle = $state(false);

  let partNumber = $state("PART 1");
  let tagBadge = $state("CORE DERIVATIONS");

  let mainTitle = $state("WORK, ENERGY & POWER");
  let subtitle = $state("Work-Energy Theorem & Important Derivations");
  let channelName = $state("PHYSICS With Dhanya");
  let showChannel = $state(true);

  let titleSize = $state(76);

  let toastMessage = $state("");
  let showToast = $state(false);
  let canvasEl: HTMLCanvasElement | null = $state(null);
  let simThumbUrl = $state("");

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

  let currentChapterList = $derived(selectedClass === "+1" ? PLUS_ONE_CHAPTERS : PLUS_TWO_CHAPTERS);
  let currentChapterObj = $derived(currentChapterList.find(c => c.num === selectedChapterNum) || currentChapterList[0]);

  function triggerToast(msg: string) {
    toastMessage = msg;
    showToast = true;
    setTimeout(() => {
      showToast = false;
    }, 2400);
  }

  function applyChapter(ch: Chapter) {
    selectedChapterNum = ch.num;
    selectedChapterStr = String(ch.num);
    if (isMalayalamTitle) {
      mainTitle = ch.malayalam;
    } else {
      mainTitle = ch.title;
    }
    subtitle = ch.derivations[0] || ch.sub;
    triggerToast(`Loaded Chapter ${ch.num}: ${ch.title}`);
  }

  function toggleLanguage() {
    isMalayalamTitle = !isMalayalamTitle;
    if (isMalayalamTitle) {
      mainTitle = currentChapterObj.malayalam;
      triggerToast("Switched to Malayalam (മലയാളം)");
    } else {
      mainTitle = currentChapterObj.title;
      triggerToast("Switched to English");
    }
  }

  function loadImage(src: string): Promise<HTMLImageElement> {
    return new Promise((resolve) => {
      const img = new Image();
      img.crossOrigin = "anonymous";
      img.onload = () => {
        bgImage = img;
        renderCanvas();
        resolve(img);
      };
      img.onerror = () => {
        console.error("Failed to load image:", src);
        resolve(img);
      };
      img.src = src;
    });
  }

  async function fetchYouTubeThumbnail() {
    if (!ytUrl.trim()) return;
    isFetching = true;
    ytStatus = "Fetching video details...";
    try {
      const res = await fetch(`${API_BASE}/api/youtube-info?url=${encodeURIComponent(ytUrl)}`);
      if (!res.ok) throw new Error("Video not found");
      const data = await res.json();
      
      if (data.thumbnail_url) {
        await loadImage(data.thumbnail_url);
      }

      if (data.detected_class === "+2") {
        selectedClass = "+2";
      } else if (data.detected_class === "+1") {
        selectedClass = "+1";
      }

      if (data.detected_chapter_num) {
        selectedChapterNum = data.detected_chapter_num;
        selectedChapterStr = String(data.detected_chapter_num);
        const list = selectedClass === "+1" ? PLUS_ONE_CHAPTERS : PLUS_TWO_CHAPTERS;
        const found = list.find(c => c.num === data.detected_chapter_num);
        if (found) {
          applyChapter(found);
        }
      } else if (data.title) {
        mainTitle = data.title;
      }

      if (data.detected_part) {
        partNumber = data.detected_part;
      }

      if (data.author) {
        channelName = data.author;
      }

      ytStatus = `Loaded: "${data.title}"`;
      triggerToast("Video frame & chapter auto-loaded!");
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
    triggerToast("Generating SEO kit with Gemini Flash...");
    try {
      const res = await fetch(`${API_BASE}/api/generate-seo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          video_id: ytUrl || "c-M2jbSHhTg",
          class_name: selectedClass,
          chapter_num: selectedChapterNum,
          chapter_title: currentChapterObj.title,
          focus_topic: subtitle,
          part: partNumber,
          malayalam_title: currentChapterObj.malayalam
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
     CANVAS ENGINE (PURE BORDERLESS TYPOGRAPHY)
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
        eyebrowBg: "rgba(15, 23, 42, 0.75)",
        eyebrowText: "#F8FAFC",
        accentPillBg: "#F1F5F9",
        accentPillText: "#0F172A",
        cardBg: "rgba(15, 23, 42, 0.88)",
        gradientEnd: "#080d1a"
      };
    }
    if (colorTheme === "warm_editorial") {
      return {
        title: "#FDFBF7",
        sub: "#D6D3D1",
        eyebrowBg: "rgba(24, 24, 27, 0.82)",
        eyebrowText: "#FAFAF9",
        accentPillBg: "#F5F5F4",
        accentPillText: "#1C1917",
        cardBg: "rgba(24, 24, 27, 0.90)",
        gradientEnd: "#141210"
      };
    }
    if (colorTheme === "subtle_amber") {
      return {
        title: "#FFFFFF",
        sub: "#E4E4E7",
        eyebrowBg: "rgba(0, 0, 0, 0.75)",
        eyebrowText: "#FFFFFF",
        accentPillBg: "#F59E0B",
        accentPillText: "#000000",
        cardBg: "rgba(9, 9, 11, 0.88)",
        gradientEnd: "#09090b"
      };
    }
    // Default: mono_pure
    return {
      title: "#FFFFFF",
      sub: "#E4E4E7",
      eyebrowBg: "rgba(0, 0, 0, 0.70)",
      eyebrowText: "#FFFFFF",
      accentPillBg: "#FFFFFF",
      accentPillText: "#09090B",
      cardBg: "rgba(9, 9, 11, 0.86)",
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
    const fontSize = 19;
    ctx.font = `800 ${fontSize}px "Inter", sans-serif`;
    const metrics = ctx.measureText(text);
    const padX = 14;
    const padY = 7;
    const w = metrics.width + (padX * 2);
    const h = fontSize + (padY * 2);
    const radius = 6;
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
    const fontSize = 19;
    ctx.font = `900 ${fontSize}px "Inter", sans-serif`;
    const metrics = ctx.measureText(text);
    const padX = 14;
    const padY = 7;
    const w = metrics.width + (padX * 2);
    const h = fontSize + (padY * 2);
    const radius = 6;
    const topY = y - (h / 2);

    ctx.shadowColor = "rgba(0, 0, 0, 0.4)";
    ctx.shadowBlur = 6;
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
    const numStr = selectedChapterNum < 10 ? `0${selectedChapterNum}` : `${selectedChapterNum}`;
    ctx.save();
    ctx.font = `900 320px "Inter", "Bebas Neue", sans-serif`;
    ctx.fillStyle = "rgba(255, 255, 255, 0.07)";
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

    ctx.fillStyle = "rgba(9, 9, 11, 0.75)";
    roundRect(ctx, posX, posY, totalW, totalH, 8);
    ctx.fill();

    const iconCenterX = posX + 18;
    const iconCenterY = posY + totalH / 2;
    
    ctx.strokeStyle = "rgba(255, 255, 255, 0.85)";
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

    const panelGrad = ctx.createLinearGradient(0, 0, 920, 0);
    panelGrad.addColorStop(0, colors.gradientEnd);
    panelGrad.addColorStop(0.55, colors.gradientEnd);
    panelGrad.addColorStop(0.85, "rgba(9, 9, 11, 0.45)");
    panelGrad.addColorStop(1, "rgba(9, 9, 11, 0)");
    ctx.fillStyle = panelGrad;
    ctx.fillRect(0, 0, 960, CANVAS_HEIGHT);

    renderWatermarkNumeral(ctx, 420, 360);

    const startX = 72;
    const badgeY = 130;
    let badgeX = startX;

    const numPadded = selectedChapterNum < 10 ? `0${selectedChapterNum}` : `${selectedChapterNum}`;
    const eyebrowText = `${selectedClass} PHYSICS • CHAPTER ${numPadded}`;

    badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, eyebrowText, colors.eyebrowBg, colors.eyebrowText);
    badgeX += 12;

    if (partNumber) {
      badgeX = drawInvertedPill(ctx, badgeX, badgeY, partNumber, colors.accentPillBg, colors.accentPillText);
      badgeX += 12;
    }

    if (tagBadge) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge, "rgba(255,255,255,0.12)", "#FFFFFF");
    }

    const titleY = badgeY + 70;
    const fontStr = getFont(titleSize, 900);
    const lines = wrapText(ctx, mainTitle, 680, fontStr);

    ctx.save();
    ctx.font = fontStr;
    ctx.textBaseline = "top";
    let currentY = titleY;
    const lineHeight = selectedFont === "bebas" ? titleSize * 1.02 : titleSize * 1.10;

    lines.forEach((line) => {
      ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
      ctx.shadowBlur = 16;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 4;
      ctx.fillStyle = colors.title;
      ctx.fillText(line, startX, currentY);
      currentY += lineHeight;
    });
    ctx.restore();

    if (subtitle) {
      ctx.save();
      const subSize = Math.max(26, Math.floor(titleSize * 0.40));
      ctx.font = getFont(subSize, 700, true);
      ctx.textBaseline = "top";

      const subLines = wrapText(ctx, subtitle, 660, getFont(subSize, 700, true));
      let subY = currentY + 16;

      subLines.forEach((sLine) => {
        ctx.shadowColor = "rgba(0, 0, 0, 0.90)";
        ctx.shadowBlur = 10;
        ctx.shadowOffsetX = 0;
        ctx.shadowOffsetY = 2;
        ctx.fillStyle = colors.sub;
        ctx.fillText(sLine, startX, subY);
        subY += subSize * 1.30;
      });
      ctx.restore();
    }
  }

  function renderHorizonBottom(ctx: CanvasRenderingContext2D) {
    const colors = getThemeColors();
    const bannerHeight = 330;
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

    const numPadded = selectedChapterNum < 10 ? `0${selectedChapterNum}` : `${selectedChapterNum}`;
    const eyebrowText = `${selectedClass} PHYSICS • CHAPTER ${numPadded}`;

    badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, eyebrowText, colors.eyebrowBg, colors.eyebrowText);
    badgeX += 12;

    if (partNumber) {
      badgeX = drawInvertedPill(ctx, badgeX, badgeY, partNumber, colors.accentPillBg, colors.accentPillText);
      badgeX += 12;
    }

    if (tagBadge) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge, "rgba(255,255,255,0.12)", "#FFFFFF");
    }

    const titleY = badgeY + 60;
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

    if (subtitle && curY < CANVAS_HEIGHT - 30) {
      ctx.save();
      const subSize = Math.max(26, Math.floor(titleSize * 0.40));
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
    const cardY = 54;
    const cardW = 760;
    const cardH = CANVAS_HEIGHT - 108;

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
    const badgeY = cardY + 62;
    let badgeX = startX;

    const numPadded = selectedChapterNum < 10 ? `0${selectedChapterNum}` : `${selectedChapterNum}`;
    const eyebrowText = `${selectedClass} PHYSICS • CHAPTER ${numPadded}`;

    badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, eyebrowText, colors.eyebrowBg, colors.eyebrowText);
    badgeX += 12;

    if (partNumber) {
      badgeX = drawInvertedPill(ctx, badgeX, badgeY, partNumber, colors.accentPillBg, colors.accentPillText);
      badgeX += 12;
    }

    if (tagBadge) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge, "rgba(255,255,255,0.12)", "#FFFFFF");
    }

    const titleY = badgeY + 70;
    ctx.save();
    const fontStr = getFont(titleSize, 900);
    ctx.font = fontStr;
    ctx.textBaseline = "top";
    let curY = titleY;
    const lineHeight = selectedFont === "bebas" ? titleSize * 1.02 : titleSize * 1.10;

    const lines = wrapText(ctx, mainTitle, 660, fontStr);
    lines.forEach((line) => {
      ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
      ctx.shadowBlur = 14;
      ctx.shadowOffsetY = 3;
      ctx.fillStyle = colors.title;
      ctx.fillText(line, startX, curY);
      curY += lineHeight;
    });
    ctx.restore();

    if (subtitle) {
      ctx.save();
      const subSize = Math.max(26, Math.floor(titleSize * 0.40));
      ctx.font = getFont(subSize, 700, true);
      ctx.shadowColor = "rgba(0, 0, 0, 0.90)";
      ctx.shadowBlur = 10;
      ctx.shadowOffsetY = 2;
      ctx.fillStyle = colors.sub;
      ctx.textBaseline = "top";
      const subLines = wrapText(ctx, subtitle, 660, getFont(subSize, 700, true));
      let subY = curY + 16;
      subLines.forEach((sLine) => {
        ctx.fillText(sLine, startX, subY);
        subY += subSize * 1.30;
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
    const badgeY = 120;
    let badgeX = startX;

    badgeX = drawInvertedPill(ctx, badgeX, badgeY, `${selectedClass} PHYSICS`, colors.accentPillBg, colors.accentPillText);
    badgeX += 12;

    const numPadded = selectedChapterNum < 10 ? `0${selectedChapterNum}` : `${selectedChapterNum}`;
    badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, `CH ${numPadded}`, colors.eyebrowBg, colors.eyebrowText);
    badgeX += 12;

    if (partNumber) {
      badgeX = drawEyebrowBadge(ctx, badgeX, badgeY, partNumber, "rgba(255,255,255,0.15)", "#FFFFFF");
      badgeX += 12;
    }

    if (tagBadge) {
      drawEyebrowBadge(ctx, badgeX, badgeY, tagBadge, "rgba(255,255,255,0.10)", "#FFFFFF");
    }

    const titleY = badgeY + 65;
    ctx.save();
    const fontStr = getFont(titleSize, 900);
    ctx.font = fontStr;
    ctx.textBaseline = "top";
    let curY = titleY;
    const lineHeight = selectedFont === "bebas" ? titleSize * 1.02 : titleSize * 1.10;

    const lines = wrapText(ctx, mainTitle, 680, fontStr);
    lines.forEach((line) => {
      ctx.shadowColor = "rgba(0, 0, 0, 0.95)";
      ctx.shadowBlur = 16;
      ctx.shadowOffsetY = 4;
      ctx.fillStyle = colors.title;
      ctx.fillText(line, startX, curY);
      curY += lineHeight;
    });
    ctx.restore();

    if (subtitle) {
      ctx.save();
      const subSize = Math.max(26, Math.floor(titleSize * 0.40));
      ctx.font = getFont(subSize, 700, true);
      ctx.shadowColor = "rgba(0, 0, 0, 0.90)";
      ctx.shadowBlur = 10;
      ctx.shadowOffsetY = 2;
      ctx.fillStyle = colors.sub;
      ctx.textBaseline = "top";
      const subLines = wrapText(ctx, subtitle, 680, getFont(subSize, 700, true));
      let subY = curY + 16;
      subLines.forEach((sLine) => {
        ctx.fillText(sLine, startX, subY);
        subY += subSize * 1.30;
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

    // 6. Mobile Preview Simulation
    simThumbUrl = canvasEl.toDataURL("image/jpeg", 0.70);
  }

  function downloadThumbnail() {
    if (!canvasEl) return;
    renderCanvas();
    const link = document.createElement("a");
    const safeCh = `CH${selectedChapterNum}`;
    link.download = `Dhanya_${selectedClass.replace("+", "Plus")}_${safeCh}_${Date.now()}.jpg`;
    link.href = canvasEl.toDataURL("image/jpeg", 0.95);
    link.click();
    triggerToast("Downloaded 1280 × 720 HD Thumbnail! 🎉");
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
    const _ch = selectedChapterNum;
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
    const _bg = bgImage;
    const _pge = activePage;

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

<div class="w-full max-w-full overflow-x-hidden pb-24">
  
  <!-- ========================================================
       PAGE 1: DATA INPUT & STYLING (Streamlined with Dropdowns)
       ======================================================== -->
  {#if activePage === "input"}
    <main class="flex-1 w-full max-w-3xl mx-auto p-4 sm:p-6 space-y-6">
      
      <!-- Video URL Card (No photo upload, clean URL input) -->
      <Card>
        <CardHeader>
          <div class="flex items-center justify-between">
            <CardTitle class="text-base flex items-center gap-2">
              <Video class="size-4" />
              YouTube Video Link
            </CardTitle>
            <Badge variant="secondary">Auto-Detect</Badge>
          </div>
          <CardDescription>
            Paste your YouTube video link to automatically grab the thumbnail and detect chapter details.
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          <div class="space-y-2">
            <Label for="yt-input">Video URL</Label>
            <div class="flex gap-2">
              <Input
                id="yt-input"
                bind:value={ytUrl}
                onkeydown={(e) => e.key === 'Enter' && fetchYouTubeThumbnail()}
                placeholder="https://www.youtube.com/watch?v=..."
              />
              <Button disabled={isFetching} onclick={fetchYouTubeThumbnail}>
                {#if isFetching}
                  <RefreshCw class="size-4 animate-spin mr-1.5" />
                {/if}
                Fetch Video
              </Button>
            </div>
            {#if ytStatus}
              <p class="text-xs text-muted-foreground">{ytStatus}</p>
            {/if}
          </div>

          <!-- Quick Test Shortcut for Dhanya's Chapter 5 -->
          <div class="pt-1">
            <Button
              variant="outline"
              size="sm"
              onclick={() => {
                ytUrl = "https://www.youtube.com/watch?v=c-M2jbSHhTg";
                fetchYouTubeThumbnail();
              }}
            >
              Load Sample: +1 Physics Chapter 5 Video
            </Button>
          </div>
        </CardContent>
      </Card>

      <!-- Kerala Syllabus & Chapter Details (Clean Dropdowns) -->
      <Card>
        <CardHeader>
          <div class="flex items-center justify-between">
            <CardTitle class="text-base flex items-center gap-2">
              <BookOpen class="size-4" />
              Kerala Syllabus & Chapter
            </CardTitle>
            <Button variant="outline" size="sm" onclick={toggleLanguage}>
              {isMalayalamTitle ? "English" : "മലയാളം"}
            </Button>
          </div>
          <CardDescription>
            Select class and chapter from the Kerala Higher Secondary SCERT curriculum.
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          
          <!-- Class Dropdown -->
          <div class="space-y-2">
            <Label>Higher Secondary Class</Label>
            <Select
              type="single"
              value={selectedClass}
              onValueChange={(val) => {
                if (val === "+1" || val === "+2") {
                  selectedClass = val;
                  const list = val === "+1" ? PLUS_ONE_CHAPTERS : PLUS_TWO_CHAPTERS;
                  const ch = list.find(c => c.num === selectedChapterNum) || list[0];
                  applyChapter(ch);
                }
              }}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Class" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="+1" label="Plus One (+1 Physics)">Plus One (+1 Physics)</SelectItem>
                <SelectItem value="+2" label="Plus Two (+2 Physics)">Plus Two (+2 Physics)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Chapter Dropdown -->
          <div class="space-y-2">
            <Label>Chapter</Label>
            <Select
              type="single"
              bind:value={selectedChapterStr}
              onValueChange={(val) => {
                if (!val) return;
                const ch = currentChapterList.find(c => c.num === parseInt(val, 10));
                if (ch) applyChapter(ch);
              }}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Chapter" />
              </SelectTrigger>
              <SelectContent class="max-h-72">
                <SelectGroup>
                  <SelectGroupHeading>{selectedClass === "+1" ? "+1 Physics" : "+2 Physics"}</SelectGroupHeading>
                  {#each currentChapterList as ch (ch.num)}
                    <SelectItem value={String(ch.num)} label={`Chapter ${ch.num}: ${ch.title}`}>
                      Chapter {ch.num}: {ch.title}
                    </SelectItem>
                  {/each}
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          <!-- Important Derivations Dropdown -->
          <div class="space-y-2">
            <Label>Key Derivation / Sub-Topic</Label>
            <Select
              type="single"
              value={subtitle}
              onValueChange={(val) => {
                if (val) subtitle = val;
              }}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Derivation" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectGroupHeading>Derivations for Ch {selectedChapterNum}</SelectGroupHeading>
                  {#each currentChapterObj.derivations as dev}
                    <SelectItem value={dev} label={dev}>{dev}</SelectItem>
                  {/each}
                  <SelectItem value={currentChapterObj.sub} label={currentChapterObj.sub}>{currentChapterObj.sub}</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          <!-- Video Part Dropdown -->
          <div class="space-y-2">
            <Label>Video Part / Episode</Label>
            <Select
              type="single"
              bind:value={partNumber}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Part" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="" label="Full Video / One-Shot">Full Video / One-Shot</SelectItem>
                <SelectItem value="PART 1" label="Part 1">Part 1</SelectItem>
                <SelectItem value="PART 2" label="Part 2">Part 2</SelectItem>
                <SelectItem value="PART 3" label="Part 3">Part 3</SelectItem>
                <SelectItem value="PART 4" label="Part 4">Part 4</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Focus Tag Dropdown -->
          <div class="space-y-2">
            <Label>Exam Focus Tag</Label>
            <Select
              type="single"
              bind:value={tagBadge}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Tag" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="" label="None">None</SelectItem>
                <SelectItem value="CORE DERIVATIONS" label="Core Derivations">Core Derivations</SelectItem>
                <SelectItem value="ONE SHOT REVISION" label="One Shot Revision">One Shot Revision</SelectItem>
                <SelectItem value="EXAM ESSENTIALS" label="Exam Essentials">Exam Essentials</SelectItem>
                <SelectItem value="PREVIOUS YEAR QUESTIONS" label="Previous Year Questions (PYQ)">Previous Year Questions (PYQ)</SelectItem>
                <SelectItem value="CONCEPT & PROBLEMS" label="Concept & Problems">Concept & Problems</SelectItem>
                <SelectItem value="FULL CHAPTER" label="Full Chapter">Full Chapter</SelectItem>
                <SelectItem value="FORMULA REVISION" label="Formula Revision">Formula Revision</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <Separator />

          <!-- Main Title & Subtitle Edit Inputs -->
          <div class="space-y-2">
            <Label for="main-title">Headline Text</Label>
            <Input id="main-title" bind:value={mainTitle} />
          </div>

          <div class="space-y-2">
            <Label for="sub-title">Subtitle Text</Label>
            <Input id="sub-title" bind:value={subtitle} />
          </div>

        </CardContent>
      </Card>

      <!-- Thumbnail Style & Typography (Clean Dropdowns & Sliders) -->
      <Card>
        <CardHeader>
          <CardTitle class="text-base flex items-center gap-2">
            <SlidersHorizontal class="size-4" />
            Thumbnail Style & Typography
          </CardTitle>
          <CardDescription>
            Choose designer font, layout style, and contrast palette.
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-4">
          
          <!-- Font Dropdown -->
          <div class="space-y-2">
            <Label>Designer Font Family</Label>
            <Select
              type="single"
              bind:value={selectedFont}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Font" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="inter" label="Inter (Swiss Modern Sans)">Inter (Swiss Modern Sans)</SelectItem>
                <SelectItem value="bebas" label="Bebas Neue (Bold Impact Display)">Bebas Neue (Bold Impact Display)</SelectItem>
                <SelectItem value="jakarta" label="Plus Jakarta Sans (Modern Geometric)">Plus Jakarta Sans (Modern Geometric)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Layout Dropdown -->
          <div class="space-y-2">
            <Label>Layout Structure</Label>
            <Select
              type="single"
              bind:value={layout}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Layout" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="editorial_left" label="Studio Left (Recommended - Keeps notes clear)">Studio Left (Recommended - Keeps notes clear)</SelectItem>
                <SelectItem value="horizon_bottom" label="Cinematic Horizon (Lower Third)">Cinematic Horizon (Lower Third)</SelectItem>
                <SelectItem value="frosted_card" label="Frosted Studio Card">Frosted Studio Card</SelectItem>
                <SelectItem value="swiss_poster" label="Swiss Minimal Poster">Swiss Minimal Poster</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Contrast Palette Dropdown -->
          <div class="space-y-2">
            <Label>Contrast Palette</Label>
            <Select
              type="single"
              bind:value={colorTheme}
            >
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select Palette" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="mono_pure" label="Pure Monochrome (Black & White)">Pure Monochrome (Black & White)</SelectItem>
                <SelectItem value="mono_slate" label="Studio Slate (Graphite & Crisp White)">Studio Slate (Graphite & Crisp White)</SelectItem>
                <SelectItem value="warm_editorial" label="Warm Ivory (Academic Editorial)">Warm Ivory (Academic Editorial)</SelectItem>
                <SelectItem value="subtle_amber" label="Amber Accent (Minimalist Warm)">Amber Accent (Minimalist Warm)</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Toggles -->
          <div class="flex items-center justify-between pt-1">
            <div class="space-y-0.5">
              <Label>Ghost Chapter Numeral ({selectedChapterNum})</Label>
              <p class="text-xs text-muted-foreground">Translucent stylized chapter number</p>
            </div>
            <Switch bind:checked={showWatermarkNum} />
          </div>

          <div class="flex items-center justify-between">
            <div class="space-y-0.5">
              <Label>Channel Stamp</Label>
              <p class="text-xs text-muted-foreground">Physics with Dhanya badge</p>
            </div>
            <Switch bind:checked={showChannel} />
          </div>

          <Separator />

          <!-- Headline Size Slider -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-sm">
              <Label>Headline Size</Label>
              <span class="text-xs font-mono text-muted-foreground">{titleSize}px</span>
            </div>
            <Slider
              type="single"
              bind:value={titleSize}
              min={56}
              max={96}
              step={2}
            />
          </div>

          <!-- Dimmer Slider -->
          <div class="space-y-3">
            <div class="flex items-center justify-between text-sm">
              <Label>Background Dimmer</Label>
              <span class="text-xs font-mono text-muted-foreground">{bgDarknessPercent}%</span>
            </div>
            <Slider
              type="single"
              bind:value={bgDarknessPercent}
              min={10}
              max={80}
              step={5}
            />
          </div>

        </CardContent>
      </Card>

    </main>

    <!-- Page 1 Sticky Bottom Bar: Go to Preview -->
    <div class="fixed inset-x-0 bottom-0 z-40 border-t bg-background/95 backdrop-blur px-4 py-3 w-full">
      <div class="max-w-3xl mx-auto flex justify-end w-full">
        <Button
          size="lg"
          class="w-full sm:w-auto font-semibold gap-2"
          onclick={() => {
            activePage = "preview";
            setTimeout(renderCanvas, 60);
            if (!seoData) {
              generateSeoKit();
            }
          }}
        >
          <span>NEXT</span>
          <ChevronRight class="size-4" />
        </Button>
      </div>
    </div>
  {/if}

  <!-- ========================================================
       PAGE 2: PREVIEW, DOWNLOAD & AI SEO KIT
       ======================================================== -->
  {#if activePage === "preview"}
    <main class="flex-1 w-full max-w-5xl mx-auto p-4 sm:p-6 space-y-6">
      
      <!-- Top Action Bar -->
      <div class="flex flex-wrap items-center justify-between gap-3 w-full">
        <Button
          variant="outline"
          size="sm"
          onclick={() => activePage = "input"}
          class="gap-1.5 shrink-0"
        >
          <ChevronLeft class="size-4" />
          Back to Setup
        </Button>
      </div>

      <!-- HD Canvas Preview Card -->
      <Card class="w-full overflow-hidden">
        <CardHeader class="pb-3">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <CardTitle class="text-base font-semibold">1280 × 720 HD Thumbnail</CardTitle>
            <div class="flex items-center gap-1.5 flex-wrap">
              <Badge variant="secondary">{selectedClass} Physics • Ch {selectedChapterNum}</Badge>
              {#if partNumber}
                <Badge variant="outline">{partNumber}</Badge>
              {/if}
            </div>
          </div>
          <CardDescription>
            High resolution 1280×720 export ready to publish on YouTube.
          </CardDescription>
        </CardHeader>
        <CardContent class="p-0">
          <div class="w-full aspect-video bg-black overflow-hidden relative">
            <canvas
              bind:this={canvasEl}
              width={CANVAS_WIDTH}
              height={CANVAS_HEIGHT}
              class="w-full h-full object-contain block"
            ></canvas>
          </div>
        </CardContent>
      </Card>

      <!-- YouTube Mobile Feed Simulation Card -->
      <Card>
        <CardHeader class="pb-2">
          <CardTitle class="text-xs font-semibold text-muted-foreground uppercase tracking-wider flex items-center gap-2">
            <Smartphone class="size-3.5" />
            YouTube Mobile Feed Simulation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="flex gap-3 items-center">
            <img
              src={simThumbUrl}
              alt="Preview"
              class="w-28 aspect-video object-cover rounded bg-black shrink-0 border"
            />
            <div class="min-w-0 flex-1">
              <p class="text-sm font-medium line-clamp-2 leading-snug">
                {selectedClass} PHYSICS | {mainTitle} {partNumber ? `| ${partNumber}` : ''}
              </p>
              <p class="text-xs text-muted-foreground mt-1 truncate">
                {channelName} • 3.2K views
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      <!-- AI SEO & Publishing Kit (Gemini Flash) -->
      <Card>
        <CardHeader>
          <div class="flex items-center justify-between">
            <CardTitle class="text-base flex items-center gap-2">
              <Sparkles class="size-4 text-primary" />
              AI SEO & Publishing Kit (Gemini Flash)
            </CardTitle>
            <Button
              variant="outline"
              size="sm"
              disabled={isGeneratingSeo}
              onclick={generateSeoKit}
            >
              {#if isGeneratingSeo}
                <RefreshCw class="size-3.5 animate-spin mr-1.5" />
                Generating
              {:else}
                <RefreshCw class="size-3.5 mr-1.5" />
                Regenerate
              {/if}
            </Button>
          </div>
          <CardDescription>
            Channel-consistent standardized title, Kerala SCERT SEO description, and high-CTR search tags.
          </CardDescription>
        </CardHeader>
        <CardContent class="space-y-5">
          
          {#if isGeneratingSeo}
            <div class="py-12 flex flex-col items-center justify-center text-center space-y-3">
              <RefreshCw class="size-6 animate-spin text-primary" />
              <p class="text-sm font-medium">Analyzing video & generating SEO kit...</p>
              <p class="text-xs text-muted-foreground">Extracting YouTube Malayalam speech & structuring description</p>
            </div>
          {:else if seoData}
            
            <!-- Standardized Video Title -->
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Channel-Standardized Video Title
                </Label>
                <Button variant="ghost" size="sm" class="h-7 text-xs" onclick={() => copyText(seoData!.title, "Title")}>
                  <Copy class="size-3.5 mr-1" />
                  Copy Title
                </Button>
              </div>
              <div class="p-3 bg-muted/40 rounded-md border font-medium text-sm">
                {seoData.title}
              </div>
            </div>

            <!-- YouTube SEO Description -->
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  SEO Description (Malayalam + English)
                </Label>
                <Button variant="ghost" size="sm" class="h-7 text-xs" onclick={() => copyText(seoData!.description, "Description")}>
                  <Copy class="size-3.5 mr-1" />
                  Copy Description
                </Button>
              </div>
              <div class="p-3 bg-muted/40 rounded-md border text-xs whitespace-pre-wrap max-h-56 overflow-y-auto leading-relaxed font-sans">
                {seoData.description}
              </div>
            </div>

            <!-- YouTube Search Tags -->
            <div class="space-y-2">
              <div class="flex items-center justify-between">
                <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  YouTube Search Tags
                </Label>
                <Button variant="ghost" size="sm" class="h-7 text-xs" onclick={() => copyText(seoData!.tags_string, "Tags")}>
                  <Copy class="size-3.5 mr-1" />
                  Copy All Tags
                </Button>
              </div>
              <div class="p-2.5 bg-muted/40 rounded-md border flex flex-wrap gap-1.5">
                {#each seoData.tags_string.split(", ") as tag}
                  <Badge variant="secondary" class="text-xs font-normal">{tag}</Badge>
                {/each}
              </div>
            </div>

            <!-- Malayalam Key Takeaways -->
            {#if seoData.malayalam_summary}
              <div class="space-y-2">
                <Label class="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Malayalam Study Points (മലയാളം)
                </Label>
                <div class="p-3 bg-muted/40 rounded-md border text-xs leading-relaxed">
                  {seoData.malayalam_summary}
                </div>
              </div>
            {/if}

            <!-- Autogenerated Captions / Transcript -->
            {#if seoData.has_captions}
              <div class="p-3.5 bg-muted/20 rounded-lg border flex flex-col sm:flex-row sm:items-center justify-between gap-3 w-full">
                <div class="space-y-1 min-w-0">
                  <div class="flex items-center gap-2">
                    <Badge variant="outline" class="text-[10px] px-1.5 py-0 font-medium">CC Subtitles</Badge>
                    <span class="text-xs font-medium">Spoken Malayalam Audio</span>
                  </div>
                  <p class="text-[11px] text-muted-foreground">Autogenerated Malayalam speech audio transcript</p>
                </div>
                <div class="flex items-center gap-2 shrink-0">
                  <Button variant="outline" size="sm" class="h-8 text-xs flex-1 sm:flex-initial" onclick={() => copyText(seoData!.captions_text, "Captions")}>
                    <Copy class="size-3.5 mr-1" />
                    Copy
                  </Button>
                  <Button variant="secondary" size="sm" class="h-8 text-xs flex-1 sm:flex-initial" href={`${API_BASE}/api/download-captions?video_id=${ytUrl || "c-M2jbSHhTg"}`} target="_blank">
                    <Download class="size-3.5 mr-1" />
                    Download .txt
                  </Button>
                </div>
              </div>
            {/if}

          {:else}
            <div class="py-8 text-center space-y-2">
              <p class="text-sm text-muted-foreground">Click below to generate SEO description and tags.</p>
              <Button onclick={generateSeoKit}>
                <Sparkles class="size-4 mr-2" />
                Generate AI SEO Kit
              </Button>
            </div>
          {/if}

        </CardContent>
      </Card>

    </main>

    <!-- Page 2 Sticky Bottom Bar -->
    <div class="fixed inset-x-0 bottom-0 z-40 border-t bg-background/95 backdrop-blur px-4 py-3 w-full">
      <div class="max-w-5xl mx-auto flex items-center justify-between gap-3 w-full">
        <Button
          variant="outline"
          size="lg"
          onclick={() => activePage = "input"}
          class="gap-1.5 shrink-0"
        >
          <ChevronLeft class="size-4" />
          <span>Setup</span>
        </Button>

        <div class="flex items-center gap-2">
          <Button variant="outline" size="lg" onclick={copyToClipboard} class="font-semibold gap-2">
            <Copy class="size-4" />
            <span>Copy Image</span>
          </Button>
          <Button
            size="lg"
            class="font-semibold gap-2"
            onclick={downloadThumbnail}
          >
            <Download class="size-4" />
            <span>Download HD (1280×720)</span>
          </Button>
        </div>
      </div>
    </div>
  {/if}

  <!-- Toast Notification -->
  {#if showToast}
    <div class="fixed top-16 right-6 z-50 bg-foreground text-background font-medium text-xs py-2 px-3.5 rounded-md shadow-lg flex items-center gap-2 animate-in fade-in duration-150">
      <Check class="size-3.5" />
      <span>{toastMessage}</span>
    </div>
  {/if}

</div>
