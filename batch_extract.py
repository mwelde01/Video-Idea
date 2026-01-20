#!/usr/bin/env python3
"""
Batch process multiple Panopto videos and save transcripts to individual files
"""

import sys
import os
from extract_panopto_transcripts import extract_panopto_transcript, extract_video_id

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def batch_extract_from_file(input_file, output_dir="transcripts"):
    """
    Extract transcripts from multiple URLs listed in a file

    Args:
        input_file: Path to file containing one Panopto URL per line
        output_dir: Directory to save transcript files

    Returns:
        dict: Results with success/failure status for each URL
    """

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Read URLs from file
    try:
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        return {}

    if not urls:
        print("Error: No URLs found in input file")
        return {}

    print(f"Found {len(urls)} URLs to process\n")

    results = {}
    success_count = 0
    failure_count = 0

    # Process each URL
    for i, url in enumerate(urls, 1):
        print(f"\n{'='*80}")
        print(f"Processing {i}/{len(urls)}: {url}")
        print('='*80)

        # Extract video ID for filename
        video_id = extract_video_id(url)
        if not video_id:
            print("Error: Could not extract video ID from URL")
            results[url] = {"status": "failed", "error": "Invalid URL"}
            failure_count += 1
            continue

        # Extract transcript
        transcript = extract_panopto_transcript(url)

        # Check if extraction was successful
        if transcript.startswith("Error") or transcript.startswith("No transcript"):
            print(f"Failed: {transcript}")
            results[url] = {"status": "failed", "error": transcript}
            failure_count += 1
            continue

        # Save transcript to file
        filename = sanitize_filename(f"{video_id}.txt")
        output_path = os.path.join(output_dir, filename)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Source: {url}\n")
                f.write(f"Video ID: {video_id}\n")
                f.write("="*80 + "\n\n")
                f.write(transcript)

            print(f"✓ Success! Saved to: {output_path}")

            # Calculate stats
            word_count = len(transcript.split())
            results[url] = {
                "status": "success",
                "output_file": output_path,
                "word_count": word_count,
                "char_count": len(transcript)
            }
            success_count += 1

        except Exception as e:
            print(f"Error saving file: {str(e)}")
            results[url] = {"status": "failed", "error": f"File save error: {str(e)}"}
            failure_count += 1

    # Print summary
    print("\n" + "="*80)
    print("BATCH PROCESSING SUMMARY")
    print("="*80)
    print(f"Total URLs: {len(urls)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")
    print(f"Output directory: {os.path.abspath(output_dir)}")

    if success_count > 0:
        print("\nSuccessfully processed videos:")
        for url, result in results.items():
            if result["status"] == "success":
                print(f"  - {url}")
                print(f"    File: {result['output_file']}")
                print(f"    Words: {result['word_count']}")

    if failure_count > 0:
        print("\nFailed videos:")
        for url, result in results.items():
            if result["status"] == "failed":
                print(f"  - {url}")
                print(f"    Error: {result['error']}")

    return results

def batch_extract_from_list(urls, output_dir="transcripts"):
    """
    Extract transcripts from a list of URLs

    Args:
        urls: List of Panopto URLs
        output_dir: Directory to save transcript files

    Returns:
        dict: Results with success/failure status for each URL
    """

    # Create temporary file with URLs
    temp_file = "temp_urls.txt"
    with open(temp_file, 'w') as f:
        f.write('\n'.join(urls))

    # Process using file-based function
    results = batch_extract_from_file(temp_file, output_dir)

    # Clean up temp file
    os.remove(temp_file)

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_extract.py <input_file> [output_dir]")
        print("\nExample:")
        print("  python batch_extract.py urls.txt transcripts")
        print("\nThe input file should contain one Panopto URL per line.")
        print("Lines starting with # are treated as comments and ignored.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "transcripts"

    batch_extract_from_file(input_file, output_dir)
