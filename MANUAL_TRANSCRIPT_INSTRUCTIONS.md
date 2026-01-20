# How to Add Manual Transcripts

If some videos didn't have transcripts available, you can manually add them using this process.

## Step 1: Get the Missing Transcripts

For each video that's missing a transcript:

1. Open the video in your browser (Panopto or Google Drive)
2. Look for the "Captions" or "CC" tab/button
3. Copy ALL the caption text (including timestamps - the script will remove them)
4. Or, if you need to manually transcribe, just type out what's said in the video

## Step 2: Save as Text Files

Save each transcript as a text file with this naming format:

```
FirstName_LastName_CaseType_manual.txt
```

**Important:**
- Use underscores `_` between words (not spaces)
- Case type must be exactly `Positive` or `Negative` (capital P or N)
- Must end with `_manual.txt`

### Examples:

- `Emma_Frank_Positive_manual.txt`
- `Emma_Frank_Negative_manual.txt`
- `Xanny_Frazier_Positive_manual.txt`
- `Charles_Barr_Positive_manual.txt`

### Save Location:

Save these files in the **same folder** as `compiled_transcripts.md` (your Video-Idea repository folder)

## Step 3: What the Text File Should Contain

Just paste the raw captions - timestamps and all! For example:

```
1
00:00:00 --> 00:00:03
Hello everyone, today I'm going to talk about

2
00:00:03 --> 00:00:07
artificial intelligence in healthcare.

3
00:00:07 --> 00:00:12
This is an example of a positive AI case...
```

OR if you're typing it yourself:

```
Hello everyone, today I'm going to talk about artificial intelligence in healthcare. This is an example of a positive AI case...
```

The script handles both formats!

## Step 4: Run the Script

Open Command Prompt in your Video-Idea folder and run:

```cmd
python add_manual_transcripts.py
```

## What the Script Does:

1. **Finds** all your `*_manual.txt` files
2. **Cleans** them by removing:
   - Timestamp lines (00:00:12 --> 00:00:15)
   - Sequence numbers (1, 2, 3...)
   - Inline timestamps [00:12] or (0:12)
3. **Converts** to narrative format (continuous text)
4. **Updates** `compiled_transcripts.md` by replacing error messages with the cleaned transcript

## Expected Output:

```
================================================================================
MANUAL TRANSCRIPT PROCESSOR
================================================================================

Found 4 manual transcript file(s):

  Emma Frank:
    - Positive AI Case: Emma_Frank_Positive_manual.txt
    - Negative AI Case: Emma_Frank_Negative_manual.txt

Processing: Emma Frank
  Found section for: Emma Frank
    Processing Positive AI Case from Emma_Frank_Positive_manual.txt
    ✓ Updated Positive AI Case
    Processing Negative AI Case from Emma_Frank_Negative_manual.txt
    ✓ Updated Negative AI Case

================================================================================
✓ Successfully updated 2 transcript(s) in compiled_transcripts.md
================================================================================
```

## Troubleshooting

### "No manual transcript files found"

Make sure:
- Files end with `_manual.txt`
- Files are in the same folder as the script
- Filename format is correct: `FirstName_LastName_CaseType_manual.txt`

### "No updates were made"

Check that:
- Student name in filename matches the name in `compiled_transcripts.md` exactly
- Case type is `Positive` or `Negative` (capital first letter)
- The student section exists in `compiled_transcripts.md`

### Name doesn't match

If the name in your filename doesn't match the compiled document, you can:
1. Rename your file to match
2. Or edit the script to handle variations

For example, if the document says "Rabija Efendira" but you typed "Rabija_Efendira" - that should work. But "R_Efendira" won't work because it's too different.

## Quick Reference

### File Naming Examples:
✅ `Charles_Barr_Positive_manual.txt`
✅ `Emma_Frank_Negative_manual.txt`
✅ `Xanny_Frazier_Positive_manual.txt`

❌ `charles barr positive.txt` (spaces, no _manual)
❌ `Emma_Frank_positive_manual.txt` (lowercase 'p')
❌ `Barr_Positive_manual.txt` (missing first name)

### Commands:
```cmd
# Install requirements (if you haven't already)
python -m pip install -r requirements.txt

# Process manual transcripts
python add_manual_transcripts.py

# View the updated document
notepad compiled_transcripts.md
```
