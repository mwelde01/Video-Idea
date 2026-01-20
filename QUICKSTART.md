# Quick Start Guide

## Installation

```bash
pip install -r requirements.txt
```

## Use Cases

### 1. Extract Single Video Transcript

**Command:**
```bash
python extract_panopto_transcripts.py "https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID"
```

**Example:**
```bash
python extract_panopto_transcripts.py "https://louisville.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4335bd73-57a0-4730-b44c-b3d401582ab9"
```

### 2. Extract Multiple Videos (Batch Processing)

**Step 1:** Create a text file with URLs (one per line)
```
https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID-1
https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID-2
https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID-3
```

**Step 2:** Run batch extractor
```bash
python batch_extract.py urls.txt transcripts
```

This will create a `transcripts/` directory with individual .txt files for each video.

### 3. Save Transcript to File

**Use the example script:**
```python
from extract_panopto_transcripts import extract_panopto_transcript

url = "https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID"
transcript = extract_panopto_transcript(url)

with open("my_transcript.txt", "w") as f:
    f.write(transcript)
```

### 4. Use in Your Python Code

```python
from extract_panopto_transcripts import extract_panopto_transcript

url = "https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID"
transcript = extract_panopto_transcript(url)

if not transcript.startswith("Error"):
    # Process the transcript
    print(f"Got transcript with {len(transcript.split())} words")
```

## Direct Caption URL Method

If you know the exact caption URL:

```bash
curl "https://site.panopto.com/Panopto/Pages/Transcription/GenerateSRT.ashx?id=VIDEO-ID&language=English_USA" -o transcript.srt
```

Then parse the SRT file to remove timestamps.

## Understanding the Output

The script returns **clean text** with:
- ✓ No timestamps
- ✓ No sequence numbers
- ✓ Continuous readable text
- ✓ Proper spacing between sentences

## Troubleshooting

| Error | Solution |
|-------|----------|
| "No transcript found" | Video may not have captions enabled |
| "Authentication required" | Video is private, not public/unlisted |
| "Could not extract video ID" | Check URL format is correct |
| Network errors | Check internet connection and firewall settings |

## Caption URL Format Reference

Standard Panopto caption URL:
```
https://[SITE].panopto.com/Panopto/Pages/Transcription/GenerateSRT.ashx?id=[VIDEO-ID]&language=[LANG]
```

Common language codes:
- `English_USA`
- `English_GBR`
- `0` or `1`
- `en-US`
- `en`

## File Structure

```
.
├── extract_panopto_transcripts.py  # Main extraction script
├── batch_extract.py                # Batch processing tool
├── example_usage.py                # Usage examples
├── panopto_api_example.py         # REST API approach
├── requirements.txt                # Python dependencies
├── README.md                       # Full documentation
└── example_urls.txt               # Example URL list
```

## Next Steps

1. **Single video**: Use `extract_panopto_transcripts.py` directly
2. **Multiple videos**: Use `batch_extract.py` with a URL list file
3. **Integration**: Import the functions into your own Python code
4. **Production use**: Consider the REST API approach (see `panopto_api_example.py`)

## Getting Help

- Check `README.md` for detailed documentation
- Review `example_usage.py` for code examples
- See Panopto Community discussions (links in README.md)
- Review Panopto REST API documentation
