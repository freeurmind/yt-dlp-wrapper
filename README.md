# yt-dlp-wrapper

A simple Python wrapper script for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that downloads the highest quality MP4 video and M4A audio from a YouTube URL, saving the result in a well-named folder in your `~/Downloads` directory. It also downloads English auto-generated subtitles and converts them to SRT format.

## Features

- Automatically selects the highest quality MP4 video and M4A audio streams.
- Downloads English auto-generated subtitles and converts them to SRT.
- Output folder is named as `YYYY.MM.DD - <YouTube Video Title>`.
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

Run the script with a YouTube URL:

```sh
python yt-dlp-wrapper.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

Or, if you made it executable:

```sh
./yt-dlp-wrapper.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

The script will:
- List available formats,
- Select the best MP4 video and M4A audio,
- Download the video and audio,
- Download and convert English subtitles,
- Save everything to `~/Downloads/YYYY.MM.DD - <Video Title>/`.

## Example

```sh
python yt-dlp-wrapper.py "https://www.youtube.com/watch?v=u2Ftw_VuedA"
```

## Notes

- The script only works with YouTube URLs.
- Output folder names are sanitized for filesystem compatibility.
- If no suitable formats are found, the script will print an error.

## License

MIT License

---