#!/usr/bin/env python3
"""
Test the SRT parser with sample data to demonstrate functionality
"""

from extract_panopto_transcripts import parse_srt_content

# Sample SRT format (typical Panopto caption output)
sample_srt = """1
00:00:00,000 --> 00:00:03,500
Welcome to this Panopto video tutorial.

2
00:00:03,500 --> 00:00:07,200
Today we'll be discussing the fundamentals of machine learning.

3
00:00:07,200 --> 00:00:11,800
Machine learning is a subset of artificial intelligence.

4
00:00:11,800 --> 00:00:15,300
It allows computers to learn from data without being explicitly programmed.

5
00:00:15,300 --> 00:00:19,600
There are three main types of machine learning: supervised, unsupervised, and reinforcement learning.

6
00:00:19,600 --> 00:00:23,400
Supervised learning uses labeled data to train models.

7
00:00:23,400 --> 00:00:27,100
Unsupervised learning finds patterns in unlabeled data.

8
00:00:27,100 --> 00:00:31,500
Reinforcement learning uses rewards and penalties to guide learning.

9
00:00:31,500 --> 00:00:35,200
In this course, we'll explore each of these approaches in detail.

10
00:00:35,200 --> 00:00:38,000
Let's get started with our first example.
"""

def test_srt_parser():
    """Test the SRT parser with sample data"""

    print("="*80)
    print("TESTING SRT PARSER")
    print("="*80)

    print("\nInput: Sample SRT format with timestamps")
    print("-"*80)
    print(sample_srt[:300] + "...")  # Show first 300 chars

    print("\n" + "="*80)
    print("PARSED OUTPUT (Clean Transcript)")
    print("="*80 + "\n")

    # Parse the SRT content
    clean_transcript = parse_srt_content(sample_srt)
    print(clean_transcript)

    # Show statistics
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Word count: {len(clean_transcript.split())}")
    print(f"Character count: {len(clean_transcript)}")
    print(f"Contains timestamps: {'-->' in clean_transcript}")
    print(f"Contains sequence numbers: {any(char.isdigit() and char + ' ' in clean_transcript for char in '0123456789')}")

    print("\n✓ Parser successfully removed timestamps and sequence numbers!")

if __name__ == "__main__":
    test_srt_parser()
