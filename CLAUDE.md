# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python wrapper script for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that provides intelligent video downloading from YouTube, X (Twitter), and other platforms. The project consists of a single Python script (`yt-dlp-wrapper.py`) with no build system or testing framework.

## Key Components

### Main Script: `yt-dlp-wrapper.py`
- **VideoDownloader class**: Core functionality for downloading videos
- **Platform detection**: Automatically detects YouTube, X/Twitter, or other platforms
- **Smart format selection**: Prioritizes 4K→2K→1080p→720p with codec preference (av01 > vp9 > avc1)
- **Cookie extraction**: Supports Firefox, Chrome, Safari browsers for authenticated downloads
- **Error handling**: Comprehensive validation and timeout protection
- **Output organization**: Creates dated folders in `~/Downloads/YYYY.MM.DD - <Video Title>/`

### Configuration Constants
- `DEFAULT_FORMAT_SELECTOR`: Complex format selector string prioritizing resolution and codec
- `SUPPORTED_PLATFORMS`: Platform detection mapping for YouTube, X/Twitter

## Common Development Commands

### Running the Script
```bash
python yt-dlp-wrapper.py "https://www.youtube.com/watch?v=VIDEO_ID"
python yt-dlp-wrapper.py "URL" --browser chrome --format "best[height<=1080]" --verbose
```

### Dependencies
- **Python 3.7+** required
- **yt-dlp** must be installed and in PATH: `pip install -U yt-dlp`
- **Browser** (Firefox, Chrome, or Safari) for cookie extraction

### Testing
No formal testing framework is configured. Test manually with various video URLs from different platforms.

## Architecture Notes

### Command Line Interface
Uses `argparse` with `parse_known_args()` to forward unknown arguments directly to yt-dlp, enabling pass-through of additional yt-dlp options.

### Error Handling Strategy
- Custom `YtDlpWrapperError` exception for wrapper-specific errors
- Timeout protection: 5 minutes for metadata, 1 hour for downloads
- Graceful degradation when browser cookies unavailable
- Proper exit codes (0 for success, 1 for failure)

### Video Processing Flow
1. Validate dependencies (yt-dlp, browser availability)
2. Detect platform from URL
3. Extract video metadata with timeout protection
4. Create organized output directory with sanitized names
5. Download video with optimized format selector
6. Download and convert subtitles to SRT
7. Embed metadata in video file

### Format Selection Logic
Uses regex-based format selector prioritizing:
- Resolution: 4K (2160p) → 2K (1440p) → 1080p → 720p
- Codec: av01 > vp9 > avc1 within each resolution
- Fallback to best available format

## File Organization

- **Single script architecture**: All functionality in `yt-dlp-wrapper.py`
- **No build system**: Direct Python execution
- **No configuration files**: All settings are constants in the script
- **Minimal dependencies**: Only standard library + yt-dlp

## Development Considerations

- The script is designed for direct execution, not as a package
- No unit tests - rely on manual testing with real URLs
- Logging uses Python's standard logging module (INFO level default, DEBUG with --verbose)
- File operations use pathlib for cross-platform compatibility
- Browser cookie extraction paths are hardcoded for common locations