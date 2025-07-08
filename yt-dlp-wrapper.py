#!/usr/bin/env python3

"""
Multi-platform video downloader wrapper for yt-dlp.
Supports YouTube (highest quality MP4 video and M4A audio formats),
X (Twitter), and other platforms supported by yt-dlp.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: Command '{cmd}' failed with return code {e.returncode}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return ""


def get_video_info(url):
    """Get video metadata as JSON."""
    try:
        cmd = f'yt-dlp --cookies-from-browser firefox -j "{url}"'
        output = run_command(cmd)
        return json.loads(output) if output else {}
    except json.JSONDecodeError:
        print("Error: Could not parse video information")
        return {}


def get_formats(url):
    """Get available formats list from yt-dlp."""
    cmd = f'yt-dlp --cookies-from-browser firefox --list-formats "{url}"'
    return run_command(cmd)


def detect_platform(url):
    """Detect the platform from the URL."""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'twitter.com' in url or 'x.com' in url:
        return 'x'
    else:
        return 'other'


def create_output_dir(title, date_str=None):
    """Create an output directory based on video title and date."""
    # Format date
    if date_str:
        try:
            date_fmt = datetime.strptime(date_str, '%Y%m%d').strftime('%Y.%m.%d')
        except ValueError:
            date_fmt = datetime.now().strftime('%Y.%m.%d')
    else:
        date_fmt = datetime.now().strftime('%Y.%m.%d')
    
    # Clean title for filesystem compatibility
    clean_title = re.sub(r'[\\/:*?\"<>|]', '', title)
    folder_name = f"{date_fmt} - {clean_title}"
    
    # Create directory
    output_dir = Path.home() / "Downloads" / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


def main():
    """Main function to handle command line arguments and orchestrate the download."""
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Download videos from YouTube, X (Twitter), and other platforms'
    )
    parser.add_argument('url', help='URL to download (YouTube, X, etc.)')
    # Parse known and unknown args
    args, extra_args = parser.parse_known_args()
    
    # Detect platform (optional, kept for possible future use)
    platform = detect_platform(args.url)
    print(f"Detected platform: {platform.capitalize()}")
    
    # Get video metadata
    print("Fetching video metadata...")
    info = get_video_info(args.url)
    if not info:
        print("Warning: Could not get complete video information.")
    
    # Create output directory
    title = info.get('title', 'video')
    date_str = info.get('upload_date') or info.get('release_date')
    output_dir = create_output_dir(title, date_str)
    print(f"Output directory: {output_dir}")
    
    # Use yt-dlp's built-in format selector with highest resolution priority, then vcodec: av01 > vp9 > avc1
    format_selector = (
        'bestvideo[height>=2160][vcodec=av01]+bestaudio/'
        'bestvideo[height>=2160][vcodec=vp9]+bestaudio/'
        'bestvideo[height>=2160][vcodec=avc1]+bestaudio/'
        'bestvideo[height>=2160]+bestaudio/'
        'bestvideo[height>=1440][vcodec=av01]+bestaudio/'
        'bestvideo[height>=1440][vcodec=vp9]+bestaudio/'
        'bestvideo[height>=1440][vcodec=avc1]+bestaudio/'
        'bestvideo[height>=1440]+bestaudio/'
        'bestvideo[height>=1080][vcodec=av01]+bestaudio/'
        'bestvideo[height>=1080][vcodec=vp9]+bestaudio/'
        'bestvideo[height>=1080][vcodec=avc1]+bestaudio/'
        'bestvideo[height>=1080]+bestaudio/'
        'bestvideo[height>=720][vcodec=av01]+bestaudio/'
        'bestvideo[height>=720][vcodec=vp9]+bestaudio/'
        'bestvideo[height>=720][vcodec=avc1]+bestaudio/'
        'bestvideo[height>=720]+bestaudio/'
        'best[ext=mp4]/best'
    )
    
    # Build the yt-dlp command, including any extra args
    extra_args_str = ' '.join([f'"{arg}"' if ' ' in arg else arg for arg in extra_args])
    dl_cmd = (
        f'yt-dlp --cookies-from-browser firefox '
        f'-f "{format_selector}" '
        f'--write-auto-sub --sub-lang "en.*" --convert-subs srt '
        f'-P "{output_dir}" {extra_args_str} "{args.url}"'
    )
    
    print(f"Running: {dl_cmd}")
    subprocess.run(dl_cmd, shell=True)
    print("Download complete!")


if __name__ == '__main__':
    main()
