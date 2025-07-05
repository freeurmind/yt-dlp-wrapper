# yt-dlp-wrapper

A Python wrapper script for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that intelligently downloads videos from various platforms including YouTube and X (Twitter). The script leverages yt-dlp's powerful built-in format selector to prioritize highest resolution first, then preferred video codecs (av01 > vp9 > avc1). It saves the result in a well-named folder in your `~/Downloads` directory and downloads English auto-generated subtitles for YouTube videos.

## Features

- **Smart Format Selection**: Uses yt-dlp's built-in format selector with resolution priority (4K > 2K > 1080p > 720p) and codec preference (av01 > vp9 > avc1)
- **Firefox Integration**: Automatically extracts cookies from Firefox for authenticated downloads
- **Multi-Platform Support**: Works with YouTube, X (Twitter), and other platforms supported by yt-dlp
- **Subtitle Download**: Downloads English auto-generated subtitles and converts them to SRT format
- **Organized Output**: Creates folders named `YYYY.MM.DD - <Video Title>` in your `~/Downloads` directory
- **Simple Usage**: Single command-line interface

## Format Selection Strategy

The script uses yt-dlp's advanced format selector with the following priority:

1. **Resolution Priority**: 4K (2160p) → 2K (1440p) → 1080p → 720p
2. **Codec Priority**: Within each resolution, prefers av01 > vp9 > avc1
3. **Fallback**: Best available format if preferred options aren't available

## Requirements

- Python 3.6+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed and available in your PATH
- Firefox browser (for cookie extraction)

## Installation

1. Clone this repository or copy `yt-dlp-wrapper.py` to your local machine.
2. Make sure `yt-dlp` is installed:
    ```sh
    pip install -U yt-dlp
    ```
3. (Optional) Make the script executable:
    ```sh
    chmod +x yt-dlp-wrapper.py
    ```

## Usage

Run the script with a video URL from a supported platform:

**YouTube:**
```sh
python yt-dlp-wrapper.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

**X (Twitter):**
```sh
python yt-dlp-wrapper.py "https://twitter.com/username/status/YOUR_TWEET_ID"
```

**Other platforms:**
```sh
python yt-dlp-wrapper.py "https://example.com/video"
```

Or, if you made it executable:

```sh
./yt-dlp-wrapper.py "<URL>"
```

## What the script does

1. **Detects platform** from the URL
2. **Extracts cookies** from Firefox for authenticated access
3. **Fetches video metadata** to get title and upload date
4. **Creates output directory** with organized naming
5. **Downloads video** using yt-dlp's format selector with your preferences
6. **Downloads subtitles** (for YouTube videos)
7. **Saves everything** to the organized folder

## Example

```sh
python yt-dlp-wrapper.py "https://www.youtube.com/watch?v=u2Ftw_VuedA"
```

This will:
- Download the highest resolution available (prioritizing 4K if available)
- Prefer av01 codec, then vp9, then avc1 within that resolution
- Download English subtitles
- Save to `~/Downloads/YYYY.MM.DD - Video Title/`

## Notes

- The script automatically uses your Firefox cookies for authenticated downloads
- Output folder names are sanitized for filesystem compatibility
- Format selection is handled entirely by yt-dlp's robust built-in selector
- Works with any platform supported by yt-dlp

## License

MIT License

---