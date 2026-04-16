#!/usr/bin/env python3
"""
Clean transcript files by removing timestamps and sequence numbers,
organizing by speaker with bold headers.
"""

import re
from pathlib import Path

def clean_transcript(input_file, output_file):
    """
    Process a transcript file to remove timestamps and organize by speaker.

    Args:
        input_file: Path to input transcript file
        output_file: Path to output cleaned file
    """
    print(f"Processing {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Variables to track current speaker and their dialogue
    current_speaker = None
    speaker_dialogue = []
    cleaned_content = []

    # Process each line
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines, WEBVTT headers, and sequence numbers
        if not line or line == 'WEBVTT' or line.isdigit():
            i += 1
            continue

        # Skip timestamp lines (format: 00:00:00.000 --> 00:00:00.000)
        if '-->' in line:
            i += 1
            continue

        # Check if line contains speaker dialogue (format: "Speaker Name: dialogue text")
        if ':' in line:
            parts = line.split(':', 1)
            if len(parts) == 2:
                speaker_name = parts[0].strip()
                dialogue_text = parts[1].strip()

                # If this is a new speaker, save previous speaker's dialogue
                if speaker_name != current_speaker:
                    if current_speaker and speaker_dialogue:
                        # Add the previous speaker's section
                        cleaned_content.append(f"**{current_speaker}:**\n")
                        cleaned_content.append(' '.join(speaker_dialogue) + '\n\n')

                    # Start new speaker
                    current_speaker = speaker_name
                    speaker_dialogue = [dialogue_text] if dialogue_text else []
                else:
                    # Same speaker, accumulate dialogue
                    if dialogue_text:
                        speaker_dialogue.append(dialogue_text)

        i += 1

    # Don't forget the last speaker's dialogue
    if current_speaker and speaker_dialogue:
        cleaned_content.append(f"**{current_speaker}:**\n")
        cleaned_content.append(' '.join(speaker_dialogue) + '\n\n')

    # Write cleaned content to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(cleaned_content)

    print(f"Created {output_file}")
    return len(cleaned_content)

def main():
    """Process all 6 transcript files."""

    base_dir = Path('/home/user/Video-Idea')

    # List of files to process
    files_to_process = [
        'Cindy Lee and Bill Braxton.txt',
        'Interview with Father Guerric Heckel.txt',
        'Jim Johnson and Helen Osman.txt',
        'Joe Primo and Seifu Singh-Molares.txt',
        'Margaret Benefield.txt',
        'Scott Stoner and Brandon Nappi.txt'
    ]

    print("=" * 60)
    print("Transcript Cleaning Script")
    print("=" * 60)
    print()

    for filename in files_to_process:
        input_path = base_dir / filename
        output_filename = filename.replace('.txt', '_cleaned.txt')
        output_path = base_dir / output_filename

        if input_path.exists():
            try:
                lines_written = clean_transcript(input_path, output_path)
                print(f"  ✓ Successfully processed - {lines_written} sections created")
            except Exception as e:
                print(f"  ✗ Error processing file: {e}")
        else:
            print(f"  ✗ File not found: {filename}")
        print()

    print("=" * 60)
    print("Processing complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
