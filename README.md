# Starlight Downloader ✨

A user-friendly command-line tool for downloading videos and playlists from various websites supported by `yt-dlp`, including YouTube, Vimeo, SoundCloud, and more. It offers video (MP4) and audio (MP3) downloads with customizable quality options and a colorful, interactive interface.

## Features
- Download single videos in MP4 format with selectable quality from `yt-dlp`-supported websites.
- Extract audio as MP3 (192kbps) from videos.
- Download entire playlists or select specific videos from playlists.
- Progress bar with download speed and estimated time using `tqdm`.
- Colorful CLI interface with ASCII art banner and success cards.
- Sanitizes filenames for cross-platform compatibility.
- Robust error handling for invalid URLs, missing FFmpeg, and download failures.

## Supported Websites
Starlight Downloader leverages `yt-dlp`, which supports hundreds of websites. For a full list, [see the yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md?plain=1). Examples include:
- YouTube
- Vimeo
- SoundCloud
- Dailymotion
- And many more!

## Prerequisites
- **Python 3.8+** installed on your system.
- **FFmpeg** installed and accessible in your system's PATH (required for video downloads and audio extraction).
- Required Python packages:
  - `yt-dlp`: For downloading content from supported websites.
  - `tqdm`: For progress bar visualization.
  - `ctypes`: For setting console title on Windows (built-in).
- On Windows, the console title is set to "Starlight Downloader ✨".

## Installation
1. Clone or download this repository:
   ```bash
   git clone https://github.com/yourusername/Starlight-Downloader
   cd Starlight-Downloader
   ```
2. Install the required Python packages:
   ```bash
   pip install yt-dlp tqdm
   ```
3. Install FFmpeg:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or install via Chocolatey (`choco install ffmpeg`).
   - **Linux**: Use your package manager, e.g., `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora).
   - **macOS**: Install via Homebrew (`brew install ffmpeg`).
4. Verify FFmpeg is accessible by running `ffmpeg -version`.

## Usage
1. Run the program:
   ```bash
   python app_cleaned.py
   ```
2. The program displays a colorful ASCII banner and prompts you to paste a URL from a `yt-dlp`-supported website.
3. Follow the on-screen instructions:
   - For a **single video**:
     - Choose between downloading as video (MP4) or audio (MP3).
     - For video, select a quality from the available resolutions (e.g., 1080p, 720p).
     - The download starts with a progress bar, and a success card is shown upon completion.
   - For a **playlist** (if supported by the website):
     - Choose to download all videos or select a specific video.
     - If selecting a specific video, enter its number from the listed videos.
     - For all videos, they are downloaded into a folder named after the playlist.
4. Files are saved in the current directory (or a playlist-named folder for playlist downloads).

## How It Works
The program is structured into several key components:

1. **Config Class**: Stores constants like the app title, download types, and audio quality.
2. **Colors Class**: Defines ANSI color codes for a visually appealing CLI experience.
3. **TqdmProgressHook Class**: Manages the progress bar and success card display during downloads.
4. **YouTubeDownloader Class**: Handles the core downloading logic using `yt-dlp`:
   - Fetches video/playlist metadata from supported websites.
   - Provides options for video quality or audio extraction.
   - Downloads content with progress tracking.
5. **DownloaderCLI Class**: Orchestrates the user interface, URL input, and download dispatching.

The program uses `yt-dlp` to extract video/playlist information and download content from supported websites. FFmpeg is required for merging video/audio streams and converting to MP3. The interface is designed to be intuitive, with clear prompts and error messages.

## Example
```bash
$ python app_cleaned.py
[Banner and tagline displayed]
 ┌──────────────────────────────────────────────┐
 │  Enter the full link below to get started    │
 └──────────────────────────────────────────────┘
 > Paste Link: https://vimeo.com/example
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
│ Your file is ready.                              │
│ Saved as: Example Video - 1080p.mp4              │
└──────────────────────────────────────────────────┘
```

## Notes
- Filenames are sanitized to remove invalid characters.
- Playlist downloads create a folder with the sanitized playlist title (if supported by the website).
- FFmpeg is required for video downloads and playlist downloads; otherwise, an error will be displayed.
- Interrupt the program with `Ctrl+C` to cancel operations gracefully.
- Not all websites support playlist downloads; check the [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md?plain=1) for details.

## Contributing
Submit issues or pull requests for bug fixes or new features. Ensure code follows the existing style and includes appropriate error handling.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
