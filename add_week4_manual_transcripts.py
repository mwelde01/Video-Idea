#!/usr/bin/env python3
"""
Add manual transcripts to Week 4 compiled document.

For students whose videos didn't have auto-captions or are Google Drive videos,
manually copy the transcript and save as: FirstName_LastName_manual.txt

Then run this script to update week4_transcripts.md

Usage:
    python add_week4_manual_transcripts.py
"""

import os
import re
from add_manual_transcripts import remove_timestamps

def find_week4_manual_transcripts(directory='.'):
    """Find all Week 4 manual transcript files"""
    manual_files = {}

    for filename in os.listdir(directory):
        if filename.endswith('_manual.txt') and not any(x in filename for x in ['Positive', 'Negative']):
            # Parse filename: FirstName_LastName_manual.txt
            student_name = filename.replace('_manual.txt', '').replace('_', ' ')
            manual_files[student_name] = filename

    return manual_files

def read_and_clean_transcript(filepath):
    """Read transcript file and remove timestamps"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        # Use the comprehensive timestamp remover
        cleaned = remove_timestamps(raw_text)

        return cleaned
    except Exception as e:
        return f"Error reading file: {str(e)}"

def update_week4_document(manual_transcripts, compiled_file='week4_transcripts.md'):
    """Update the Week 4 compiled document with manual transcripts"""

    if not os.path.exists(compiled_file):
        print(f"Error: {compiled_file} not found!")
        print("Run process_week4_transcripts.py first to create the base document.")
        return False

    # Read the compiled document
    with open(compiled_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Track updates
    updates_made = 0

    # Process each manual transcript
    for student_name, filename in manual_transcripts.items():
        print(f"\nProcessing: {student_name}")

        # Try different name formats
        student_variations = [
            student_name,
            student_name.title(),
            ' '.join([part.capitalize() for part in student_name.split()])
        ]

        for name_variant in student_variations:
            # Look for the student's section
            section_pattern = re.escape(f"## {name_variant}")

            if re.search(section_pattern, content):
                print(f"  Found section for: {name_variant}")
                print(f"    Processing from {filename}")

                # Read and clean the transcript
                transcript = read_and_clean_transcript(filename)

                if transcript.startswith("Error"):
                    print(f"    ⚠ {transcript}")
                    continue

                # Find the student's section boundaries
                student_section_match = re.search(section_pattern, content)
                if not student_section_match:
                    continue

                student_start = student_section_match.start()

                # Find the next student section (next ##) to determine end boundary
                next_section_match = re.search(r'\n## ', content[student_start + 1:])
                if next_section_match:
                    student_end = student_start + 1 + next_section_match.start()
                else:
                    student_end = len(content)

                student_section = content[student_start:student_end]

                # Find the content area (everything after ## Name and before ---)
                content_match = re.search(r'## ' + re.escape(name_variant) + r'\n\n(.*?)\n\n---', student_section, re.DOTALL)

                if content_match:
                    current_content = content_match.group(1).strip()

                    # Check if it's an error or needs replacement
                    if current_content.startswith('*Error') or current_content.startswith('*No'):
                        # Calculate position and replace
                        content_start = student_start + content_match.start(1)
                        content_end = student_start + content_match.end(1)

                        # Replace the content
                        content = content[:content_start] + transcript + content[content_end:]

                        print(f"    ✓ Updated transcript")
                        updates_made += 1
                    else:
                        print(f"    ℹ Transcript already exists, skipping")

                # Found the student, no need to try other name variants
                break

    if updates_made > 0:
        # Write the updated content back
        with open(compiled_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"\n{'='*80}")
        print(f"✓ Successfully updated {updates_made} transcript(s) in {compiled_file}")
        print(f"{'='*80}")
        return True
    else:
        print(f"\n{'='*80}")
        print(f"⚠ No updates were made.")
        print(f"  Make sure:")
        print(f"  - Student names in filenames match names in week4_transcripts.md")
        print(f"  - Files end with '_manual.txt'")
        print(f"  - Example: Harshini_Sarojini_manual.txt or Xanny_Frazier_manual.txt")
        print(f"{'='*80}")
        return False

def main():
    print("="*80)
    print("WEEK 4 MANUAL TRANSCRIPT PROCESSOR")
    print("="*80)
    print()

    # Find all Week 4 manual transcript files
    manual_transcripts = find_week4_manual_transcripts()

    if not manual_transcripts:
        print("No manual transcript files found.")
        print()
        print("Expected filename format:")
        print("  FirstName_LastName_manual.txt")
        print()
        print("Examples:")
        print("  Harshini_Sarojini_manual.txt")
        print("  Xanny_Frazier_manual.txt")
        return

    print(f"Found {len(manual_transcripts)} manual transcript file(s):\n")

    for student, filename in sorted(manual_transcripts.items()):
        print(f"  {student}: {filename}")

    print()

    # Process and update
    update_week4_document(manual_transcripts)

if __name__ == "__main__":
    main()
