#!/usr/bin/env python3
"""
Reorganize transcripts from compiled_transcripts.md by case type.

Creates a new file with all Positive AI Cases grouped together,
followed by all Negative AI Cases grouped together.

Usage:
    python reorganize_by_case_type.py

Input:  compiled_transcripts.md (organized by student)
Output: transcripts_by_case_type.md (organized by case type)
"""

import re
import os

def parse_compiled_transcripts(filepath='compiled_transcripts.md'):
    """Parse the compiled transcripts file and extract all transcripts by student and case type"""

    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found!")
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Dictionary to store transcripts: {student_name: {'Positive': text, 'Negative': text}}
    transcripts = {}

    # Split by student sections (## Student Name)
    student_sections = re.split(r'\n## ', content)

    for section in student_sections[1:]:  # Skip the header/intro
        lines = section.split('\n')
        student_name = lines[0].strip()

        # Find Positive and Negative AI Case sections
        positive_match = re.search(r'### Positive AI Case\n\n(.*?)\n\n### Negative AI Case', section, re.DOTALL)
        negative_match = re.search(r'### Negative AI Case\n\n(.*?)\n\n---', section, re.DOTALL)

        transcripts[student_name] = {
            'Positive': positive_match.group(1).strip() if positive_match else None,
            'Negative': negative_match.group(1).strip() if negative_match else None
        }

    return transcripts

def create_by_case_type_document(transcripts, output_file='transcripts_by_case_type.md'):
    """Create a new document organized by case type"""

    with open(output_file, 'w', encoding='utf-8') as f:
        # Header
        f.write("# AI Case Video Transcripts - Organized by Case Type\n\n")
        f.write("All student video transcripts organized by Positive and Negative AI cases.\n\n")
        f.write("---\n\n")

        # Table of Contents
        f.write("## Table of Contents\n\n")
        f.write("- [Positive AI Cases](#positive-ai-cases)\n")
        f.write("- [Negative AI Cases](#negative-ai-cases)\n")
        f.write("\n---\n\n")

        # Positive AI Cases Section
        f.write("# Positive AI Cases\n\n")
        f.write("These case studies demonstrate positive outcomes and successful implementations of AI in business contexts.\n\n")
        f.write("---\n\n")

        positive_count = 0
        for student_name in sorted(transcripts.keys()):
            positive_transcript = transcripts[student_name]['Positive']

            if positive_transcript and not positive_transcript.startswith('*'):
                positive_count += 1
                f.write(f"## {student_name}\n\n")
                f.write(f"{positive_transcript}\n\n")
                f.write("---\n\n")

        # Negative AI Cases Section
        f.write("\n\n")
        f.write("# Negative AI Cases\n\n")
        f.write("These case studies demonstrate challenges, failures, or negative outcomes related to AI implementation in business.\n\n")
        f.write("---\n\n")

        negative_count = 0
        for student_name in sorted(transcripts.keys()):
            negative_transcript = transcripts[student_name]['Negative']

            if negative_transcript and not negative_transcript.startswith('*'):
                negative_count += 1
                f.write(f"## {student_name}\n\n")
                f.write(f"{negative_transcript}\n\n")
                f.write("---\n\n")

    return positive_count, negative_count

def main():
    print("="*80)
    print("REORGANIZE TRANSCRIPTS BY CASE TYPE")
    print("="*80)
    print()

    # Parse the original compiled transcripts
    print("Reading compiled_transcripts.md...")
    transcripts = parse_compiled_transcripts()

    if not transcripts:
        return

    print(f"Found {len(transcripts)} students\n")

    # Create the reorganized document
    print("Creating transcripts_by_case_type.md...")
    positive_count, negative_count = create_by_case_type_document(transcripts)

    print("\n" + "="*80)
    print("SUCCESS")
    print("="*80)
    print(f"✓ Created: transcripts_by_case_type.md")
    print(f"✓ Positive AI Cases: {positive_count}")
    print(f"✓ Negative AI Cases: {negative_count}")
    print(f"✓ Total transcripts: {positive_count + negative_count}")
    print()
    print("Note: Error messages and missing transcripts were excluded from the output.")
    print()

if __name__ == "__main__":
    main()
