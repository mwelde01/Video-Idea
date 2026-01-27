#!/usr/bin/env python3
"""
Process Week 2 AI Tool Use video transcripts.

Extracts transcripts from Panopto videos, removes timestamps,
and compiles them into a single narrative document.

Usage:
    python process_week2_transcripts.py
"""

import os
from extract_panopto_transcripts import extract_panopto_transcript

def parse_video_links(filepath='week2_video_links.txt'):
    """Parse the tab-separated video links file"""
    students = []

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Skip header
    for line in lines[1:]:
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

def process_all_videos(input_file='week2_video_links.txt', output_file='week2_ai_tool_use_transcripts.md'):
    """Process all Week 2 videos and compile transcripts"""

    print("="*80)
    print("WEEK 2: AI TOOL USE TRANSCRIPT EXTRACTOR")
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

    for student in students:
        processed += 1
        name = student['name']
        url = student['video_url']

        print(f"[{processed}/{total}] Processing: {name}")
        print(f"URL: {url}")
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
        f.write("# Week 2: AI Tool Use Video Transcripts\n\n")
        f.write("Student presentations on AI tool usage and applications.\n\n")
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
    print()

    if success_count < total:
        print("For videos without captions, you can:")
        print("1. Manually copy transcripts from Panopto")
        print("2. Save them as StudentName_manual.txt")
        print("3. Run: python add_week2_manual_transcripts.py")
        print()

    return results

if __name__ == "__main__":
    process_all_videos()
