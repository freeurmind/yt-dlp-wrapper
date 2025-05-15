#!/usr/bin/env python3

import argparse
import subprocess
import os
import re
import json
from datetime import datetime

# Helper to run a shell command and return output
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# Get video info as JSON
def get_video_info(url):
    cmd = f'yt-dlp -j "{url}"'
    output = run_cmd(cmd)
    return json.loads(output)

# Get available formats
def get_formats(url):
    cmd = f'yt-dlp --list-formats "{url}"'
    return run_cmd(cmd)

# Parse formats to get best video (mp4) and best audio (m4a)
def select_best_formats(formats_output):
    video_id = None
    audio_id = None
    video_re = re.compile(r'^(\d+)\s+mp4')
    audio_re = re.compile(r'^(\d+)\s+m4a')
    best_video = (0, None)
    best_audio = (0, None)
    for line in formats_output.splitlines():
        v = video_re.match(line)
        if v:
            # Try to get resolution or TBR
            tbr = re.search(r'(\d+)k', line)
            tbr_val = int(tbr.group(1)) if tbr else 0
            if tbr_val > best_video[0]:
                best_video = (tbr_val, v.group(1))
        a = audio_re.match(line)
        if a:
            abr = re.search(r'(\d+)k', line)
            abr_val = int(abr.group(1)) if abr else 0
            if abr_val > best_audio[0]:
                best_audio = (abr_val, a.group(1))
    return best_video[1], best_audio[1]

def main():
    parser = argparse.ArgumentParser(description='yt-dlp wrapper')
    parser.add_argument('url', help='YouTube URL')
    args = parser.parse_args()
    url = args.url

    # Get formats
    formats_output = get_formats(url)
    print(formats_output)

    # Select best video/audio
    video_id, audio_id = select_best_formats(formats_output)
    if not video_id or not audio_id:
        print('Could not find suitable video/audio formats.')
        return
    print(f'Selected video: {video_id}, audio: {audio_id}')

    # Get video info for title and date
    info = get_video_info(url)
    title = info.get('title', 'video')
    date_str = info.get('upload_date') or info.get('release_date')
    if date_str:
        date_fmt = datetime.strptime(date_str, '%Y%m%d').strftime('%Y.%m.%d')
    else:
        date_fmt = datetime.now().strftime('%Y.%m.%d')
    folder_name = f"{date_fmt} - {title}"
    folder_name = re.sub(r'[\\/:*?\"<>|]', '', folder_name)  # Clean for filesystem
    out_dir = os.path.expanduser(f"~/Downloads/{folder_name}")
    os.makedirs(out_dir, exist_ok=True)

    # Download command
    dl_cmd = (
        f'yt-dlp -f {video_id}+{audio_id} --write-auto-sub --sub-lang "en.*" '
        f'--convert-subs srt -P "{out_dir}" "{url}"'
    )
    print(f"Running: {dl_cmd}")
    subprocess.run(dl_cmd, shell=True)

if __name__ == '__main__':
    main()
