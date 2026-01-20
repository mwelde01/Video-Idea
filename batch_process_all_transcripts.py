#!/usr/bin/env python3
"""
Batch process all student video transcripts from Panopto and Google Drive.
Compiles them into a single organized document in narrative format.
"""

import sys
import os
from extract_panopto_transcripts import extract_panopto_transcript, parse_srt_content
import requests
from urllib.parse import urlparse, parse_qs

def extract_google_drive_transcript(url):
    """
    Extract transcript from Google Drive video.
    Note: Google Drive videos may not have auto-generated captions.
    This function attempts to use yt-dlp to extract any available captions.
    """
    import subprocess

    # Extract file ID from Google Drive URL
    try:
        if 'drive.google.com' in url:
            if '/file/d/' in url:
                file_id = url.split('/file/d/')[1].split('/')[0]
            else:
                parsed = urlparse(url)
                params = parse_qs(parsed.query)
                file_id = params.get('id', [None])[0]

            if not file_id:
                return "Error: Could not extract Google Drive file ID"

            print(f"Google Drive File ID: {file_id}")
            print("Attempting to extract transcript using yt-dlp...")

            # Try to extract subtitles using yt-dlp
            cmd = [
                'yt-dlp',
                '--skip-download',
                '--write-auto-sub',
                '--write-sub',
                '--sub-format', 'vtt',
                '--output', f'temp_gdrive_{file_id}',
                '--no-warnings',
                url
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

                # Check if subtitle file was created
                subtitle_files = [f for f in os.listdir('.') if f.startswith(f'temp_gdrive_{file_id}') and f.endswith('.vtt')]

                if subtitle_files:
                    with open(subtitle_files[0], 'r', encoding='utf-8') as f:
                        srt_content = f.read()

                    # Clean up
                    os.remove(subtitle_files[0])

                    # Parse and return transcript
                    return parse_srt_content(srt_content)
                else:
                    return "No captions available for this Google Drive video. Manual transcription may be required."

            except subprocess.TimeoutExpired:
                return "Error: Timeout while extracting Google Drive transcript"
            except Exception as e:
                return f"Error extracting Google Drive transcript: {str(e)}"

    except Exception as e:
        return f"Error: {str(e)}"

def process_all_videos(input_file='video_links.txt', output_file='compiled_transcripts.md'):
    """Process all videos and compile transcripts into one document"""

    print("="*80)
    print("AI CASE VIDEO TRANSCRIPT EXTRACTOR")
    print("="*80)
    print()

    # Read video links
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    # Parse video information
    videos = []
    for line in lines:
        parts = line.split('|')
        if len(parts) == 3:
            student, case_type, url = parts
            videos.append({
                'student': student.strip(),
                'case_type': case_type.strip(),
                'url': url.strip()
            })

    print(f"Found {len(videos)} videos to process\n")

    # Group by student
    students = {}
    for video in videos:
        student = video['student']
        if student not in students:
            students[student] = {'Positive': None, 'Negative': None}
        students[student][video['case_type']] = video['url']

    # Process each student's videos
    results = {}
    total = len(videos)
    processed = 0

    for student, urls in sorted(students.items()):
        results[student] = {'Positive': None, 'Negative': None}

        for case_type in ['Positive', 'Negative']:
            if urls[case_type]:
                processed += 1
                print(f"[{processed}/{total}] Processing: {student} - {case_type} AI Case")
                print(f"URL: {urls[case_type]}")

                # Determine video platform and extract transcript
                if 'drive.google.com' in urls[case_type]:
                    print("Platform: Google Drive")
                    transcript = extract_google_drive_transcript(urls[case_type])
                elif 'panopto.com' in urls[case_type]:
                    print("Platform: Panopto")
                    transcript = extract_panopto_transcript(urls[case_type])
                else:
                    transcript = "Unknown video platform"

                results[student][case_type] = transcript

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
        f.write("# AI Case Video Transcripts\n\n")
        f.write("Compiled transcripts from student video presentations.\n\n")
        f.write("---\n\n")

        # Table of contents
        f.write("## Table of Contents\n\n")
        for student in sorted(students.keys()):
            f.write(f"- [{student}](#{student.lower().replace(' ', '-')})\n")
        f.write("\n---\n\n")

        # Individual student sections
        for student in sorted(students.keys()):
            f.write(f"## {student}\n\n")

            # Positive AI Case
            f.write(f"### Positive AI Case\n\n")
            if results[student]['Positive']:
                if results[student]['Positive'].startswith("Error") or results[student]['Positive'].startswith("No"):
                    f.write(f"*{results[student]['Positive']}*\n\n")
                else:
                    f.write(f"{results[student]['Positive']}\n\n")
            else:
                f.write("*No video submitted*\n\n")

            # Negative AI Case
            f.write(f"### Negative AI Case\n\n")
            if results[student]['Negative']:
                if results[student]['Negative'].startswith("Error") or results[student]['Negative'].startswith("No"):
                    f.write(f"*{results[student]['Negative']}*\n\n")
                else:
                    f.write(f"{results[student]['Negative']}\n\n")
            else:
                f.write("*No video submitted*\n\n")

            f.write("---\n\n")

    print(f"✓ Compilation complete!")
    print(f"✓ Output saved to: {output_file}")
    print()

    # Summary statistics
    success_count = sum(1 for student in results.values()
                       for transcript in student.values()
                       if transcript and not transcript.startswith("Error") and not transcript.startswith("No"))

    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total videos: {total}")
    print(f"Successfully extracted: {success_count}")
    print(f"Failed/No captions: {total - success_count}")
    print()

    return results

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'video_links.txt'
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'compiled_transcripts.md'

    process_all_videos(input_file, output_file)
