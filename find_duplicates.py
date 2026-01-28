#!/usr/bin/env python3
"""
Find duplicate files and large files in a directory.
Usage: python find_duplicates.py [directory] [--min-size SIZE_IN_MB]
"""

import os
import sys
import hashlib
from collections import defaultdict
from pathlib import Path


def get_file_hash(filepath, chunk_size=8192):
    """Calculate MD5 hash of a file."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, PermissionError):
        return None


def format_size(size_bytes):
    """Format bytes into human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def find_duplicates_and_large_files(directory, min_size_mb=10):
    """
    Scan directory for duplicate files and large files.

    Args:
        directory: Path to scan
        min_size_mb: Minimum size in MB to consider a file "large"
    """
    min_size_bytes = min_size_mb * 1024 * 1024

    # Group files by size first (quick filter for potential duplicates)
    size_to_files = defaultdict(list)
    large_files = []

    print(f"Scanning directory: {directory}")
    print(f"Looking for large files >= {min_size_mb} MB")
    print("-" * 60)

    file_count = 0
    for root, dirs, files in os.walk(directory):
        # Skip hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]

        for filename in files:
            if filename.startswith('.'):
                continue

            filepath = os.path.join(root, filename)
            try:
                size = os.path.getsize(filepath)
                file_count += 1

                # Track for duplicate detection
                size_to_files[size].append(filepath)

                # Track large files
                if size >= min_size_bytes:
                    large_files.append((filepath, size))

            except (OSError, PermissionError):
                continue

    print(f"Scanned {file_count} files\n")

    # Find duplicates by comparing hashes of same-size files
    duplicates = []
    hash_to_files = defaultdict(list)

    for size, files in size_to_files.items():
        if len(files) > 1:  # Only check files with matching sizes
            for filepath in files:
                file_hash = get_file_hash(filepath)
                if file_hash:
                    hash_to_files[(size, file_hash)].append(filepath)

    for (size, file_hash), files in hash_to_files.items():
        if len(files) > 1:
            duplicates.append((files, size))

    # Report large files
    print("=" * 60)
    print("LARGE FILES")
    print("=" * 60)
    if large_files:
        large_files.sort(key=lambda x: x[1], reverse=True)
        for filepath, size in large_files:
            rel_path = os.path.relpath(filepath, directory)
            print(f"  {format_size(size):>12}  {rel_path}")
        print()
        total_large = sum(size for _, size in large_files)
        print(f"Total large files: {len(large_files)} ({format_size(total_large)})")
    else:
        print(f"  No files >= {min_size_mb} MB found")
    print()

    # Report duplicates
    print("=" * 60)
    print("DUPLICATE FILES")
    print("=" * 60)
    if duplicates:
        duplicates.sort(key=lambda x: x[1] * (len(x[0]) - 1), reverse=True)
        total_wasted = 0

        for files, size in duplicates:
            wasted = size * (len(files) - 1)
            total_wasted += wasted
            print(f"\n  Size: {format_size(size)} | Wasted: {format_size(wasted)} | Copies: {len(files)}")
            for filepath in files:
                rel_path = os.path.relpath(filepath, directory)
                print(f"    - {rel_path}")

        print()
        print(f"Total duplicate groups: {len(duplicates)}")
        print(f"Total wasted space: {format_size(total_wasted)}")
    else:
        print("  No duplicate files found")
    print()

    return duplicates, large_files


def main():
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    min_size = 10  # Default 10 MB

    # Parse --min-size argument
    for i, arg in enumerate(sys.argv):
        if arg == "--min-size" and i + 1 < len(sys.argv):
            try:
                min_size = float(sys.argv[i + 1])
            except ValueError:
                print(f"Invalid size: {sys.argv[i + 1]}")
                sys.exit(1)

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory")
        sys.exit(1)

    find_duplicates_and_large_files(os.path.abspath(directory), min_size)


if __name__ == "__main__":
    main()
