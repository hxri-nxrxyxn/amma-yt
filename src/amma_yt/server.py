import io
import re
from pathlib import Path
from typing import Optional

import httpx
from fastapi import FastAPI, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "static"
FONTS_DIR = STATIC_DIR / "fonts"
SAMPLES_DIR = STATIC_DIR / "samples"

app = FastAPI(title="PHYSICS With Dhanya - Thumbnail Studio")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/api/youtube-info")
async def get_youtube_info(url: str = Query(..., description="YouTube video URL or ID")):
    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL or Video ID")

    # Fetch oEmbed data for title and author
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    title = ""
    author = "PHYSICS With Dhanya"
    
    async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
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

    # Heuristic parsing for class and chapter from title
    detected_class = None
    title_lower = title.lower()
    if "+1" in title or "plus one" in title_lower or "class 11" in title_lower:
        detected_class = "+1 PHYSICS"
    elif "+2" in title or "plus two" in title_lower or "class 12" in title_lower:
        detected_class = "+2 PHYSICS"

    # Extract chapter number and part if available
    detected_chapter = ""
    detected_chapter_num = None
    ch_match = re.search(r"(?:chapter|ch|unit)\s*[:.-]?\s*(\d+)", title, re.IGNORECASE)
    if ch_match:
        detected_chapter_num = int(ch_match.group(1))
        detected_chapter = f"CHAPTER {detected_chapter_num}"
    
    detected_part = ""
    part_match = re.search(r"(?:part|ep|episode)\s*[:.-]?\s*(\d+)", title, re.IGNORECASE)
    if part_match:
        detected_part = f"PART {part_match.group(1)}"

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
        "detected_part": detected_part,
    }

@app.get("/api/proxy-thumbnail")
async def proxy_thumbnail(id: str = Query(..., description="YouTube video ID")):
    video_id = extract_video_id(id)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid Video ID")

    maxres_url = f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"
    sd_url = f"https://i.ytimg.com/vi/{video_id}/sddefault.jpg"
    hq_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"

    async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as client:
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
    api_key: Optional[str] = "AIzaSyBv-L_oHiaW3kwrGwslTU1cK-1US8miV40"

@app.post("/api/generate-seo")
async def generate_seo(req: SeoRequest):
    video_id = extract_video_id(req.video_id) or req.video_id
    api_key = req.api_key or "AIzaSyBv-L_oHiaW3kwrGwslTU1cK-1US8miV40"
    
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
