#!/usr/bin/env python3
"""
Example usage of the Panopto transcript extractor
"""

from extract_panopto_transcripts import extract_panopto_transcript

def extract_single_video():
    """Extract transcript from a single video"""
    url = "https://louisville.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4335bd73-57a0-4730-b44c-b3d401582ab9"

    print("Extracting transcript from single video...")
    transcript = extract_panopto_transcript(url)

    print("\n" + "="*80)
    print("TRANSCRIPT")
    print("="*80 + "\n")
    print(transcript)

    return transcript

def extract_multiple_videos():
    """Extract transcripts from multiple videos"""
    urls = [
        "https://site1.panopto.com/Panopto/Pages/Viewer.aspx?id=video-id-1",
        "https://site2.panopto.com/Panopto/Pages/Viewer.aspx?id=video-id-2",
        "https://site3.panopto.com/Panopto/Pages/Viewer.aspx?id=video-id-3",
    ]

    transcripts = {}

    for i, url in enumerate(urls, 1):
        print(f"\n{'='*80}")
        print(f"Processing video {i}/{len(urls)}")
        print(f"{'='*80}\n")

        transcript = extract_panopto_transcript(url)
        transcripts[url] = transcript

    return transcripts

def save_transcript_to_file(url, output_file="transcript.txt"):
    """Extract transcript and save to a file"""
    print(f"Extracting transcript from: {url}")
    transcript = extract_panopto_transcript(url)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Transcript from: {url}\n")
        f.write("="*80 + "\n\n")
        f.write(transcript)

    print(f"\nTranscript saved to: {output_file}")
    return transcript

def extract_and_analyze(url):
    """Extract transcript and perform basic analysis"""
    transcript = extract_panopto_transcript(url)

    if not transcript.startswith("Error") and not transcript.startswith("No transcript"):
        word_count = len(transcript.split())
        char_count = len(transcript)

        print("\n" + "="*80)
        print("ANALYSIS")
        print("="*80)
        print(f"Word count: {word_count}")
        print(f"Character count: {char_count}")
        print(f"Estimated reading time: {word_count / 200:.1f} minutes (at 200 wpm)")
        print("\n" + "="*80)
        print("TRANSCRIPT")
        print("="*80 + "\n")
        print(transcript)
    else:
        print(f"\n{transcript}")

    return transcript

if __name__ == "__main__":
    # Example 1: Extract single video
    print("Example 1: Single video extraction")
    print("-" * 80)
    extract_single_video()

    # Example 2: Save to file
    # print("\n\nExample 2: Save transcript to file")
    # print("-" * 80)
    # url = "https://louisville.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=4335bd73-57a0-4730-b44c-b3d401582ab9"
    # save_transcript_to_file(url, "my_transcript.txt")

    # Example 3: Extract with analysis
    # print("\n\nExample 3: Extract with analysis")
    # print("-" * 80)
    # extract_and_analyze(url)

    # Example 4: Multiple videos
    # print("\n\nExample 4: Multiple videos")
    # print("-" * 80)
    # transcripts = extract_multiple_videos()
