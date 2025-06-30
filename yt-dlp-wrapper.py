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
        cmd = f'yt-dlp --cookies youtube.com_cookies.txt -j "{url}"'
        output = run_command(cmd)
        return json.loads(output) if output else {}
    except json.JSONDecodeError:
        print("Error: Could not parse video information")
        return {}


def get_formats(url):
    """Get available formats list from yt-dlp."""
    cmd = f'yt-dlp --cookies youtube.com_cookies.txt --list-formats "{url}"'
    return run_command(cmd)


def detect_platform(url):
    """Detect the platform from the URL."""
    if 'youtube.com' in url or 'youtu.be' in url:
        return 'youtube'
    elif 'twitter.com' in url or 'x.com' in url:
        return 'x'
    else:
        return 'other'


def select_best_formats(formats_output, platform='youtube'):
    """Parse formats to find best formats based on the platform.
    
    For YouTube: Best MP4 video and M4A audio based on bitrate.
    For X (Twitter): Best available format.
    For other platforms: Falls back to best available format.
    """
    # Initialize variables
    best_video = (0, None)  # (bitrate, format_id)
    best_audio = (0, None)  # (bitrate, format_id)
    best_combined = None     # For platforms with combined formats
    
    # Regular expressions for parsing format lines
    video_pattern = re.compile(r'^(\d+)\s+mp4')
    audio_pattern = re.compile(r'^(\d+)\s+m4a')
    bitrate_pattern = re.compile(r'(\d+)k')
    
    # For X and other platforms, look for best format or combined format
    if platform in ['x', 'other']:
        # Look for lines with best quality indicators
        for line in formats_output.splitlines():
            if 'best' in line.lower():
                match = re.search(r'^(\d+)', line)
                if match:
                    best_combined = match.group(1)
                    break
    
    # YouTube-specific format selection (or fallback for other platforms)
    if platform == 'youtube' or (platform in ['x', 'other'] and not best_combined):
        # Process each line in the format output
        for line in formats_output.splitlines():
            # Check for video formats (mp4)
            video_match = video_pattern.match(line)
            if video_match:
                bitrate_match = bitrate_pattern.search(line)
                bitrate = int(bitrate_match.group(1)) if bitrate_match else 0
                if bitrate > best_video[0]:
                    best_video = (bitrate, video_match.group(1))
            
            # Check for audio formats (m4a)
            audio_match = audio_pattern.match(line)
            if audio_match:
                bitrate_match = bitrate_pattern.search(line)
                bitrate = int(bitrate_match.group(1)) if bitrate_match else 0
                if bitrate > best_audio[0]:
                    best_audio = (bitrate, audio_match.group(1))
    
    # Return based on platform
    if best_combined:
        return best_combined, None  # For platforms with combined format
    else:
        return best_video[1], best_audio[1]  # For YouTube-style separate formats


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
    args = parser.parse_args()
    
    # Detect platform
    platform = detect_platform(args.url)
    print(f"Detected platform: {platform.capitalize()}")
    
    # Get available formats
    print("Fetching available formats...")
    formats_output = get_formats(args.url)
    if not formats_output:
        print("Error: Could not retrieve video formats.")
        sys.exit(1)
    print(formats_output)
    
    # Select best formats based on platform
    video_id, audio_id = select_best_formats(formats_output, platform)
    
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
    
    # Build and execute download command based on platform
    if platform == 'youtube' and video_id and audio_id:
        # YouTube with separate video and audio formats
        dl_cmd = (
            f'yt-dlp --cookies youtube.com_cookies.txt -f {video_id}+{audio_id} --write-auto-sub --sub-lang "en.*" '
            f'--convert-subs srt -P "{output_dir}" "{args.url}"'
        )
    elif platform == 'x' and video_id:
        # X (Twitter) with single format (no audio format needed)
        dl_cmd = f'yt-dlp --cookies youtube.com_cookies.txt -f {video_id} -P "{output_dir}" "{args.url}"'
    else:
        # Fallback for other platforms or when format selection fails
        # Let yt-dlp automatically select and merge the best available formats
        dl_cmd = f'yt-dlp --cookies youtube.com_cookies.txt -P "{output_dir}" "{args.url}"'
        print("Using automatic format selection as fallback.")
    
    print(f"Running: {dl_cmd}")
    subprocess.run(dl_cmd, shell=True)
    print("Download complete!")


if __name__ == '__main__':
    main()
