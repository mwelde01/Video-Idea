# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This repository serves two primary purposes:

1. **Video Transcript Extraction & Processing** - Tools for extracting transcripts from Panopto videos and converting them to clean, readable formats
2. **Educational Content Management** - Managing and organizing video transcripts for multiple educational courses, including:
   - "The Soul of Management" MBA course (spirituality, leadership, core values)
   - AI/Technology courses covering ethics, tools, and case studies
   - Guest lecture series and interviews

## Tech Stack

- **Python 3.6+** - Core language
- **requests** - HTTP requests for video transcript extraction
- **beautifulsoup4 + lxml** - HTML parsing and web scraping
- **yt-dlp** - Video download capabilities (if needed)
- **Standard library** - re, pathlib, os for file operations

## Key Architecture & Conventions

### File Organization Patterns

The repository uses a **flat file structure** with naming conventions to organize content:

**Raw Transcripts** (with timestamps):
- Format: `[Name/Topic].txt`
- Contains VTT/SRT format with timestamps and sequence numbers
- Examples: `Rev. Michael Curry.txt`, `Jim Johnson and Helen Osman.txt`

**Cleaned Transcripts** (narrative format):
- Format: `[Name/Topic]_cleaned.txt`
- No timestamps, organized by speaker with bold headers
- Examples: `Rev. Michael Curry_cleaned.txt`, `Cindy Lee and Bill Braxton_cleaned.txt`

**Manual Transcripts**:
- Format: `[Student_Name]_manual.txt` or `[Student_Name]_[Type]_manual.txt`
- Used for manually created content that bypasses automated extraction

**Week-based Organization**:
- `week[N]_transcripts.md` - Compiled transcripts for a specific week
- `week[N]_video_links.txt` - URL lists for batch processing

### Transcript Processing Pipeline

**1. Extraction** (`extract_panopto_transcripts.py`):
- Extracts transcripts from Panopto video URLs
- Uses multiple fallback methods (direct download → scraping → JSON parsing)
- Tries various language codes: English_USA, English_GBR, 0, 1, en-US, en

**2. Cleaning** (`clean_transcripts.py`):
- Removes timestamps (format: `00:00:00.000 --> 00:00:00.000`)
- Removes sequence numbers and WEBVTT headers
- Organizes by speaker with format: `**Speaker Name:**\n[dialogue]\n\n`
- Combines consecutive dialogue from same speaker into paragraphs

**3. Compilation** (various `process_week[N]_transcripts.py`):
- Aggregates multiple transcripts into markdown files
- Organizes by student name or topic
- Creates table of contents

**4. Reorganization** (`reorganize_by_case_type.py`):
- Alternative organization schemes (e.g., by case type: Positive/Negative AI Cases)
- Reads from master `compiled_transcripts.md`
- Generates alternative views on demand

### Core Processing Functions

**When adding new transcript processing scripts:**

```python
def clean_transcript(input_file, output_file):
    """
    Standard signature for transcript cleaning.
    
    Process flow:
    1. Read file line by line
    2. Skip empty lines, WEBVTT, timestamps (-->), sequence numbers
    3. Parse "Speaker: dialogue" format
    4. Group consecutive dialogue by speaker
    5. Write with **Speaker:** headers
    """
    pass

def extract_video_id(url):
    """Extract video ID from Panopto URL using regex"""
    pass

def parse_srt_content(srt_text):
    """Remove timestamps and numbers from SRT format"""
    pass
```

### Batch Processing Convention

All batch scripts follow this pattern:

1. Read URLs/files from input (text file with one item per line)
2. Create output directory if needed
3. Process each item with error handling
4. Report success/failure counts
5. Save individual files with sanitized names

Example:
```bash
python batch_extract.py video_links.txt transcripts/
```

## Important Workflows

### Adding New Video Transcripts

**Method 1: Automated Extraction (Panopto)**
```bash
# Single video
python extract_panopto_transcripts.py "https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID"

# Multiple videos
# 1. Create URL list file
# 2. Run batch extraction
python batch_extract.py video_urls.txt output_dir/
```

**Method 2: Manual Transcripts**
```bash
# 1. Create manual transcript file: Student_Name_manual.txt
# 2. Run appropriate processor
python add_manual_transcripts.py  # Updates compiled_transcripts.md
```

### Cleaning Existing Transcripts

```bash
# Process specific files
python clean_transcripts.py  # Processes hardcoded list

# Or use the function directly in Python
from clean_transcripts import clean_transcript
clean_transcript("input.txt", "output_cleaned.txt")
```

### Course Content Management

**For "Soul of Management" lectures:**
- Guest speakers stored as: `[Speaker Names].txt` (raw)
- Cleaned versions: `[Speaker Names]_cleaned.txt`
- Multiple speakers separated in filename with "and"

**For AI course content:**
- Organized by week: `week2_`, `week4_`, `week5_`
- Topic-based files: `[Topic Title].txt`
- Case studies may include student names

## File Naming Conventions

**DO:**
- Use descriptive names: `Interview with Father Guerric Heckel.txt`
- Preserve speaker names in guest lectures
- Use underscores for programmatic suffixes: `_cleaned`, `_manual`
- Include week numbers for course content: `week4_transcripts.md`

**DON'T:**
- Use special characters: `<>:"/\|?*`
- Mix naming conventions within a batch
- Forget the `_cleaned` suffix for processed files

## Testing

Run test scripts to verify parsing:
```bash
python test_srt_parser.py  # Tests SRT timestamp removal
```

## Network Limitations

The Panopto extraction scripts may fail with `403 Forbidden` errors in restricted environments. This is expected - the code works correctly in unrestricted local environments.

## Common Tasks

**Clean a new transcript:**
```python
from clean_transcripts import clean_transcript
clean_transcript("new_lecture.txt", "new_lecture_cleaned.txt")
```

**Add to weekly compilation:**
1. Place raw transcript in repo
2. Update appropriate `process_week[N]_transcripts.py`
3. Run script to regenerate compiled markdown

**Reorganize content:**
```bash
python reorganize_by_case_type.py  # Regenerates case-type view
```

## Code Style

- Use docstrings for all functions
- Handle errors gracefully with try/except
- Print progress messages for batch operations
- Sanitize filenames before writing
- Use pathlib for cross-platform paths when possible

## Git Workflow

- Work on feature branches: `claude/[task-description]-[id]`
- Commit cleaned files separately from raw files
- Include session URL in commit messages
- Push changes to remote branch when complete
