import io
import json
import os
import re
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
STATIC_DIR = BASE_DIR / "static"
FONTS_DIR = STATIC_DIR / "fonts"
SAMPLES_DIR = STATIC_DIR / "samples"

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

app = FastAPI(title="PHYSICS With Dhanya - Thumbnail Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PLUS_ONE_CHAPTERS = [
    {"num": 1, "title": "UNITS & MEASUREMENTS", "sub": "Dimensional Analysis & Errors", "malayalam": "യൂണിറ്റുകളും അളവുകളും", "derivations": ["Dimensional Analysis", "Error Analysis & Significant Figures"], "keywords": ["unit", "measurement", "dimension", "error"]},
    {"num": 2, "title": "MOTION IN A STRAIGHT LINE", "sub": "Equations of Motion & Graphs", "malayalam": "നേർരേഖാ ചലനം", "derivations": ["Equations of Motion (v = u + at, s = ut + ½at²)", "Relative Velocity & Velocity-Time Graphs"], "keywords": ["straight line", "equations of motion", "velocity"]},
    {"num": 3, "title": "MOTION IN A PLANE", "sub": "Projectile Motion & Vectors", "malayalam": "ഒരു പ്രതലത്തിലെ ചലനം", "derivations": ["Trajectory of Projectile & Max Height", "Horizontal Range & Centripetal Acceleration"], "keywords": ["plane", "projectile", "vector", "trajectory"]},
    {"num": 4, "title": "LAWS OF MOTION", "sub": "Newton's Laws & Friction", "malayalam": "ചലന നിയമങ്ങൾ", "derivations": ["Banking of Roads (Friction & Angle)", "Conservation of Linear Momentum & Recoil"], "keywords": ["laws of motion", "newton", "banking of road", "friction"]},
    {"num": 5, "title": "WORK, ENERGY & POWER", "sub": "Work-Energy Theorem & Collisions", "malayalam": "പ്രവൃത്തി, ഊർജ്ജം, പവർ", "derivations": ["Work-Energy Theorem Derivation", "Elastic Collision in One Dimension"], "keywords": ["work", "energy", "power", "work-energy", "collision"]},
    {"num": 6, "title": "SYSTEM OF PARTICLES & ROTATION", "sub": "Moment of Inertia & Torque", "malayalam": "ഭ്രമണചലനവും കണികകളും", "derivations": ["Parallel & Perpendicular Axes Theorems", "Torque = Iα & Angular Momentum Conservation"], "keywords": ["particles", "rotation", "moment of inertia", "torque"]},
    {"num": 7, "title": "GRAVITATION", "sub": "Kepler's Laws & Escape Speed", "malayalam": "ഗുരുത്വാകർഷണം", "derivations": ["Acceleration due to Gravity at Height & Depth", "Escape Speed & Orbital Velocity Derivations"], "keywords": ["gravitation", "kepler", "escape speed", "orbital"]},
    {"num": 8, "title": "MECHANICAL PROPERTIES OF SOLIDS", "sub": "Hooke's Law & Stress-Strain", "malayalam": "ഖരവസ്തുക്കളുടെ ഗുണങ്ങൾ", "derivations": ["Stress-Strain Curve & Young's Modulus", "Elastic Potential Energy in a Stretched Wire"], "keywords": ["solids", "hooke", "stress", "strain", "modulus", "elasticity"]},
    {"num": 9, "title": "MECHANICAL PROPERTIES OF FLUIDS", "sub": "Bernoulli's Theorem & Viscosity", "malayalam": "ദ്രാവകങ്ങളുടെ ഗുണങ്ങൾ", "derivations": ["Bernoulli's Principle & Applications", "Terminal Velocity (Stokes' Law) & Surface Tension"], "keywords": ["fluids", "bernoulli", "viscosity", "surface tension", "stokes"]},
    {"num": 10, "title": "THERMAL PROPERTIES OF MATTER", "sub": "Calorimetry & Heat Transfer", "malayalam": "ദ്രവ്യത്തിന്റെ താപഗുണങ്ങൾ", "derivations": ["Newton's Law of Cooling", "Specific Heat Capacity & Thermal Conductivity"], "keywords": ["thermal", "calorimetry", "cooling", "heat transfer"]},
    {"num": 11, "title": "THERMODYNAMICS", "sub": "First Law & Heat Engines", "malayalam": "തെർമോഡൈനാമിക്സ്", "derivations": ["Mayer's Relation (Cp - Cv = R)", "Carnot Engine & Efficiency (η = 1 - T2/T1)"], "keywords": ["thermodynamics", "carnot", "mayer", "entropy"]},
    {"num": 12, "title": "KINETIC THEORY", "sub": "Ideal Gas Laws & Equipartition", "malayalam": "കൈനറ്റിക് തിയറി", "derivations": ["Pressure Expression for Ideal Gas (P = ⅓ρv²)", "Degrees of Freedom & Law of Equipartition"], "keywords": ["kinetic theory", "ideal gas", "equipartition"]},
    {"num": 13, "title": "OSCILLATIONS", "sub": "Simple Harmonic Motion (SHM)", "malayalam": "ആന്ദോളനങ്ങൾ", "derivations": ["Time Period of Simple Pendulum (T = 2π√(l/g))", "Kinetic & Potential Energy in SHM"], "keywords": ["oscillation", "shm", "simple pendulum", "harmonic"]},
    {"num": 14, "title": "WAVES", "sub": "Standing Waves & Beats", "malayalam": "തരംഗങ്ങൾ", "derivations": ["Modes of Vibration in Organ Pipes", "Beats Frequency & Doppler Effect"], "keywords": ["waves", "organ pipe", "beats", "doppler"]}
]

PLUS_TWO_CHAPTERS = [
    {"num": 1, "title": "ELECTRIC CHARGES & FIELDS", "sub": "Gauss's Law & Dipole Field", "malayalam": "വൈദ്യുത ചാർജ്ജുകളും മണ്ഡലങ്ങളും", "derivations": ["Gauss's Law (Line, Plane Sheet, Shell)", "Electric Field due to Dipole (Axial & Equatorial)"], "keywords": ["charges", "fields", "gauss", "dipole"]},
    {"num": 2, "title": "ELECTROSTATIC POTENTIAL & CAPACITANCE", "sub": "Capacitors & Potential", "malayalam": "പൊട്ടൻഷ്യലും കപ്പാസിറ്റൻസും", "derivations": ["Parallel Plate Capacitor with Dielectric", "Energy Stored in Capacitor (U = ½CV²)"], "keywords": ["potential", "capacitance", "capacitor"]},
    {"num": 3, "title": "CURRENT ELECTRICITY", "sub": "Kirchhoff's Rules & Wheatstone Bridge", "malayalam": "കറന്റ് ഇലക്ട്രിസിറ്റി", "derivations": ["Drift Velocity & Ohm's Law Relation", "Wheatstone Bridge Principle (P/Q = R/S)"], "keywords": ["current electricity", "kirchhoff", "wheatstone", "drift velocity"]},
    {"num": 4, "title": "MOVING CHARGES & MAGNETISM", "sub": "Biot-Savart Law & Ampere's Law", "malayalam": "ചലിക്കുന്ന ചാർജ്ജുകളും കാന്തികതയും", "derivations": ["Magnetic Field on Axis of Circular Loop", "Ampere's Circuital Law & Solenoid / Toroid"], "keywords": ["moving charges", "magnetism", "biot savart", "ampere", "solenoid"]},
    {"num": 5, "title": "MAGNETISM & MATTER", "sub": "Bar Magnet & Magnetic Materials", "malayalam": "കാന്തികതയും പദാർത്ഥങ്ങളും", "derivations": ["Magnetic Dipole Moment & Earth's Magnetism", "Dia, Para & Ferromagnetic Properties"], "keywords": ["magnetism and matter", "bar magnet", "dia para ferro"]},
    {"num": 6, "title": "ELECTROMAGNETIC INDUCTION", "sub": "Faraday's Law & Lenz's Law", "malayalam": "വൈദ്യുതകാന്തിക പ്രേരണം", "derivations": ["Motional EMF (e = Blv)", "Self & Mutual Inductance Derivations"], "keywords": ["induction", "faraday", "lenz", "motional emf", "inductance"]},
    {"num": 7, "title": "ALTERNATING CURRENT", "sub": "LCR Series Circuit & Transformer", "malayalam": "ആൾട്ടർനേറ്റിങ് കറന്റ്", "derivations": ["LCR Series Resonance & Impedance (Z)", "Transformer Principle & Power Factor"], "keywords": ["alternating current", "lcr", "transformer", "resonance"]},
    {"num": 8, "title": "ELECTROMAGNETIC WAVES", "sub": "Displacement Current & Spectrum", "malayalam": "വൈദ്യുതകാന്തിക തരംഗങ്ങൾ", "derivations": ["Displacement Current Concept", "Electromagnetic Spectrum Frequencies & Uses"], "keywords": ["electromagnetic waves", "displacement current", "em waves"]},
    {"num": 9, "title": "RAY OPTICS & INSTRUMENTS", "sub": "Refraction, Prism & Lens Formula", "malayalam": "കിരണ ഒപ്റ്റിക്സും ഉപകരണങ്ങളും", "derivations": ["Lens Maker's Formula Derivation", "Refraction through Prism (Prism Formula)"], "keywords": ["ray optics", "lens maker", "prism", "refraction"]},
    {"num": 10, "title": "WAVE OPTICS", "sub": "Huygens' Principle & Interference", "malayalam": "തരംഗ ഒപ്റ്റിക്സ്", "derivations": ["Young's Double Slit Fringe Width (β = λD/d)", "Huygens' Principle Laws of Reflection & Refraction"], "keywords": ["wave optics", "young", "double slit", "fringe width", "huygen", "diffraction"]},
    {"num": 11, "title": "DUAL NATURE OF RADIATION", "sub": "Photoelectric Effect & de Broglie", "malayalam": "വികിരണ-പദാർത്ഥ ഇരട്ടസ്വഭാവം", "derivations": ["Einstein's Photoelectric Equation", "de Broglie Wavelength of Electron (λ = h/p)"], "keywords": ["dual nature", "photoelectric", "de broglie", "einstein"]},
    {"num": 12, "title": "ATOMS", "sub": "Bohr's Model & Energy Levels", "malayalam": "ആറ്റങ്ങൾ", "derivations": ["Radius of nth Bohr Orbit & Electron Energy", "Hydrogen Emission Spectrum (Lyman, Balmer)"], "keywords": ["atoms", "bohr", "hydrogen spectrum", "energy levels"]},
    {"num": 13, "title": "NUCLEI", "sub": "Binding Energy & Nuclear Reactions", "malayalam": "ന്യൂക്ലിയസ്സുകൾ", "derivations": ["Mass Defect & Binding Energy per Nucleon", "Nuclear Fission & Fusion Energy"], "keywords": ["nuclei", "binding energy", "mass defect", "fission", "fusion"]},
    {"num": 14, "title": "SEMICONDUCTOR ELECTRONICS", "sub": "PN Junction & Rectifiers", "malayalam": "അർദ്ധചാലക ഇലക്ട്രോണിക്സ്", "derivations": ["Half-Wave & Full-Wave Rectifier Circuits", "Energy Bands & V-I Characteristics"], "keywords": ["semiconductor", "pn junction", "rectifier", "transistor", "logic gates"]}
]

def extract_video_id(url_or_id: str) -> Optional[str]:
    """Extract 11-char YouTube video ID from various URL formats or plain ID."""
    url_or_id = url_or_id.strip()
    if re.fullmatch(r"[a-zA-Z0-9_-]{11}", url_or_id):
        return url_or_id

    patterns = [
        r"(?:v=|\/v\/|youtu\.be\/|\/embed\/|\/shorts\/|\/live\/)([a-zA-Z0-9_-]{11})",
        r"[?&]v=([a-zA-Z0-9_-]{11})",
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None

def heuristic_match_chapter(title: str, class_name: Optional[str] = None):
    """Match chapter details from title using syllabus knowledge base."""
    title_lower = title.lower()
    ch_list = PLUS_TWO_CHAPTERS if class_name == "+2 PHYSICS" else PLUS_ONE_CHAPTERS
    
    # Try chapter number first
    ch_match = re.search(r"(?:chapter|ch|unit)\s*[:.-]?\s*(\d+)", title, re.IGNORECASE)
    if ch_match:
        ch_num = int(ch_match.group(1))
        for c in ch_list:
            if c["num"] == ch_num:
                return c

    # Try keyword matching across chapters
    for c in ch_list:
        for kw in c["keywords"]:
            if kw in title_lower:
                return c

    # Try other class if not found
    other_list = PLUS_ONE_CHAPTERS if class_name == "+2 PHYSICS" else PLUS_TWO_CHAPTERS
    for c in other_list:
        for kw in c["keywords"]:
            if kw in title_lower:
                return c

    return None

@app.get("/api/youtube-info")
async def get_youtube_info(
    url: str = Query(..., description="YouTube video URL or ID"),
    api_key: Optional[str] = Query(None, description="Optional Gemini API key")
):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL or Video ID")

    # Fetch oEmbed data for title and author
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    title = ""
    author = "PHYSICS With Dhanya"
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers=DEFAULT_HEADERS) as client:
        try:
            oembed_resp = await client.get(oembed_url)
            if oembed_resp.status_code == 200:
                data = oembed_resp.json()
                title = data.get("title", "")
                author = data.get("author_name", author).strip()
        except Exception:
            pass

        # Check thumbnail availability (maxresdefault vs hqdefault)
        maxres_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
        hq_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        
        has_maxres = False
        try:
            head_resp = await client.head(maxres_url)
            content_length = int(head_resp.headers.get("content-length", 0))
            if head_resp.status_code == 200 and content_length > 2000:
                has_maxres = True
            elif head_resp.status_code != 200:
                has_maxres = False
            else:
                has_maxres = True
        except Exception:
            has_maxres = False

    # 1. Base heuristic detection
    title_lower = title.lower()
    detected_class = "+1 PHYSICS"
    if "+2" in title or "plus two" in title_lower or "class 12" in title_lower:
        detected_class = "+2 PHYSICS"
    elif "+1" in title or "plus one" in title_lower or "class 11" in title_lower:
        detected_class = "+1 PHYSICS"

    matched_ch = heuristic_match_chapter(title, detected_class)
    
    detected_chapter_num = matched_ch["num"] if matched_ch else None
    if not detected_chapter_num:
        ch_match = re.search(r"(?:chapter|ch|unit)\s*[:.-]?\s*(\d+)", title, re.IGNORECASE)
        if ch_match:
            detected_chapter_num = int(ch_match.group(1))

    detected_chapter = f"CH {detected_chapter_num:02d}" if detected_chapter_num else "CH 01"
    
    # Part detection
    detected_part = ""
    part_match = re.search(r"(?:part|ep|episode)\s*[:.-]?\s*(\d+)", title, re.IGNORECASE)
    if part_match:
        detected_part = f"PART {part_match.group(1)}"

    # Headline and Subtitle defaults
    if matched_ch:
        detected_headline = matched_ch["title"]
        detected_subtitle = matched_ch["derivations"][0] if matched_ch.get("derivations") else matched_ch["sub"]
        detected_malayalam = matched_ch.get("malayalam", "")
    else:
        # Clean title for headline
        clean_t = re.sub(r"(?i)\b(plus one|plus two|\+1|\+2|physics with dhanya|chapter \d+|part \d+|malayalam|kerala syllabus)\b", "", title)
        clean_t = re.sub(r"[|:–—\-]+", " ", clean_t).strip()
        detected_headline = " ".join(clean_t.split()[:5]).upper() or "PHYSICS"
        detected_subtitle = "Important Concepts & Derivations"
        detected_malayalam = ""

    detected_tag = "CORE DERIVATIONS"
    if "one shot" in title_lower or "revision" in title_lower:
        detected_tag = "ONE SHOT REVISION"
    elif "pyq" in title_lower or "previous year" in title_lower:
        detected_tag = "PREVIOUS YEAR QUESTIONS"
    elif "exam" in title_lower or "special" in title_lower:
        detected_tag = "EXAM ESSENTIALS"

    clean_key = api_key if isinstance(api_key, str) else None
    effective_api_key = clean_key or os.environ.get("GEMINI_API_KEY", "")
    ai_enhanced = False

    # 2. If Gemini API key is available, use Gemini Flash to create high-CTR thumbnail fields
    if effective_api_key and effective_api_key.strip():
        try:
            prompt = f"""
You are an expert YouTube Thumbnail specialist for a Kerala Higher Secondary (+1 & +2) Physics teacher channel: "PHYSICS With Dhanya".
Analyze this YouTube video:
Title: "{title}"
Teacher/Channel: "{author}"

Generate structured JSON with concise, punchy text formatted specifically for high-contrast YouTube thumbnails (max 3-5 bold words for headline):
{{
  "class_name": "{detected_class}",
  "chapter_badge": "{detected_chapter}",
  "chapter_num": {detected_chapter_num or 1},
  "headline": "SHORT PUNCHY THUMBNAIL HEADLINE IN ALL CAPS (max 3-5 words, e.g. WORK, ENERGY & POWER or LAWS OF MOTION)",
  "subtitle": "Key derivation or specific focus topic in title case (max 6-8 words)",
  "part": "{detected_part}",
  "tag": "{detected_tag}",
  "malayalam_headline": "Malayalam topic title"
}}
Return only valid JSON matching these keys.
"""
            url_gemini = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={effective_api_key.strip()}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"response_mime_type": "application/json"}
            }
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.post(url_gemini, json=payload)
                if resp.status_code == 200:
                    ai_json = json.loads(resp.json()["candidates"][0]["content"]["parts"][0]["text"])
                    detected_class = ai_json.get("class_name", detected_class)
                    detected_chapter = ai_json.get("chapter_badge", detected_chapter)
                    detected_chapter_num = ai_json.get("chapter_num", detected_chapter_num)
                    detected_headline = ai_json.get("headline", detected_headline)
                    detected_subtitle = ai_json.get("subtitle", detected_subtitle)
                    detected_part = ai_json.get("part", detected_part)
                    detected_tag = ai_json.get("tag", detected_tag)
                    detected_malayalam = ai_json.get("malayalam_headline", detected_malayalam)
                    ai_enhanced = True
        except Exception as e:
            print(f"Gemini thumbnail extraction notice (using fallback): {e}")

    return {
        "video_id": video_id,
        "title": title,
        "author": author,
        "has_maxres": has_maxres,
        "thumbnail_url": f"/api/proxy-thumbnail?id={video_id}",
        "raw_thumbnail_url": maxres_url if has_maxres else hq_url,
        "detected_class": detected_class,
        "detected_chapter": detected_chapter,
        "detected_chapter_num": detected_chapter_num,
        "detected_headline": detected_headline,
        "detected_subtitle": detected_subtitle,
        "detected_part": detected_part,
        "detected_tag": detected_tag,
        "detected_malayalam": detected_malayalam,
        "ai_enhanced": ai_enhanced
    }

@app.get("/api/proxy-thumbnail")
async def proxy_thumbnail(id: str = Query(..., description="YouTube video ID")):
    video_id = extract_video_id(id)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid Video ID")

    maxres_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    sd_url = f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg"
    hq_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True, headers=DEFAULT_HEADERS) as client:
        for url in [maxres_url, sd_url, hq_url]:
            try:
                resp = await client.get(url)
                if resp.status_code == 200 and len(resp.content) > 2000:
                    return Response(
                        content=resp.content,
                        media_type="image/jpeg",
                        headers={
                            "Cache-Control": "public, max-age=86400",
                            "Access-Control-Allow-Origin": "*",
                        },
                    )
            except Exception:
                continue

    raise HTTPException(status_code=404, detail="Thumbnail not found")

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    """Accept an uploaded image and return it resized/cropped to 1280x720."""
    contents = await file.read()
    try:
        img = Image.open(io.BytesIO(contents))
        img = img.convert("RGB")
        target_w, target_h = 1280, 720
        img_ratio = img.width / img.height
        target_ratio = target_w / target_h

        if abs(img_ratio - target_ratio) > 0.01:
            if img_ratio > target_ratio:
                new_w = int(img.height * target_ratio)
                left = (img.width - new_w) // 2
                img = img.crop((left, 0, left + new_w, img.height))
            else:
                new_h = int(img.width / target_ratio)
                top = (img.height - new_h) // 2
                img = img.crop((0, top, img.width, top + new_h))

        img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
        out_buf = io.BytesIO()
        img.save(out_buf, format="JPEG", quality=95)
        return Response(
            content=out_buf.getvalue(),
            media_type="image/jpeg",
            headers={"Access-Control-Allow-Origin": "*"},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

@app.get("/api/samples")
def list_samples():
    return {
        "boat": "/static/samples/boat.jpg",
        "video_frame": "/static/samples/video_frame.jpg",
    }

class SeoRequest(BaseModel):
    video_id: str
    class_name: str
    chapter_num: int
    chapter_title: str
    focus_topic: Optional[str] = ""
    part: Optional[str] = ""
    malayalam_title: Optional[str] = ""
    api_key: Optional[str] = None

@app.post("/api/generate-seo")
async def generate_seo(req: SeoRequest):
    video_id = extract_video_id(req.video_id) or req.video_id
    api_key = req.api_key or os.environ.get("GEMINI_API_KEY", "")
    
    # 1. Fetch autogenerated captions if available
    transcript_text = ""
    has_captions = False
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        t_list = api.list(video_id)
        # Prefer Malayalam, then English, or any available
        transcript_obj = None
        for lang in ["ml", "en"]:
            try:
                transcript_obj = t_list.find_transcript([lang])
                if transcript_obj:
                    break
            except Exception:
                continue
        if not transcript_obj and t_list:
            transcript_obj = next(iter(t_list), None)
            
        if transcript_obj:
            snippets = transcript_obj.fetch()
            transcript_text = " ".join(s.text for s in snippets)
            has_captions = True
    except Exception as e:
        print(f"Transcript lookup notice: {e}")

    # Standardized Title Rule for Channel Consistency
    class_label = f"{req.class_name} Physics" if not req.class_name.lower().endswith("physics") else req.class_name
    part_label = f"| {req.part.strip()}" if req.part.strip() else ""
    topic_label = f"| {req.focus_topic.strip()}" if req.focus_topic.strip() else ""
    
    fallback_title = f"{class_label} Chapter {req.chapter_num} | {req.chapter_title} {topic_label} {part_label} | Physics with Dhanya"
    fallback_title = " ".join(fallback_title.split())

    # 2. Prompt Gemini 2.5 Flash for SEO Kit
    sample_speech = transcript_text[:1200] if transcript_text else "No auto-generated captions found."
    prompt = f"""
You are an expert YouTube SEO specialist for an individual Kerala Higher Secondary (+1 & +2) Physics teacher channel: "PHYSICS With Dhanya".
The teacher is Dhanya, teaching Kerala SCERT / NCERT state board physics syllabus in Malayalam & English.

Video Details:
- Class: {req.class_name} PHYSICS
- Chapter: Chapter {req.chapter_num} - {req.chapter_title} ({req.malayalam_title or ''})
- Key Focus / Derivation: {req.focus_topic or 'Core Concepts & Exam Essentials'}
- Video Part: {req.part or 'Full Video'}
- Audio Transcript Snippet (what she taught): "{sample_speech}"

Generate a structured JSON output with:
1. "standard_title": Follow channel pattern: "{class_label} Chapter {req.chapter_num} | {req.chapter_title} {topic_label} {part_label} | Physics with Dhanya" (clean, no unnecessary emojis, strictly professional and uniform for the channel).
2. "seo_description": A friendly, well-structured YouTube description written in a helpful Malayalam + English mix tailored for Kerala Higher Secondary exam students. Include:
   - Warm welcome to PHYSICS With Dhanya channel.
   - Summary of topics and derivations covered in this session.
   - Mention that notes & derivations follow Kerala State Board / NCERT syllabus.
   - Suggested Timestamps outline (e.g. 00:00 - Introduction, 01:30 - Core Concept, etc.).
   - Standard channel playlist/subscribe links placeholder.
   - 4 to 6 relevant hashtags at the bottom (e.g. #PlusOnePhysics #KeralaSyllabus #PhysicsWithDhanya).
3. "tags": An array of 15 targeted, high-CTR YouTube search tags that Kerala students search on YouTube before model and board exams (e.g. "plus one physics chapter {req.chapter_num}", "work energy power kerala syllabus", "physics with dhanya", "kerala hss physics focus area", "important physics derivations").
4. "malayalam_summary": A concise 3-4 bullet point summary in Malayalam of the key exam takeaways from this class.

Return valid JSON strictly matching these keys.
"""
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json"
            }
        }
        async with httpx.AsyncClient(timeout=25.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                result_json = resp.json()
                raw_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
                import json
                ai_data = json.loads(raw_text)
                tags_list = ai_data.get("tags", [])
                return {
                    "success": True,
                    "title": ai_data.get("standard_title", fallback_title),
                    "description": ai_data.get("seo_description", ""),
                    "tags": tags_list,
                    "tags_string": ", ".join(tags_list),
                    "malayalam_summary": ai_data.get("malayalam_summary", ""),
                    "has_captions": has_captions,
                    "captions_text": transcript_text
                }
    except Exception as err:
        print(f"Gemini API error: {err}")

    # Fallback if AI or Network fails
    default_tags = [
        f"{req.class_name} physics",
        f"chapter {req.chapter_num} physics",
        req.chapter_title.lower(),
        "physics with dhanya",
        "kerala syllabus physics",
        "plus one physics kerala",
        "hss physics classes",
        "important physics derivations"
    ]
    return {
        "success": False,
        "title": fallback_title,
        "description": f"Welcome to PHYSICS With Dhanya!\n\nIn this video, we cover {req.class_name} Physics Chapter {req.chapter_num}: {req.chapter_title}.\nFocus: {req.focus_topic or 'Important concepts and derivations'}.\n\n#KeralaSyllabus #PhysicsWithDhanya #{req.class_name.replace('+', 'Plus')}Physics",
        "tags": default_tags,
        "tags_string": ", ".join(default_tags),
        "malayalam_summary": f"ചാപ്റ്റർ {req.chapter_num} ({req.chapter_title}) പ്രധാന ആശയങ്ങളും ഫോർമുലകളും.",
        "has_captions": has_captions,
        "captions_text": transcript_text
    }

@app.get("/api/download-captions")
async def download_captions(video_id: str = Query(..., description="YouTube video ID")):
    clean_id = extract_video_id(video_id) or video_id
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        t_list = api.list(clean_id)
        transcript_obj = None
        for lang in ["ml", "en"]:
            try:
                transcript_obj = t_list.find_transcript([lang])
                if transcript_obj:
                    break
            except Exception:
                continue
        if not transcript_obj and t_list:
            transcript_obj = next(iter(t_list), None)

        if transcript_obj:
            snippets = transcript_obj.fetch()
            formatted = []
            for s in snippets:
                mins = int(s.start // 60)
                secs = int(s.start % 60)
                formatted.append(f"[{mins:02d}:{secs:02d}] {s.text}")
            content = "\n".join(formatted)
            return Response(
                content=content,
                media_type="text/plain; charset=utf-8",
                headers={
                    "Content-Disposition": f"attachment; filename=Captions_{clean_id}.txt"
                }
            )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Captions not available: {e}")

    raise HTTPException(status_code=404, detail="Captions not found")

# Mount static assets for SvelteKit SPA
app.mount("/_app", StaticFiles(directory=str(STATIC_DIR / "_app")), name="_app")
app.mount("/fonts", StaticFiles(directory=str(STATIC_DIR / "fonts")), name="fonts")
app.mount("/samples", StaticFiles(directory=str(STATIC_DIR / "samples")), name="samples")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Thumbnail Studio is initializing...</h1>")

def start():
    import uvicorn
    uvicorn.run("amma_yt.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
