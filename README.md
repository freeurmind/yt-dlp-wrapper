# yt-dlp-wrapper

Vibe coding an optimized Python wrapper script for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that intelligently downloads videos from various platforms including YouTube and X (Twitter). The script features robust error handling, multiple browser support, and smart format selection with codec preferences (av01 > vp9 > avc1). It organizes downloads in well-named folders and includes comprehensive logging.

## Features

- **Smart Format Selection**: Optimized format selector with resolution priority (4K > 2K > 1080p > 720p) and codec preference (av01 > vp9 > avc1)
- **Premium Format Detection**: Automatically detects and uses YouTube Premium formats when available
- **Multi-Browser Support**: Extract cookies from Firefox, Chrome, or Safari for authenticated downloads
- **Robust Error Handling**: Comprehensive validation, timeout protection, and graceful failure handling
- **Multi-Platform Support**: Works with YouTube, X (Twitter), and other platforms supported by yt-dlp
- **Subtitle Download**: Downloads English auto-generated subtitles and converts them to SRT format
- **Organized Output**: Creates folders named `YYYY.MM.DD - <Video Title>` in your `~/Downloads` directory
- **Advanced Logging**: Configurable logging levels with detailed progress information
- **Custom Format Support**: Override default format selection with custom selectors
- **Dependency Validation**: Automatic checking of required tools and browsers
- **Timeout Protection**: Prevents hanging on long operations
- **YouTube SABR Support**: Handles YouTube's Server-side Adaptive Bitrate streaming protocol

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

**Handle YouTube SABR streaming issues:**
```sh
python yt-dlp-wrapper.py "URL" --youtube-client android
```

**Enable SABR format support:**
```sh
python yt-dlp-wrapper.py "URL" --enable-sabr
```

**Disable Premium format detection:**
```sh
python yt-dlp-wrapper.py "URL" --no-premium
```

### Command-Line Options

- `--format, -f`: Custom format selector (overrides default smart selection)
- `--browser, -b`: Browser to extract cookies from (firefox, chrome, safari)
- `--verbose, -v`: Enable detailed logging output
- `--youtube-client, -y`: YouTube client to use (web, android, tv, web_music, android_music)
- `--enable-sabr`: Enable YouTube SABR streaming format support
- `--no-fallback`: Disable automatic fallback to other YouTube clients
- `--no-premium`: Disable automatic selection of Premium formats
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
- **YouTube Client Fallback**: Automatically tries alternative YouTube clients if the default fails

## YouTube SABR Streaming

Starting in 2025, YouTube began rolling out a new streaming protocol called SABR (Server-side Adaptive Bitrate), which has impacted tools like yt-dlp. When YouTube serves content via SABR, traditional download methods may fail or only retrieve lower quality formats.

This wrapper includes features to handle SABR streaming:

1. **Automatic Client Fallback**: If a download fails due to SABR restrictions, the wrapper will automatically try alternative YouTube clients (android, tv) that may still provide traditional formats.

2. **Manual Client Selection**: You can manually specify which YouTube client to use with `--youtube-client`. Using `android` or `tv` often avoids SABR restrictions.

3. **SABR Support**: If needed, you can enable SABR format support with `--enable-sabr`. This requires a recent version of yt-dlp that supports SABR.

4. **Error Detection**: The wrapper automatically detects SABR-related errors and provides appropriate fallback solutions.

If you encounter download failures with YouTube, try using:
```sh
python yt-dlp-wrapper.py "URL" --youtube-client android
```

Or for more recent videos where SABR is fully enforced:
```sh
python yt-dlp-wrapper.py "URL" --enable-sabr
```

## YouTube Premium Formats

The wrapper automatically detects and prioritizes YouTube Premium formats when available. Premium formats (such as format ID 616) often provide better quality video with enhanced bitrates.

Key features of the Premium format detection:

1. **Automatic Detection**: The wrapper scans the available formats and automatically selects Premium formats when detected.

2. **Smart Premium Quality**: When multiple Premium formats are available, automatically selects the one with the highest resolution.

3. **Manual Control**: You can disable Premium format selection with `--no-premium` if you prefer to use the default format selector.

4. **Best Audio Pairing**: When using Premium video formats, the wrapper automatically selects the best available audio to pair with it.

This feature is particularly useful for high-quality archiving of YouTube content that includes Premium format options.

## License

MIT License

---