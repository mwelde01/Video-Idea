#!/usr/bin/env python3
"""
Process Week 4 video transcripts.

Extracts transcripts from Panopto videos, removes timestamps,
and compiles them into a single narrative document.

Note: Google Drive videos require manual transcript extraction.

Usage:
    python process_week4_transcripts.py
"""

import os
from extract_panopto_transcripts import extract_panopto_transcript

def parse_video_links(filepath='week4_video_links.txt'):
    """Parse the tab-separated video links file"""
    students = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Process all lines (no header in week4 file)
    for line in lines:
        if not line.strip():
            continue

        parts = line.strip().split('\t')
        if len(parts) >= 2:
            student = {
                'name': parts[0].strip(),
                'video_url': parts[1].strip()
            }
            students.append(student)

    return students

def process_all_videos(input_file='week4_video_links.txt', output_file='week4_transcripts.md'):
    """Process all Week 4 videos and compile transcripts"""

    print("="*80)
    print("WEEK 4: VIDEO TRANSCRIPT EXTRACTOR")
    print("="*80)
    print()

    # Read video links
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    students = parse_video_links(input_file)
    print(f"Found {len(students)} students\n")

    # Process each student's video
    results = {}
    total = len(students)
    processed = 0
    google_drive_videos = []

    for student in students:
        processed += 1
        name = student['name']
        url = student['video_url']

        print(f"[{processed}/{total}] Processing: {name}")
        print(f"URL: {url}")

        # Check if it's a Google Drive video
        if 'drive.google.com' in url:
            print("Platform: Google Drive (requires manual transcript)")
            results[name] = "Error: Google Drive video - please extract transcript manually"
            google_drive_videos.append(name)
            print(f"⚠ Manual extraction required")
        else:
            print("Platform: Panopto")
            # Extract transcript
            transcript = extract_panopto_transcript(url)
            results[name] = transcript

            # Show preview
            if transcript and not transcript.startswith("Error") and not transcript.startswith("No"):
                preview = transcript[:150] + "..." if len(transcript) > 150 else transcript
                print(f"✓ Success! Preview: {preview}")
            else:
                print(f"⚠ {transcript}")

        print("-" * 80)
        print()

    # Compile results into markdown document
    print("Compiling results into document...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Week 4: Video Transcripts\n\n")
        f.write("Student video presentations and demonstrations.\n\n")
        f.write("---\n\n")

        # Table of contents
        f.write("## Table of Contents\n\n")
        for name in sorted(results.keys()):
            f.write(f"- [{name}](#{name.lower().replace(' ', '-')})\n")
        f.write("\n---\n\n")

        # Individual student sections
        for name in sorted(results.keys()):
            f.write(f"## {name}\n\n")

            if results[name]:
                if results[name].startswith("Error") or results[name].startswith("No"):
                    f.write(f"*{results[name]}*\n\n")
                else:
                    f.write(f"{results[name]}\n\n")
            else:
                f.write("*No transcript available*\n\n")

            f.write("---\n\n")

    print(f"✓ Compilation complete!")
    print(f"✓ Output saved to: {output_file}")
    print()

    # Summary statistics
    success_count = sum(1 for transcript in results.values()
                       if transcript and not transcript.startswith("Error") and not transcript.startswith("No"))

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total students: {total}")
    print(f"Successfully extracted: {success_count}")
    print(f"Failed/No captions: {total - success_count}")

    if google_drive_videos:
        print(f"\nGoogle Drive videos (require manual extraction):")
        for name in google_drive_videos:
            print(f"  - {name}")
    print()

    if success_count < total:
        print("For videos without captions or Google Drive videos, you can:")
        print("1. Manually copy transcripts from the video platform")
        print("2. Save them as FirstName_LastName_manual.txt")
        print("3. Run: python add_week4_manual_transcripts.py")
        print()

    return results

if __name__ == "__main__":
    process_all_videos()
