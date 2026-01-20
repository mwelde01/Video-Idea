# Panopto Transcript Extractor

A Python script to extract transcripts and closed captions from Panopto videos without timestamps.

## Features

- Extracts transcripts from public/unlisted Panopto videos
- Removes timestamps and formatting to provide clean text
- Supports multiple language codes
- Uses multiple fallback methods for robust extraction
- Works with Panopto's GenerateSRT.ashx endpoint

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python extract_panopto_transcripts.py "https://your-site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID"
```

### Example

```bash
python extract_panopto_transcripts.py "https://louisville.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4335bd73-57a0-4730-b44c-b3d401582ab9"
```

## How It Works

The script uses multiple methods to extract transcripts:

### Method 1: Direct Caption Download
Attempts to download captions directly from Panopto's GenerateSRT.ashx endpoint using various language codes:
- English_USA
- English_GBR
- 0, 1
- en-US, en

URL format: `https://site.panopto.com/Panopto/Pages/Transcription/GenerateSRT.ashx?id=VIDEO-ID&language=LANGUAGE_CODE`

### Method 2: Page Scraping
If direct download fails, the script scrapes the video page HTML to find:
- CaptionDownloadUrl references
- Embedded caption URLs
- GenerateSRT.ashx endpoints in JavaScript

### Method 3: Embedded JSON Data
Searches for transcript data embedded in page JavaScript as JSON objects.

## Output Format

The script returns clean transcript text with:
- No timestamps
- No sequence numbers
- Continuous text with proper spacing

## Limitations

- **Public/Unlisted Videos Only**: The script works best with public or unlisted videos. Private videos may require authentication cookies.
- **Authentication**: The GenerateSRT.ashx endpoint may require authentication cookies for restricted videos. The script does not currently handle authenticated sessions.
- **Caption Availability**: The video must have closed captions or auto-generated captions enabled.

## Troubleshooting

### "No transcript found"
- Verify the video has closed captions enabled
- Check if the video is truly public/unlisted
- Try accessing the video in a browser to confirm captions exist

### "Authentication required"
For private videos, you may need to:
1. Log in to Panopto in your browser
2. Export your session cookies
3. Add cookie support to the script (advanced)

### Network Errors
- Check your internet connection
- Verify the Panopto URL is accessible
- Some institutional firewalls may block programmatic access

## API Alternative

For programmatic access at scale, consider using Panopto's official REST API:

1. Authenticate with your Panopto credentials
2. Call `Sessions_GetSessionById` endpoint
3. Extract the `CaptionDownloadUrl` from the response
4. Download and parse the SRT file

API Documentation: `demo.hosted.panopto.com/Panopto/api/docs/index.html`

## Contributing

Improvements and bug fixes are welcome. Common areas for enhancement:
- Cookie/authentication support for private videos
- Additional language code support
- VTT format parsing
- Batch processing multiple videos

## References

Based on research from:
- Panopto Community discussions on programmatic transcript access
- Panopto REST API documentation
- SRT caption file format specifications

## License

MIT License - Feel free to use and modify as needed.
