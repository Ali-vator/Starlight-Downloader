# Starlight Downloader ✨

A user-friendly command-line tool for downloading YouTube videos and playlists using `yt-dlp`. It supports both video (MP4) and audio (MP3) downloads with customizable quality options and a colorful, interactive interface.

## Features
- Download single YouTube videos in MP4 format with selectable quality.
- Download audio from videos in MP3 format with high quality (192kbps).
- Download entire YouTube playlists or select specific videos from a playlist.
- Progress bar with download speed and estimated time using `tqdm`.
- Colorful CLI interface with ASCII art banner and success cards.
- Sanitizes filenames to ensure compatibility across operating systems.
- Error handling for invalid URLs, missing FFmpeg, and download failures.

## Prerequisites
- **Python 3.8+** installed on your system.
- **FFmpeg** installed and accessible in your system's PATH (required for video downloads and audio extraction).
- Required Python packages:
  - `yt-dlp`: For downloading YouTube content.
  - `tqdm`: For progress bar visualization.
  - `ctypes`: For setting console title on Windows (built-in).
- On Windows, the console title is set to "Starlight Downloader ✨".

## Installation
1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd starlight-downloader
   ```
2. Install the required Python packages:
   ```bash
   pip install yt-dlp tqdm
   ```
3. Install FFmpeg:
   - **Windows**: Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) or install via a package manager like Chocolatey (`choco install ffmpeg`).
   - **Linux**: Install via your package manager, e.g., `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora).
   - **macOS**: Install via Homebrew (`brew install ffmpeg`).
4. Ensure FFmpeg is accessible by running `ffmpeg -version` in your terminal.

## Usage
1. Run the program:
   ```bash
   python app_cleaned.py
   ```
2. The program displays a colorful ASCII banner and prompts you to paste a YouTube URL (video or playlist).
3. Follow the on-screen instructions:
   - For a **single video**:
     - Choose between downloading as video (MP4) or audio (MP3).
     - For video, select a quality from the available resolutions (e.g., 1080p, 720p).
     - The download starts with a progress bar, and a success card is shown upon completion.
   - For a **playlist**:
     - Choose to download all videos or select a specific video.
     - If selecting a specific video, enter its number from the listed videos.
     - For all videos, they are downloaded sequentially into a folder named after the playlist.
4. Files are saved in the current directory (or a playlist-named folder for playlist downloads).

## How It Works
The program is structured into several key components:

1. **Config Class**: Stores constants like the app title, download types, and audio quality.
2. **Colors Class**: Defines ANSI color codes for a visually appealing CLI experience.
3. **TqdmProgressHook Class**: Manages the progress bar and success card display during downloads.
4. **YouTubeDownloader Class**: Handles the core downloading logic using `yt-dlp`:
   - Fetches video/playlist metadata.
   - Provides options for video quality or audio extraction.
   - Downloads content with progress tracking.
5. **DownloaderCLI Class**: Orchestrates the user interface, URL input, and download dispatching.

The program uses `yt-dlp` to extract video/playlist information and download content. FFmpeg is required for merging video/audio streams and converting to MP3. The interface is designed to be intuitive, with clear prompts and error messages.

## Example
```bash
$ python app_cleaned.py
[Banner and tagline displayed]
 ┌──────────────────────────────────────────────┐
 │  Enter the full link below to get started   │
 └──────────────────────────────────────────────┘
 > Paste Link: https://www.youtube.com/watch?v=example
[~] Fetching information...
[+] Video Title: Example Video
┌──────────────────────────────┐
│  1) Download Video (MP4)     │
│  2) Download Audio (MP3)     │
└──────────────────────────────┘
> Choose an option: 1
[~] Searching for available qualities...
Available qualities (MP4):
  1) 1080p        (150.25 MB)
  2) 720p         (75.50 MB)
> Enter quality number: 1
[~] Quality selected: 1080p. Preparing download...
[Progress bar displayed]
 ✔ Download Finished!
┌──────────────────────────────────────────────────┐
│ Your file is ready.                             │
│ Saved as: Example Video - 1080p.mp4             │
└──────────────────────────────────────────────────┘
```

## Notes
- The program sanitizes filenames to remove invalid characters.
- Playlist downloads create a folder with the sanitized playlist title.
- If FFmpeg is not found, video downloads and playlist downloads will fail with an error message.
- Interrupt the program with `Ctrl+C` to cancel operations gracefully.

## Contributing
Feel free to submit issues or pull requests for bug fixes or new features. Ensure code follows the existing style and includes appropriate error handling.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
