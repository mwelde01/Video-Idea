#!/usr/bin/env python3
"""
Merges manual transcripts from ai_case_studies_manual.txt into
ai_case_studies_compiled.md, replacing failed entries and adding new students
in alphabetical order.
"""

import re
import sys
import os


def strip_timestamps(text):
    """Remove timestamp lines like 0:02 or 1:08 or 2:37 from transcript text."""
    lines = text.split('\n')
    cleaned = []
    for line in lines:
        stripped = line.strip()
        # Skip lines that are only a timestamp (e.g. "0:02", "1:08", "12:34")
        if re.match(r'^\d+:\d+(\.\d+)?$', stripped):
            continue
        # Remove leading/trailing brackets left from the template
        stripped = stripped.strip('[]')
        cleaned.append(stripped)
    # Collapse multiple blank lines into one
    result = re.sub(r'\n{3,}', '\n\n', '\n'.join(cleaned))
    return result.strip()


def parse_manual_file(filepath):
    """
    Parse manual transcript file into a dict:
    { (student_name, type): transcript_text }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = {}
    # Split on --- separator
    blocks = re.split(r'\n---+\n', content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        student_match = re.search(r'STUDENT:\s*(.+)', block)
        type_match = re.search(r'TYPE:\s*(.+)', block)

        if not student_match or not type_match:
            continue

        student = student_match.group(1).strip()
        video_type = type_match.group(1).strip()

        # Extract transcript text (everything after the TYPE line)
        type_pos = block.find('TYPE:')
        type_end = block.find('\n', type_pos)
        transcript_raw = block[type_end:].strip()

        transcript = strip_timestamps(transcript_raw)
        entries[(student, video_type)] = transcript
        print(f"  Parsed: {student} - {video_type} ({len(transcript)} chars)")

    return entries


def parse_compiled_md(filepath):
    """
    Parse the compiled markdown into a dict of student sections.
    Returns: ordered list of student names, dict of { student: {Positive, Negative} }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    students = {}
    order = []

    # Find all ## Student Name sections
    sections = re.split(r'\n## ', content)
    header = sections[0]  # Table of contents and intro

    for section in sections[1:]:
        lines = section.split('\n')
        name = lines[0].strip()
        if name in ('Table of Contents',):
            continue
        order.append(name)

        # Extract all ### subsections dynamically
        subsections = re.findall(r'### (.+?)\n\n(.*?)(?=\n### |\n---|\Z)', section, re.DOTALL)
        students[name] = {title.strip(): body.strip() for title, body in subsections}
    return header, order, students


def is_failed(text):
    """Return True if this transcript is a failure/error placeholder."""
    if not text:
        return True
    t = text.strip().lower()
    return (t.startswith('*error') or
            t.startswith('*no transcript') or
            t.startswith('*no video') or
            t == '' or
            t == '*no video submitted*')


def write_compiled_md(filepath, header, order, students):
    """Write the updated compiled markdown file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        # Write header up to (but not including) the old TOC body
        # Strip old TOC entries and rewrite
        toc_start = header.find('## Table of Contents')
        if toc_start != -1:
            f.write(header[:toc_start])
        else:
            f.write(header)

        # Table of contents
        f.write('## Table of Contents\n\n')
        for name in order:
            anchor = name.lower().replace(' ', '-')
            f.write(f'- [{name}](#{anchor})\n')
        f.write('\n---\n\n')

        # Collect all section types across all students
        all_types = []
        for s in students.values():
            for t in s.keys():
                if t not in all_types:
                    all_types.append(t)

        # Student sections
        for name in order:
            f.write(f'## {name}\n\n')
            for section_type in all_types:
                f.write(f'### {section_type}\n\n')
                content = students[name].get(section_type, '')
                f.write(f'{content}\n\n' if content else '*No video submitted*\n\n')
            f.write('---\n\n')


def merge(manual_file, compiled_file):
    print(f'\nParsing manual transcripts from: {manual_file}')
    manual = parse_manual_file(manual_file)

    print(f'\nParsing compiled file: {compiled_file}')
    header, order, students = parse_compiled_md(compiled_file)

    print(f'\nMerging {len(manual)} manual entries...')
    added = []
    updated = []

    for (student, video_type), transcript in manual.items():
        if student not in students:
            # New student — add with empty slots
            students[student] = {'Positive': '', 'Negative': ''}
            order.append(student)
            added.append(student)

        current = students[student].get(video_type, '')
        if is_failed(current) or not current:
            students[student][video_type] = transcript
            updated.append(f'{student} - {video_type}')
        else:
            print(f'  Skipping {student} - {video_type} (already has content)')

    # Sort order alphabetically by last name, handling compound last names
    compound_last_names = {
        'Haj Hussein': 'haj hussein',
        'Zakizadeh Sedaghat': 'zakizadeh sedaghat',
    }

    def sort_key(name):
        for compound, key in compound_last_names.items():
            if compound in name:
                return key
        parts = name.strip().split()
        return parts[-1].lower() if parts else name.lower()

    order_sorted = sorted(set(order), key=sort_key)

    # Write updated file
    write_compiled_md(compiled_file, header, order_sorted, students)

    print(f'\nDone!')
    print(f'  New students added: {len(added)} — {added if added else "none"}')
    print(f'  Entries updated: {len(updated)}')
    for u in updated:
        print(f'    - {u}')
    print(f'\nUpdated file saved to: {compiled_file}')


if __name__ == '__main__':
    manual_file = sys.argv[1] if len(sys.argv) > 1 else 'ai_case_studies_manual.txt'
    compiled_file = sys.argv[2] if len(sys.argv) > 2 else 'ai_case_studies_compiled.md'

    if not os.path.exists(manual_file):
        print(f'Error: Manual file not found: {manual_file}')
        sys.exit(1)
    if not os.path.exists(compiled_file):
        print(f'Error: Compiled file not found: {compiled_file}')
        sys.exit(1)

    merge(manual_file, compiled_file)
