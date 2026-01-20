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
    - 0:01 (standalone timestamps)
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

        # Skip lines that are ONLY timestamps (like "0:01" or "1:23:45")
        if re.match(r'^\d{1,2}:\d{2}(:\d{2})?$', line):
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

        # Use the comprehensive timestamp remover that handles all formats
        # including standalone timestamps like 0:01, 0:06, etc.
        cleaned = remove_timestamps(raw_text)

        # If that didn't work, try the SRT parser as fallback
        if not cleaned or len(cleaned) < 50:
            cleaned = parse_srt_content(raw_text)

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

                for case_type, filename in cases.items():
                    print(f"    Processing {case_type} AI Case from {filename}")

                    # Read and clean the transcript
                    transcript = read_and_clean_transcript(filename)

                    if transcript.startswith("Error"):
                        print(f"    ⚠ {transcript}")
                        continue

                    # Find and replace the placeholder text within this student's section
                    case_pattern = re.escape(f"### {case_type} AI Case")

                    # DEBUG: Show what we're looking for and where
                    print(f"      DEBUG: Looking for pattern: {case_pattern}")
                    print(f"      DEBUG: Student section preview: {repr(student_section[:200])}")

                    # Pattern to match the error/no transcript message
                    error_patterns = [
                        r'\*No transcript found[^*]*\*',
                        r'\*Error[^*]*\*',  # Matches *Error:...* or *Error extracting...*
                        r'\*No captions available[^*]*\*'
                    ]

                    # Find the case section within the student's section
                    case_match = re.search(case_pattern, student_section)
                    print(f"      DEBUG: Case match found: {case_match is not None}")
                    if case_match:
                        # Find the content after this case header
                        # Content starts after the header and any blank lines
                        search_start = case_match.end()

                        # DEBUG: Show what we're searching in
                        search_text = student_section[search_start:search_start+500]
                        print(f"      DEBUG: Searching in: {repr(search_text[:100])}")

                        # Find where content ends (next ### or ---)
                        # This captures everything between the case header and the next section
                        content_end_match = re.search(r'\n(###|---)', student_section[search_start:])

                        if content_end_match:
                            content_end = search_start + content_end_match.start()
                        else:
                            # If no next section found, go to end of student section
                            content_end = len(student_section)

                        # Extract the current content (might be error message or existing transcript)
                        current_content = student_section[search_start:content_end].strip()
                        print(f"      DEBUG: Current content length: {len(current_content)} chars")
                        print(f"      DEBUG: Current content preview: {repr(current_content[:80])}")

                        # Check if it's an error message or if we should replace it
                        is_error = False
                        for error_pattern in error_patterns:
                            if re.search(error_pattern, current_content):
                                is_error = True
                                print(f"      DEBUG: Matched error pattern: {error_pattern}")
                                break

                        # Also check if it contains auto-generated transcript note or starts with [
                        if '[Auto-generated transcript' in current_content:
                            print(f"      DEBUG: Found auto-generated transcript marker - will replace")
                            is_error = True  # Treat it as replaceable

                        if is_error or len(current_content) > 0:
                            # Replace the content
                            # Calculate positions in the full document
                            # We want to replace everything from after the header to before the next section
                            # But preserve the newlines structure

                            section_start = search_start
                            section_end = content_end

                            actual_start = student_start + section_start
                            actual_end = student_start + section_end

                            # Create the replacement with proper formatting
                            replacement = f"\n\n{transcript}\n"

                            # Replace in the full content
                            content = content[:actual_start] + replacement + content[actual_end:]

                            # Update the student section for next iteration
                            student_section = student_section[:section_start] + replacement + student_section[section_end:]
                            # Adjust student_end since content length changed
                            length_diff = len(replacement) - (section_end - section_start)
                            student_end += length_diff

                            print(f"    ✓ Updated {case_type} AI Case")
                            updates_made += 1
                        else:
                            print(f"      DEBUG: No content to replace found")

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
