import customtkinter as ctk
from tkinter import filedialog
import threading
import yt_dlp
from yt_dlp.utils import DownloadError
import os
import shutil

# ------------------ App Setup ------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("YouTube Video Downloader")
app.geometry("520x560")
app.resizable(False, False)

# ------------------ Control Flags ------------------
cancel_download = False
current_ydl = None

# ------------------ Main Frame ------------------
main_frame = ctk.CTkFrame(app, corner_radius=15)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# ------------------ Title ------------------
title = ctk.CTkLabel(
    main_frame,
    text="🎬 YouTube Video Downloader",
    font=ctk.CTkFont(size=20, weight="bold")
)
title.pack(pady=(20, 10))

# ------------------ URL Input ------------------
url_label = ctk.CTkLabel(main_frame, text="Video URL")
url_label.pack(anchor="w", padx=20)

url_entry = ctk.CTkEntry(
    main_frame,
    placeholder_text="Paste YouTube link here 🔗"
)
url_entry.pack(fill="x", padx=20, pady=(5, 15))

# ------------------ Options Frame ------------------
options_frame = ctk.CTkFrame(main_frame, corner_radius=10)
options_frame.pack(fill="x", padx=20, pady=10)

# Format
format_label = ctk.CTkLabel(options_frame, text="Format")
format_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

def format_changed(choice):
    if "MP3" in choice:
        quality_option.configure(
            values=["128 kbps", "192 kbps", "256 kbps", "320 kbps"]
        )
        quality_option.set("192 kbps")
    else:
        quality_option.configure(
            values=["360p", "480p", "720p", "1080p", "1440p (2K)", "2160p (4K)"]
        )
        quality_option.set("1080p")

format_option = ctk.CTkOptionMenu(
    options_frame,
    values=["MP4 (Video)", "MP3 (Audio)"],
    command=format_changed
)
format_option.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

# Quality
quality_label = ctk.CTkLabel(options_frame, text="Quality")
quality_label.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")

quality_option = ctk.CTkOptionMenu(
    options_frame,
    values=["360p", "480p", "720p", "1080p", "1440p (2K)", "2160p (4K)"]
)
quality_option.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")

options_frame.columnconfigure((0, 1), weight=1)

# ------------------ Location ------------------
location_label = ctk.CTkLabel(main_frame, text="Save Location")
location_label.pack(anchor="w", padx=20, pady=(15, 5))

location_frame = ctk.CTkFrame(main_frame, corner_radius=10)
location_frame.pack(fill="x", padx=20)

location_entry = ctk.CTkEntry(
    location_frame,
    placeholder_text="Choose download folder"
)
location_entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        location_entry.delete(0, "end")
        location_entry.insert(0, folder)

browse_btn = ctk.CTkButton(
    location_frame,
    text="Browse",
    width=80,
    command=browse_folder
)
browse_btn.pack(side="right", padx=10)

# ------------------ Progress Bar ------------------
progress_bar = ctk.CTkProgressBar(main_frame)
progress_bar.set(0)
progress_bar.pack(fill="x", padx=20, pady=(20, 5))
# FIX: Border wapas lao aur empty state ko transparent jaisa banao
progress_bar.configure(
    progress_color="#3a3a3a",  # Filled part ka color
    fg_color="#3a3a3a",        # Empty background
    border_color="#555555",    # Border color
    border_width=1,
    height=8                  # Height adjust karo
)

progress_label = ctk.CTkLabel(
    main_frame,
    text="Paste a link to begin",
    text_color="gray"
)
progress_label.pack()

# ------------------ Progress UI ------------------
def update_progress_ui(progress, percent):
    progress_bar.set(progress)
    progress_bar.configure(progress_color="#1f6aa5")  # Ensure blue color during download
    progress_label.configure(text=f"Downloading... {percent}%")

def finish_progress_ui(status="complete", message=None):
    if status == "cancelled":
        progress_bar.set(0)
        progress_bar.configure(progress_color="#3a3a3a")  # Reset to grey
        progress_label.configure(text="Download Cancelled ❌")
    elif status == "error":
        progress_bar.set(0)
        progress_bar.configure(progress_color="#3a3a3a")  # Reset to grey
        progress_label.configure(text=f"Error: {message}")
    else:
        progress_bar.set(1)
        progress_bar.configure(progress_color="#1f6aa5")  # Keep blue for complete
        progress_label.configure(text="✅ Download Complete!")

    download_btn.configure(state="normal")
    cancel_btn.configure(state="disabled")

# ------------------ Progress Hook (CORRECT WAY) ------------------
def progress_hook(d):
    global cancel_download

    if cancel_download:
        raise DownloadError("Download cancelled by user")

    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes') or d.get('total_bytes_estimate')

        if total:
            progress = downloaded / total
            percent = int(progress * 100)
            app.after(0, update_progress_ui, progress, percent)


# ------------------ Download Logic ------------------
def start_download():
    global cancel_download, current_ydl
    cancel_download = False

    url = url_entry.get().strip()
    path = location_entry.get().strip()

    if not url or not path:
        progress_label.configure(text="Please enter URL and select folder")
        return

    # ✅ ADD THIS: Create folder if doesn't exist
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        progress_label.configure(text=f"Invalid path: {str(e)[:50]}")
        return

    # ... rest of the code ...

    download_btn.configure(state="disabled")
    cancel_btn.configure(state="normal")
    progress_bar.set(0)
    progress_label.configure(text="Starting download...")

    is_mp3 = "MP3" in format_option.get()
    selected_quality = quality_option.get()

    if is_mp3 and shutil.which("ffmpeg") is None:
        progress_label.configure(text="❌ FFmpeg not found! Install FFmpeg for MP3 downloads.")
        download_btn.configure(state="normal")
        cancel_btn.configure(state="disabled")
        return

    ydl_opts = {
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'progress_hooks': [progress_hook],
        'noplaylist': True,
        'quiet': True,
	'restrictfilenames': True,
    }

    if is_mp3:
        bitrate = selected_quality.replace(" kbps", "")
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate,
            }],
        })
    else:
        if "2160" in selected_quality:
            height = 2160
        elif "1440" in selected_quality:
            height = 1440
        else:
            height = int(selected_quality.replace("p", ""))

        ydl_opts.update({
            'format': f'bestvideo[height<={height}]+bestaudio/best/best',
            'merge_output_format': 'mp4',
        })

    def run():
        global current_ydl, cancel_download
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                current_ydl = ydl
                ydl.download([url])

            if not cancel_download:
                app.after(0, finish_progress_ui)

        except DownloadError as e:
            if "Download cancelled by user" in str(e):
                app.after(0, finish_progress_ui, "cancelled")
            else:
                app.after(0, finish_progress_ui, "error", str(e)[:60])

        except Exception as e:
            app.after(0, finish_progress_ui, "error", str(e)[:60])

        finally:
            current_ydl = None
            cancel_download = False

    threading.Thread(target=run, daemon=True).start()

def cancel_current_download():
    global cancel_download
    cancel_download = True
    progress_label.configure(text="Cancelling...")
    cancel_btn.configure(state="disabled")
    
    # ✅ YAHAN ADD KARO: Force stop yt-dlp
    if current_ydl:
        try:
            # This forces yt-dlp to stop immediately
            current_ydl._download_retcode = -1
        except AttributeError:
            pass  # Agar attribute nahi mila to chhodo

def on_close():
    global cancel_download
    if download_btn.cget("state") == "disabled":
        cancel_download = True
    app.destroy()


# ------------------ Buttons Row ------------------
buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
buttons_frame.pack(pady=25)

download_btn = ctk.CTkButton(
    buttons_frame,
    text="⬇ Download",
    height=35,
    width=120,
    font=ctk.CTkFont(size=15, weight="bold"),
    command=start_download,
    state="disabled"
)
download_btn.pack(side="left", padx=10)

cancel_btn = ctk.CTkButton(
    buttons_frame,
    text="✖ Cancel",
    height=35,
    width=120,
    font=ctk.CTkFont(size=15, weight="bold"),
    fg_color="#8b0000",
    hover_color="#a00000",
    command=cancel_current_download,
    state="disabled"
)
cancel_btn.pack(side="left", padx=10)

# ------------------ URL Validation ------------------
def check_url(event=None):
    if url_entry.get().strip():
        download_btn.configure(state="normal")
        progress_label.configure(text="Ready to download")
    else:
        download_btn.configure(state="disabled")
        progress_label.configure(text="Paste a link to begin")

url_entry.bind("<KeyRelease>", check_url)

# # ------------------ Status ------------------
# status_label = ctk.CTkLabel(
#     main_frame,	
#     text="Ready",
#     text_color="gray"
# )
# status_label.pack(pady=(0, 10))

# ------------------ Run App ------------------
app.protocol("WM_DELETE_WINDOW", on_close)
app.mainloop()