# yt-dlp-wrapper

Vibe coding an optimized Python wrapper script for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that intelligently downloads videos from various platforms including YouTube and X (Twitter). The script features robust error handling, multiple browser support, and smart format selection with codec preferences (av01 > vp9 > avc1). It organizes downloads in well-named folders and includes comprehensive logging.

## Features

- **Smart Format Selection**: Optimized format selector with resolution priority (4K > 2K > 1080p > 720p) and codec preference (av01 > vp9 > avc1)
- **Multi-Browser Support**: Extract cookies from Firefox, Chrome, or Safari for authenticated downloads
- **Robust Error Handling**: Comprehensive validation, timeout protection, and graceful failure handling
- **Multi-Platform Support**: Works with YouTube, X (Twitter), and other platforms supported by yt-dlp
- **Subtitle Download**: Downloads English auto-generated subtitles and converts them to SRT format
- **Organized Output**: Creates folders named `YYYY.MM.DD - <Video Title>` in your `~/Downloads` directory
- **Advanced Logging**: Configurable logging levels with detailed progress information
- **Custom Format Support**: Override default format selection with custom selectors
- **Dependency Validation**: Automatic checking of required tools and browsers
- **Timeout Protection**: Prevents hanging on long operations

## Format Selection Strategy

The script uses yt-dlp's advanced format selector with the following priority:

1. **Resolution Priority**: 4K (2160p) → 2K (1440p) → 1080p → 720p
2. **Codec Priority**: Within each resolution, prefers av01 > vp9 > avc1
3. **Fallback**: Best available format if preferred options aren't available

## Requirements

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) installed and available in your PATH
- At least one supported browser: Firefox, Chrome, or Safari (for cookie extraction)

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

### Basic Usage

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

### Advanced Options

**Custom format selection:**
```sh
python yt-dlp-wrapper.py "URL" --format "best[height<=720]"
```

**Use different browser for cookies:**
```sh
python yt-dlp-wrapper.py "URL" --browser chrome
python yt-dlp-wrapper.py "URL" --browser safari
```

**Enable verbose logging:**
```sh
python yt-dlp-wrapper.py "URL" --verbose
```

**Combine options:**
```sh
python yt-dlp-wrapper.py "URL" --browser chrome --format "best[height<=1080]" --verbose
```

### Command-Line Options

- `--format, -f`: Custom format selector (overrides default smart selection)
- `--browser, -b`: Browser to extract cookies from (firefox, chrome, safari)
- `--verbose, -v`: Enable detailed logging output
- `--help, -h`: Show help message with examples

### Pass-through Arguments

You can pass additional yt-dlp arguments directly:
```sh
python yt-dlp-wrapper.py "URL" --write-description --write-thumbnail
```

## What the script does

1. **Validates dependencies** - Checks for yt-dlp and browser availability
2. **Detects platform** from the URL (YouTube, X/Twitter, or other)
3. **Extracts cookies** from your chosen browser for authenticated access
4. **Fetches video metadata** to get title and upload date with timeout protection
5. **Creates output directory** with organized naming and length limits
6. **Downloads video** using optimized format selector with codec preferences
7. **Downloads subtitles** and converts to SRT format
8. **Embeds metadata** in the downloaded video file
9. **Provides detailed logging** throughout the process

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

- **Browser Support**: Defaults to Firefox but supports Chrome and Safari via `--browser` option
- **Error Handling**: Script validates dependencies on startup and provides clear error messages
- **Timeout Protection**: 5-minute timeout for metadata fetching, 1-hour timeout for downloads
- **Output Organization**: Folder names are sanitized and limited to 100 characters for filesystem compatibility
- **Logging**: Uses proper logging levels (INFO by default, DEBUG with `--verbose`)
- **Exit Codes**: Returns proper exit codes (0 for success, 1 for failure) for scripting
- **Metadata Embedding**: Automatically embeds video metadata in downloaded files
- **Format Selection**: Uses optimized regex-based format selector for better performance
- **Graceful Degradation**: Continues working even if browser cookies aren't available

## License

MIT License

---