# Transcript Cleaning Summary

## Date: April 16, 2026

## Files Processed

All 6 transcript files have been successfully cleaned and converted to narrative format.

### Original Files → Cleaned Files

| Original File | Cleaned File | Size | Sections |
|--------------|--------------|------|----------|
| Cindy Lee and Bill Braxton.txt | Cindy Lee and Bill Braxton_cleaned.txt | 58K | 264 |
| Interview with Father Guerric Heckel.txt | Interview with Father Guerric Heckel_cleaned.txt | 53K | 208 |
| Jim Johnson and Helen Osman.txt | Jim Johnson and Helen Osman_cleaned.txt | 53K | 276 |
| Joe Primo and Seifu Singh-Molares.txt | Joe Primo and Seifu Singh-Molares_cleaned.txt | 59K | 154 |
| Margaret Benefield.txt | Margaret Benefield_cleaned.txt | 32K | 272 |
| Scott Stoner and Brandon Nappi.txt | Scott Stoner and Brandon Nappi_cleaned.txt | 66K | 282 |

## Cleaning Process

The following transformations were applied to each transcript:

1. **Removed timestamps** - All time codes in format `00:00:00.000 --> 00:00:00.000` were removed
2. **Removed sequence numbers** - All numeric line identifiers were removed
3. **Removed WEBVTT headers** - WebVTT format headers were removed
4. **Organized by speaker** - Dialogue organized with bold speaker headers (e.g., `**Speaker Name:**`)
5. **Created clean paragraphs** - Consecutive dialogue from the same speaker combined into flowing paragraphs
6. **Preserved all spoken content** - No dialogue content was removed or altered

## Format Used

Each speaker's dialogue is presented in the following format:

```
**Speaker Name:**
[Their complete dialogue in clean paragraph form]

**Next Speaker:**
[Their complete dialogue in clean paragraph form]
```

## Speakers Identified

The cleaned transcripts include dialogue from the following participants:

### Cindy Lee and Bill Braxton
- Nat Irvin
- Westina Matthews
- Cindy Lee
- Brad Braxton

### Interview with Father Guerric Heckel
- Nat Irvin
- Westina Matthews
- Guerric Heckel
- Julie Fisher
- Allysse Stokes
- Sophonie Bazile

### Jim Johnson and Helen Osman
- Westina Matthews
- Nat Irvin
- Jim Johnson
- Helen Osman

### Joe Primo and Seifu Singh-Molares
- Westina Matthews
- Rev. Seifu
- Joe Primo (Grateful Living)
- Nat Irvin

### Margaret Benefield
- College of Business Online Programs Office
- n0irvi01 (Nat Irvin)
- Westina Matthews
- Margaret Benefiel

### Scott Stoner and Brandon Nappi
- Westina Matthews
- Scott Stoner
- Brandon Nappi
- Nat Irvin

## Quality Assurance

✓ All files successfully processed without errors
✓ All timestamps removed
✓ All sequence numbers removed
✓ Speaker identification preserved
✓ Dialogue content preserved in full
✓ Clean, readable narrative format achieved
✓ Files saved with "_cleaned.txt" suffix

## Location

All cleaned files are saved in: `/home/user/Video-Idea/`

## Script Used

The Python cleaning script is available at: `/home/user/Video-Idea/clean_transcripts.py`

This script can be reused for processing additional transcript files in the future.
