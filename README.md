# 🎬 Video Downloader (Python + CustomTkinter)

A clean, fast, and stable desktop application to download YouTube videos or audio using **yt-dlp**, built with **Python** and **CustomTkinter**.

---

## ✨ Features

- 📹 Download videos in MP4 (360p–4K)
- 🎧 Download audio in MP3 (128–320 kbps)
- 📊 Real-time progress bar
- ❌ Cancel download anytime
- 🧠 Thread-safe UI (no freezing)
- 🪟 Safe window close during download
- 🧹 Windows-safe filenames
- 🔒 No playlists (single video only)

---

## 🛠️ Tech Stack

- Python 3.9+
- CustomTkinter
- yt-dlp
- FFmpeg (required for MP3 downloads)

---

## 📦 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/ra5533/video-downloader.git
cd video-downloader
```

### 2️⃣ Create virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Install FFmpeg (for MP3)
- Download from: https://ffmpeg.org/download.html
- Add FFmpeg to system PATH

---

## ▶️ Run the App
```bash
python src/app.py
```

---

## ⚠️ Notes & Design Decisions

- URL validation is handled internally by **yt-dlp**
- Hard subprocess killing is avoided for safety
- Download resume is not supported by design

These are **intentional trade-offs**, not bugs.

---

## 📜 License

MIT License
