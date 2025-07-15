#!/usr/bin/env python3

"""
Optimized multi-platform video downloader wrapper for yt-dlp.
Supports YouTube, X (Twitter), and other platforms with improved error handling,
performance, and maintainability.
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple


# Configuration constants
DEFAULT_FORMAT_SELECTOR = (
    "bestvideo[height<=2160][vcodec~='^(av01|vp9|avc1)']+bestaudio/"
    "bestvideo[height<=1440][vcodec~='^(av01|vp9|avc1)']+bestaudio/"
    "bestvideo[height<=1080][vcodec~='^(av01|vp9|avc1)']+bestaudio/"
    "bestvideo[height<=720][vcodec~='^(av01|vp9|avc1)']+bestaudio/"
    "best[ext=mp4]/best"
)

SUPPORTED_PLATFORMS = {
    'youtube': ['youtube.com', 'youtu.be'],
    'x': ['twitter.com', 'x.com'],
    'other': []
}

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class YtDlpWrapperError(Exception):
    """Custom exception for wrapper-specific errors."""
    pass


class VideoDownloader:
    """Main class for handling video downloads with yt-dlp."""
    
    def __init__(self, cookies_browser: str = 'firefox'):
        self.cookies_browser = cookies_browser
        self._validate_dependencies()
    
    def _validate_dependencies(self) -> None:
        """Validate that required dependencies are available."""
        if not shutil.which('yt-dlp'):
            raise YtDlpWrapperError(
                "yt-dlp not found. Install with: pip install -U yt-dlp"
            )
        
        # Check if browser is available for cookie extraction
        browser_paths = {
            'firefox': [
                '/Applications/Firefox.app',
                '~/.mozilla/firefox',
                '/usr/bin/firefox'
            ]
        }
        
        if self.cookies_browser in browser_paths:
            paths = browser_paths[self.cookies_browser]
            if not any(Path(p).expanduser().exists() for p in paths):
                logger.warning(f"{self.cookies_browser} not found. Downloads may fail for authenticated content.")
    
    def _run_command(self, cmd: str, capture_output: bool = True) -> Tuple[bool, str]:
        """Run a shell command and return success status and output."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                text=True,
                check=True,
                timeout=300  # 5 minute timeout
            )
            return True, result.stdout
        except subprocess.TimeoutExpired:
            logger.error("Command timed out after 5 minutes")
            return False, ""
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed with return code {e.returncode}")
            if e.stderr:
                logger.error(f"Error details: {e.stderr}")
            return False, e.stderr or ""
    
    def get_video_info(self, url: str) -> Dict:
        """Get video metadata as JSON."""
        cmd = f'yt-dlp --cookies-from-browser {self.cookies_browser} -j "{url}"'
        success, output = self._run_command(cmd)
        
        if not success or not output:
            logger.warning("Could not retrieve video information")
            return {}
        
        try:
            return json.loads(output)
        except json.JSONDecodeError as e:
            logger.error(f"Could not parse video information: {e}")
            return {}
    
    def detect_platform(self, url: str) -> str:
        """Detect the platform from the URL."""
        url_lower = url.lower()
        for platform, domains in SUPPORTED_PLATFORMS.items():
            if any(domain in url_lower for domain in domains):
                return platform
        return 'other'
    
    def create_output_dir(self, title: str, date_str: Optional[str] = None) -> Path:
        """Create an output directory based on video title and date."""
        # Format date
        if date_str:
            try:
                date_fmt = datetime.strptime(date_str, '%Y%m%d').strftime('%Y.%m.%d')
            except ValueError:
                logger.warning(f"Invalid date format: {date_str}")
                date_fmt = datetime.now().strftime('%Y.%m.%d')
        else:
            date_fmt = datetime.now().strftime('%Y.%m.%d')
        
        # Clean title for filesystem compatibility
        clean_title = re.sub(r'[\\/:*?\"<>|]', '', title)
        clean_title = clean_title.strip()[:100]  # Limit length
        
        folder_name = f"{date_fmt} - {clean_title}"
        output_dir = Path.home() / "Downloads" / folder_name
        
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise YtDlpWrapperError(f"Could not create output directory: {e}")
        
        return output_dir
    
    def download_video(self, url: str, extra_args: list = None, 
                      format_selector: str = None) -> bool:
        """Download video using yt-dlp with optimized settings."""
        if extra_args is None:
            extra_args = []
        
        if format_selector is None:
            format_selector = DEFAULT_FORMAT_SELECTOR
        
        # Detect platform
        platform = self.detect_platform(url)
        logger.info(f"Detected platform: {platform.capitalize()}")
        
        # Get video metadata
        logger.info("Fetching video metadata...")
        info = self.get_video_info(url)
        
        # Create output directory
        title = info.get('title', 'video')
        date_str = info.get('upload_date') or info.get('release_date')
        output_dir = self.create_output_dir(title, date_str)
        logger.info(f"Output directory: {output_dir}")
        
        # Build command
        base_cmd = [
            'yt-dlp',
            '--cookies-from-browser', self.cookies_browser,
            '-f', format_selector,
            '--write-auto-sub',
            '--sub-lang', 'en.*',
            '--convert-subs', 'srt',
            '-P', str(output_dir),
            '--no-mtime',  # Don't set file modification time
            '--embed-metadata',  # Embed metadata in video file
        ]
        
        # Add extra arguments
        base_cmd.extend(extra_args)
        base_cmd.append(url)
        
        # Execute download
        logger.info("Starting download...")
        try:
            result = subprocess.run(base_cmd, check=True, timeout=3600)  # 1 hour timeout
            logger.info("Download completed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Download failed with return code {e.returncode}")
            return False
        except subprocess.TimeoutExpired:
            logger.error("Download timed out after 1 hour")
            return False


def main():
    """Main function to handle command line arguments and orchestrate the download."""
    parser = argparse.ArgumentParser(
        description='Download videos from YouTube, X (Twitter), and other platforms',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=VIDEO_ID"
  %(prog)s "https://twitter.com/user/status/TWEET_ID" --format "best[height<=720]"
        """
    )
    
    parser.add_argument('url', help='URL to download')
    parser.add_argument('--format', '-f', 
                       help='Custom format selector (overrides default)')
    parser.add_argument('--browser', '-b', default='firefox',
                       choices=['firefox', 'chrome', 'safari'],
                       help='Browser to extract cookies from (default: firefox)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    # Parse known and unknown args to allow passing through to yt-dlp
    args, extra_args = parser.parse_known_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        downloader = VideoDownloader(cookies_browser=args.browser)
        success = downloader.download_video(
            args.url, 
            extra_args=extra_args,
            format_selector=args.format
        )
        
        sys.exit(0 if success else 1)
        
    except YtDlpWrapperError as e:
        logger.error(str(e))
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Download interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
