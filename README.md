# PHYSICS With Dhanya — YouTube Thumbnail Studio

An intuitive, modern web application built with **FastAPI** (`uv`) and **shadcn-svelte** (Svelte 5 + Tailwind CSS v4 + Bits UI). Designed specifically for **Dhanya Teacher** ("PHYSICS With Dhanya") to effortlessly create eye-catching, high-contrast, mobile-readable YouTube thumbnails (1280 × 720) for Kerala Higher Secondary (+1 & +2) Physics students.

---

## 🌟 Key Features

1. **Modern shadcn-svelte UI:**
   - Powered by **shadcn-svelte (Nova style)**, Bits UI, and Lucide icons.
   - Clean dark-mode theme designed for effortless, distraction-free creation.
2. **Direct YouTube Integration:**
   - Paste any video link (e.g. `https://www.youtube.com/watch?v=c-M2jbSHhTg`).
   - Automatically extracts the highest resolution (1280x720) video frame.
   - Auto-detects the syllabus class (`+1 PHYSICS` or `+2 PHYSICS`) and chapter title.
3. **Built for Mobile Readability:**
   - High-contrast text outline + drop shadow.
   - Dark gradient and vignette filters so whiteboard/blackboard chalk handwriting remains visible on the side while text pops out clearly.
   - Real-world **YouTube Mobile Feed Simulator** to verify thumbnail readability on student phones before downloading.
4. **Bilingual Malayalam + English Typography:**
   - Bundled with Google's **Noto Sans Malayalam**, **Manjari**, **Montserrat**, and **Bebas Neue**.
   - Supports Malayalam (e.g. *പ്ലസ് വൺ ഫിസിക്സ്*) and English derivations seamlessly.
5. **1-Click Class & Tag Presets:**
   - Class toggles: `+1 PHYSICS` (Royal Blue) & `+2 PHYSICS` (Crimson / Violet).
   - Instant tags: `ONE SHOT REVISION`, `SURE QUESTIONS`, `CHAPTER DERIVATIONS`, `PYQ 2024`, `EXAM SPECIAL`, `PART 1`, `PART 2`.
6. **Instant HD 1280x720 Export:**
   - 1-click download as YouTube-ready 1280 × 720 JPEG.
   - 1-click copy to clipboard.

---

## 🚀 How to Run

### 1. Python Backend (FastAPI + uv)
Start the backend server (which serves both the API and the compiled shadcn-svelte frontend):
```bash
uv run uvicorn amma_yt.server:app --host 0.0.0.0 --port 8000 --reload
```
Open **`http://localhost:8000`** in your browser.

### 2. Frontend Development (SvelteKit + Vite)
If you want to edit the Svelte frontend with hot-module replacement (HMR):
```bash
cd frontend
npm run dev
```
And to rebuild static files into `static/`:
```bash
cd frontend
npm run build
```
