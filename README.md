# yt-dlp-wrapper

A Python wrapper script for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that intelligently downloads videos from various platforms including YouTube and X (Twitter). For YouTube, it downloads the highest quality MP4 video and M4A audio. For X and other platforms, it uses yt-dlp's best format selection. The script saves the result in a well-named folder in your `~/Downloads` directory. For YouTube videos, it also downloads English auto-generated subtitles and converts them to SRT format.

## Features

- Automatically detects the platform (YouTube, X/Twitter, etc.) from the URL.
- For YouTube: Selects the highest quality MP4 video and M4A audio streams.
- For X/Twitter and other platforms: Utilizes yt-dlp's intelligent format selection for the best available quality.
- For YouTube: Downloads English auto-generated subtitles and converts them to SRT.
- Output folder is named as `YYYY.MM.DD - <Video Title>`.
- Output is saved to your `~/Downloads` directory.
- Simple command-line usage.

## Requirements

- Python 3.6+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed and available in your PATH

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

Or, if you made it executable:

```sh
./yt-dlp-wrapper.py "<URL>"
```

The script will:
- Detect the platform from the URL.
- List available formats (for debugging purposes).
- Select the appropriate video/audio formats based on the platform.
- Download the video and audio.
- For YouTube, download and convert English subtitles.
- Save everything to `~/Downloads/YYYY.MM.DD - <Video Title>/`.

## Example

```sh
python yt-dlp-wrapper.py "https://www.youtube.com/watch?v=u2Ftw_VuedA"
```

## Notes

- The script only works with URLs from supported platforms.
- Output folder names are sanitized for filesystem compatibility.
- If no suitable formats are found, the script will print an error.

## License

MIT License

---