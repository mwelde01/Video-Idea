#!/usr/bin/env python3
"""
Process manual transcript files and merge them into compiled_transcripts.md

This script:
1. Looks for manual transcript files in the format: StudentName_CaseType_manual.txt
2. Removes timestamps from the transcript text
3. Updates the compiled_transcripts.md file with the cleaned transcripts

Usage:
    python add_manual_transcripts.py

Manual transcript file naming format:
    FirstName_LastName_Positive_manual.txt
    FirstName_LastName_Negative_manual.txt

Examples:
    Charles_Barr_Positive_manual.txt
    Emma_Frank_Negative_manual.txt
"""

import os
import re
from extract_panopto_transcripts import parse_srt_content

def remove_timestamps(text):
    """
    Remove timestamps from transcript text.
    Handles various timestamp formats:
    - 00:00:12 --> 00:00:15
    - [00:00:12]
    - 0:12 - 0:15
    - Sequence numbers (1, 2, 3, etc.)
    """
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Skip sequence numbers (just digits on their own line)
        if line.isdigit():
            continue

        # Skip SRT timestamp lines (00:00:12 --> 00:00:15)
        if '-->' in line:
            continue

        # Remove inline timestamps like [00:00:12] or (0:12)
        line = re.sub(r'\[?\d{1,2}:\d{2}(:\d{2})?\]?', '', line)
        line = re.sub(r'\(\d{1,2}:\d{2}(:\d{2})?\)', '', line)

        # Remove timestamp ranges like 0:12 - 0:15
        line = re.sub(r'\d{1,2}:\d{2}(:\d{2})?\s*-\s*\d{1,2}:\d{2}(:\d{2})?', '', line)

        # Clean up extra whitespace
        line = ' '.join(line.split())

        if line:
            cleaned_lines.append(line)

    # Join with spaces for narrative format
    return ' '.join(cleaned_lines)

def find_manual_transcripts(directory='.'):
    """Find all manual transcript files"""
    manual_files = {}

    for filename in os.listdir(directory):
        if filename.endswith('_manual.txt'):
            # Parse filename: FirstName_LastName_CaseType_manual.txt
            parts = filename.replace('_manual.txt', '').split('_')

            if len(parts) >= 3:
                # Last part is case type (Positive/Negative)
                case_type = parts[-1]
                # Everything before that is the name
                student_name = ' '.join(parts[:-1])

                if student_name not in manual_files:
                    manual_files[student_name] = {}

                manual_files[student_name][case_type] = filename

    return manual_files

def read_and_clean_transcript(filepath):
    """Read transcript file and remove timestamps"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        # First try SRT parser (handles SRT format specifically)
        cleaned = parse_srt_content(raw_text)

        # If that didn't work well, use the general timestamp remover
        if not cleaned or len(cleaned) < 50:
            cleaned = remove_timestamps(raw_text)

        return cleaned
    except Exception as e:
        return f"Error reading file: {str(e)}"

def update_compiled_document(manual_transcripts, compiled_file='compiled_transcripts.md'):
    """Update the compiled document with manual transcripts"""

    if not os.path.exists(compiled_file):
        print(f"Error: {compiled_file} not found!")
        return False

    # Read the compiled document
    with open(compiled_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Track updates
    updates_made = 0

    # Process each manual transcript
    for student_name, cases in manual_transcripts.items():
        print(f"\nProcessing: {student_name}")

        # Find the student's section
        # Try different name formats (with different capitalizations)
        student_variations = [
            student_name,
            student_name.title(),
            ' '.join([part.capitalize() for part in student_name.split()])
        ]

        for name_variant in student_variations:
            # Look for the student's section header
            section_pattern = re.escape(f"## {name_variant}")

            if re.search(section_pattern, content):
                print(f"  Found section for: {name_variant}")

                for case_type, filename in cases.items():
                    print(f"    Processing {case_type} AI Case from {filename}")

                    # Read and clean the transcript
                    transcript = read_and_clean_transcript(filename)

                    if transcript.startswith("Error"):
                        print(f"    ⚠ {transcript}")
                        continue

                    # Find and replace the placeholder text
                    # Look for patterns like:
                    # ### Positive AI Case
                    # *No transcript found...*  OR  *Error: ...*

                    case_pattern = re.escape(f"### {case_type} AI Case")

                    # Pattern to match the error/no transcript message
                    error_patterns = [
                        r'\*No transcript found[^*]*\*',
                        r'\*Error:[^*]*\*',
                        r'\*No captions available[^*]*\*'
                    ]

                    # Find the case section
                    case_match = re.search(case_pattern, content)
                    if case_match:
                        # Find the next error message after this case header
                        search_start = case_match.end()

                        for error_pattern in error_patterns:
                            error_match = re.search(error_pattern, content[search_start:search_start+500])
                            if error_match:
                                # Calculate actual position in full content
                                actual_start = search_start + error_match.start()
                                actual_end = search_start + error_match.end()

                                # Replace the error message with the transcript
                                content = content[:actual_start] + transcript + content[actual_end:]

                                print(f"    ✓ Updated {case_type} AI Case")
                                updates_made += 1
                                break

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
        print(f"⚠ No updates were made. Check that:")
        print(f"  - Student names in filenames match names in {compiled_file}")
        print(f"  - Case type is 'Positive' or 'Negative' (case sensitive)")
        print(f"  - Files end with '_manual.txt'")
        print(f"{'='*80}")
        return False

def main():
    print("="*80)
    print("MANUAL TRANSCRIPT PROCESSOR")
    print("="*80)
    print()

    # Find all manual transcript files
    manual_transcripts = find_manual_transcripts()

    if not manual_transcripts:
        print("No manual transcript files found.")
        print()
        print("Expected filename format:")
        print("  FirstName_LastName_Positive_manual.txt")
        print("  FirstName_LastName_Negative_manual.txt")
        print()
        print("Examples:")
        print("  Charles_Barr_Positive_manual.txt")
        print("  Emma_Frank_Negative_manual.txt")
        print("  Xanny_Frazier_Positive_manual.txt")
        return

    print(f"Found {sum(len(cases) for cases in manual_transcripts.values())} manual transcript file(s):\n")

    for student, cases in sorted(manual_transcripts.items()):
        print(f"  {student}:")
        for case_type, filename in cases.items():
            print(f"    - {case_type} AI Case: {filename}")

    print()

    # Process and update
    update_compiled_document(manual_transcripts)

if __name__ == "__main__":
    main()
