import os
import shutil
from tqdm import tqdm
import ctypes
import yt_dlp
from typing import Dict, Any, Optional

class Config:
    APP_TITLE = "Starlight Downloader ✨"
    DOWNLOAD_TYPE_VIDEO = '1'
    DOWNLOAD_TYPE_AUDIO = '2'
    PLAYLIST_DOWNLOAD_ALL = 'A'
    PLAYLIST_DOWNLOAD_SELECT = 'S'
    AUDIO_QUALITY = '192'

class Colors:
    RESET = '\033[0m'
    PRIMARY_RED = '\033[91m'
    BUTTON_PINK = '\033[95m'
    ICON_GREEN = '\033[92m'
    SUCCESS_BG_SIM = '\033[42m'
    TEXT_ON_BG = '\033[97m'

    WHITE = '\033[97m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    
    BANNER_MAGENTA = '\033[35m'
    BANNER_RED = '\033[31m'

if os.name == 'nt':
    os.system('')
    ctypes.windll.kernel32.SetConsoleTitleW(Config.APP_TITLE)

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner() -> None:
    banner = f"""
{Colors.BANNER_MAGENTA}.▄▄ · ▄▄▄▄▄ ▄▄▄· ▄▄▄  ▄▄▌  ▪   ▄▄ •  ▄ .▄▄▄▄▄▄              
{Colors.BANNER_MAGENTA}▐█ ▀. •██  ▐█ ▀█ ▀▄ █·██•  ██ ▐█ ▀ ▪██▪▐█•██                
{Colors.BANNER_MAGENTA}▄▀▀▀█▄ ▐█.▪▄█▀▀█ ▐▀▀▄ ██▪  ▐█·▄█ ▀█▄██▀▐█ ▐█.▪              
{Colors.BANNER_MAGENTA}▐█▄▪▐█ ▐█▌·▐█ ▪▐▌▐█•█▌▐█▌▐▌▐█▌▐█▄▪▐███▌▐▀ ▐█▌·              
{Colors.BANNER_MAGENTA} ▀▀▀▀  ▀▀▀  ▀  ▀ .▀  ▀.▀▀▀ ▀▀▀·▀▀▀▀ ▀▀▀ · ▀▀▀               
{Colors.BANNER_RED}·▄▄▄▄        ▄▄▌ ▐ ▄▌ ▐ ▄ ▄▄▌         ▄▄▄· ·▄▄▄▄  ▄▄▄ .▄▄▄  
{Colors.BANNER_RED}██▪ ██ ▪     ██· █▌▐█•█▌▐███•  ▪     ▐█ ▀█ ██▪ ██ ▀▄.▀·▀▄ █·
{Colors.BANNER_RED}▐█· ▐█▌ ▄█▀▄ ██▪▐█▐▐▌▐█▐▐▌██▪   ▄█▀▄ ▄█▀▀█ ▐█· ▐█▌▐▀▀▪▄▐▀▀▄ 
{Colors.BANNER_RED}██. ██ ▐█▌.▐▌▐█▌██▐█▌██▐█▌▐█▌▐▌▐█▌.▐▌▐█ ▪▐▌██. ██ ▐█▄▄▌▐█•█▌
{Colors.BANNER_RED}▀▀▀▀▀•  ▀█▄▀▪ ▀▀▀▀ ▀▪▀▀ ▀▪.▀▀▀  ▀█▄▀▪ ▀  ▀ ▀▀▀▀▀•  ▀▀▀ .▀  ▀
{Colors.RESET}
    """
    tagline = f"{Colors.YELLOW}A user-friendly video & playlist downloader by yt-dlp{Colors.RESET}"
    print(banner)
    print(tagline.center(shutil.get_terminal_size().columns))
    print()

def sanitize_filename(title: str) -> str:
    return "".join([c for c in title if c.isalpha() or c.isdigit() or c in ' ._-']).rstrip()

class TqdmProgressHook:
    def __init__(self):
        self.pbar: Optional[tqdm] = None

    def __call__(self, d: Dict[str, Any]) -> None:
        if d['status'] == 'downloading':
            if self.pbar is None:
                desc = os.path.basename(d.get('filename', 'Downloading...'))
                self.pbar = tqdm(
                    total=d.get('total_bytes') or d.get('total_bytes_estimate'),
                    unit='B', unit_scale=True,
                    desc=f"{Colors.WHITE}{desc[:40]:<40}{Colors.RESET}",
                    bar_format=f'{{l_bar}}{Colors.BUTTON_PINK}{{bar}}{Colors.RESET}| {{n_fmt}}/{{total_fmt}} [{{elapsed}}<{{remaining}}]'
                )
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            if self.pbar.total != total:
                 self.pbar.total = total
            self.pbar.update(d['downloaded_bytes'] - self.pbar.n)
        
        elif d['status'] == 'finished':
            if self.pbar:
                self.pbar.close()
                self.pbar = None
            
            self._print_success_card(d.get('filename', 'Unknown File'))
            if d.get('postprocessor'):
                 print(f"    {Colors.YELLOW}Processing: {d['postprocessor']}...{Colors.RESET}")
        
        elif d['status'] == 'error':
            if self.pbar:
                self.pbar.close()
                self.pbar = None
            print(f"\n{Colors.PRIMARY_RED}[!] Download error: {d.get('error', 'Unknown error')}{Colors.RESET}")

    def _print_success_card(self, filename: str) -> None:
        short_filename = os.path.basename(filename)
        print("\n" + " " * 2 + f"{Colors.SUCCESS_BG_SIM}{Colors.TEXT_ON_BG} ✔ Download Finished! " + f"{Colors.RESET}")
        print(" " * 2 + f"┌──────────────────────────────────────────────────┐")
        print(" " * 2 + f"│ {Colors.WHITE}Your file is ready.                             {Colors.RESET}│")
        if len(short_filename) > 45:
            print(" " * 2 + f"│ Saved as: {Colors.ICON_GREEN}{short_filename[:42]}...{Colors.RESET}")
        else:
            print(" " * 2 + f"│ Saved as: {Colors.ICON_GREEN}{short_filename:<45}{Colors.RESET} │")
        print(" " * 2 + f"└──────────────────────────────────────────────────┘\n")

class YouTubeDownloader:
    """Handles the core logic for downloading videos and playlists using yt-dlp."""

    def __init__(self):
        self.progress_hook = TqdmProgressHook()

    def _get_ffmpeg_path(self) -> Optional[str]:
        return shutil.which('ffmpeg')

    def _get_video_download_options(self, info_dict: Dict[str, Any], sanitized_title: str) -> Optional[Dict[str, Any]]:
        if not self._get_ffmpeg_path():
            print(f"\n{Colors.PRIMARY_RED}[!] Critical Error: FFmpeg not found. FFmpeg is required for video downloads.{Colors.RESET}")
            return None

        print(f"\n{Colors.YELLOW}[~] Searching for available qualities...{Colors.RESET}")
        formats = [
            f for f in info_dict.get('formats', [])
            if f.get('vcodec') != 'none' and f.get('acodec') != 'none' and f.get('height') is not None
        ]
        
        if not formats:
            print(f"{Colors.PRIMARY_RED}[!] Error: No suitable video formats found.{Colors.RESET}")
            return None

        sorted_formats = sorted(formats, key=lambda x: x.get('height', 0), reverse=True)

        print(f"\n{Colors.WHITE}Available qualities (MP4):{Colors.RESET}")
        for i, f in enumerate(sorted_formats):
            resolution = f.get('format_note') or f.get('resolution') or f"{f.get('width')}x{f.get('height')}"
            filesize_bytes = f.get('filesize') or f.get('filesize_approx')
            filesize_mb = f"{filesize_bytes / (1024 * 1024):.2f} MB" if filesize_bytes else "Unknown size"
            print(f"  {Colors.YELLOW}{i+1}){Colors.RESET} {resolution:<15} ({filesize_mb})")

        try:
            quality_choice_idx = int(input(f"\n{Colors.BUTTON_PINK}> Enter quality number: {Colors.RESET}").strip()) - 1
            chosen_format = sorted_formats[quality_choice_idx]
        except (ValueError, IndexError):
            print(f"{Colors.PRIMARY_RED}[!] Invalid choice.{Colors.RESET}")
            return None

        chosen_res = chosen_format.get('format_note') or chosen_format.get('resolution')
        print(f"\n{Colors.YELLOW}[~] Quality selected: {chosen_res}. Preparing download...{Colors.RESET}")
        
        return {
            'format': chosen_format['format_id'],
            'outtmpl': f'{sanitized_title} - {chosen_res}.mp4',
            'remux_video': 'mp4',
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'noplaylist': True,
        }

    def _get_audio_download_options(self, sanitized_title: str) -> Dict[str, Any]:
        return {
            'format': 'm4a/bestaudio/best',
            'outtmpl': f'{sanitized_title}.mp3',
            'progress_hooks': [self.progress_hook],
            'postprocessors': [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': Config.AUDIO_QUALITY},
                {'key': 'EmbedThumbnail'},
                {'key': 'FFmpegMetadata'}
            ],
            'quiet': True,
            'noplaylist': True,
        }

    def download_single_video(self, info_dict: Dict[str, Any], url: str) -> None:
        title = info_dict.get('title', 'unknown_video')
        sanitized_title = sanitize_filename(title)
        print(f"\n{Colors.WHITE}[+] Video Title: {title}{Colors.RESET}")

        print(f"\n{Colors.WHITE}┌──────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.WHITE}│{Colors.RESET}  1) Download Video (MP4)     {Colors.WHITE}│{Colors.RESET}")
        print(f"{Colors.WHITE}│{Colors.RESET}  2) Download Audio (MP3)     {Colors.WHITE}│{Colors.RESET}")
        print(f"{Colors.WHITE}└──────────────────────────────┘{Colors.RESET}")
        choice = input(f"{Colors.BUTTON_PINK}> Choose an option: {Colors.RESET}").strip()
        
        ydl_opts: Optional[Dict[str, Any]] = None

        if choice == Config.DOWNLOAD_TYPE_AUDIO:
            ydl_opts = self._get_audio_download_options(sanitized_title)
        elif choice == Config.DOWNLOAD_TYPE_VIDEO:
            ydl_opts = self._get_video_download_options(info_dict, sanitized_title)
        else:
            print(f"{Colors.PRIMARY_RED}[!] Invalid choice. Please enter '{Config.DOWNLOAD_TYPE_VIDEO}' or '{Config.DOWNLOAD_TYPE_AUDIO}'.{Colors.RESET}")
            return

        if ydl_opts is None:
            return

        try:
            print(f"\n{Colors.BLUE}Starting download...{Colors.RESET}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            if self.progress_hook.pbar:
                self.progress_hook.pbar.close()
            print(f"\n{Colors.PRIMARY_RED}[!] An error occurred during download: {e}{Colors.RESET}")

    def download_playlist(self, playlist_info: Dict[str, Any], url: str) -> None:
        playlist_title = playlist_info.get('title', 'Unknown Playlist')
        video_count = playlist_info.get('playlist_count', len(playlist_info.get('entries', [])))
        print(f"\n{Colors.WHITE}[+] Playlist Detected: {playlist_title} ({video_count} videos){Colors.RESET}")
        
        choice = input(f"\n{Colors.BUTTON_PINK}> Download ({Config.PLAYLIST_DOWNLOAD_ALL})ll videos, or ({Config.PLAYLIST_DOWNLOAD_SELECT})elect one? [{Config.PLAYLIST_DOWNLOAD_ALL}/{Config.PLAYLIST_DOWNLOAD_SELECT}]: {Colors.RESET}").strip().upper()

        if choice == Config.PLAYLIST_DOWNLOAD_SELECT:
            self._handle_select_from_playlist(playlist_info)
        elif choice == Config.PLAYLIST_DOWNLOAD_ALL:
            self._handle_download_all_playlist_videos(playlist_info, url)
        else:
            print(f"{Colors.PRIMARY_RED}[!] Invalid choice. Please enter '{Config.PLAYLIST_DOWNLOAD_ALL}' or '{Config.PLAYLIST_DOWNLOAD_SELECT}'.{Colors.RESET}")

    def _handle_select_from_playlist(self, playlist_info: Dict[str, Any]) -> None:
        print(f"\n{Colors.WHITE}Videos in playlist:{Colors.RESET}")
        for i, entry in enumerate(playlist_info['entries']):
            print(f"  {Colors.YELLOW}{i+1:02d}){Colors.RESET} {entry.get('title', 'Untitled Video')}")
        
        try:
            video_idx = int(input(f"\n{Colors.BUTTON_PINK}> Enter the number of the video to download: {Colors.RESET}").strip()) - 1
            if not (0 <= video_idx < len(playlist_info['entries'])):
                raise IndexError
            
            chosen_video_info = playlist_info['entries'][video_idx]
            video_id = chosen_video_info['id']
            single_video_url = f"https://www.youtube.com/watch?v={video_id}"

            print(f"\n{Colors.YELLOW}[~] Fetching full info for selected video...{Colors.RESET}")
            with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
                single_info_dict = ydl.extract_info(single_video_url, download=False)
            self.download_single_video(single_info_dict, single_video_url)
        except (ValueError, IndexError):
            print(f"{Colors.PRIMARY_RED}[!] Invalid selection.{Colors.RESET}")
        except yt_dlp.utils.DownloadError as e:
            print(f"\n{Colors.PRIMARY_RED}[!] Error fetching info for selected video: {e}{Colors.RESET}")


    def _handle_download_all_playlist_videos(self, playlist_info: Dict[str, Any], url: str) -> None:
        if not self._get_ffmpeg_path():
            print(f"\n{Colors.PRIMARY_RED}[!] Critical Error: FFmpeg is required for playlist downloads (to merge video/audio) but not found.{Colors.RESET}")
            return

        playlist_title = playlist_info.get('title', 'Unknown Playlist')
        video_count = playlist_info.get('playlist_count', len(playlist_info.get('entries', [])))
        print(f"\n{Colors.YELLOW}[~] Preparing to download all {video_count} videos.{Colors.RESET}")
        sanitized_playlist_title = sanitize_filename(playlist_title)
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{sanitized_playlist_title}/%(playlist_index)02d - %(title)s.%(ext)s',
            'merge_output_format': 'mp4',
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'ignoreerrors': True,
        }
        
        try:
            print(f"\n{Colors.BLUE}Starting playlist download...{Colors.RESET}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"\n{Colors.PRIMARY_RED}[!] An error occurred during playlist download: {e}{Colors.RESET}")

class DownloaderCLI:
    def __init__(self):
        self.downloader = YouTubeDownloader()

    def run(self) -> None:
        clear_screen()
        print_banner()
        self._prompt_for_url()

    def _prompt_for_url(self) -> None:
        print(f" {Colors.WHITE}┌──────────────────────────────────────────────┐{Colors.RESET}")
        print(f" {Colors.WHITE}│{Colors.RESET}  Enter the full link below to get started   {Colors.WHITE}│{Colors.RESET}")
        print(f" {Colors.WHITE}└──────────────────────────────────────────────┘{Colors.RESET}")
        url = input(f" {Colors.BUTTON_PINK}> Paste Link: {Colors.RESET}").strip()

        if not url:
            print(f"{Colors.PRIMARY_RED}[!] Error: The URL cannot be empty.{Colors.RESET}")
            return

        print(f"\n{Colors.YELLOW}[~] Fetching information...{Colors.RESET}")
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': 'in_playlist', 'ignoreerrors': True}) as ydl:
                info_dict = ydl.extract_info(url, download=False)
        except yt_dlp.utils.DownloadError as e:
            print(f"\n{Colors.PRIMARY_RED}[!] Error fetching information: {e}{Colors.RESET}")
            return
        
        if not info_dict:
            print(f"{Colors.PRIMARY_RED}[!] Could not retrieve any information for that URL.{Colors.RESET}")
            return

        self._dispatch_download(info_dict, url)

    def _dispatch_download(self, info_dict: Dict[str, Any], url: str) -> None:
        if info_dict.get('_type') == 'playlist':
            print(f"\n{Colors.YELLOW}[~] Fetching full playlist details...{Colors.RESET}")
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'ignoreerrors': True}) as ydl:
                    full_playlist_info = ydl.extract_info(url, download=False)
                if full_playlist_info:
                    self.downloader.download_playlist(full_playlist_info, url)
                else:
                    print(f"{Colors.PRIMARY_RED}[!] Could not retrieve full playlist information.{Colors.RESET}")
            except yt_dlp.utils.DownloadError as e:
                print(f"\n{Colors.PRIMARY_RED}[!] Error fetching full playlist information: {e}{Colors.RESET}")
        else:
            print(f"\n{Colors.YELLOW}[~] Fetching full video details...{Colors.RESET}")
            try:
                with yt_dlp.YoutubeDL({'quiet': True, 'noplaylist': True}) as ydl:
                    full_video_info = ydl.extract_info(url, download=False)
                if full_video_info:
                    self.downloader.download_single_video(full_video_info, url)
                else:
                    print(f"{Colors.PRIMARY_RED}[!] Could not retrieve full video information.{Colors.RESET}")
            except yt_dlp.utils.DownloadError as e:
                print(f"\n{Colors.PRIMARY_RED}[!] Error fetching full video information: {e}{Colors.RESET}")

if __name__ == '__main__':
    try:
        cli = DownloaderCLI()
        cli.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}[!] Operation cancelled by user.{Colors.RESET}")
    except Exception as ex:
        print(f"\n\n{Colors.PRIMARY_RED}[!] An unexpected error occurred: {ex}{Colors.RESET}")

