#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import re
import sys
from urllib.parse import urlparse, parse_qs

def parse_srt_content(srt_content):
    """Parse SRT format and extract text without timestamps"""
    lines = srt_content.strip().split('\n')
    transcript_lines = []

    for line in lines:
        line = line.strip()
        # Skip empty lines, sequence numbers, and timestamp lines
        if line and not line.isdigit() and '-->' not in line:
            transcript_lines.append(line)

    return ' '.join(transcript_lines)

def extract_video_id(url):
    """Extract video ID from Panopto URL"""
    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        return params.get('id', [None])[0]
    except:
        return None

def extract_panopto_transcript(url):
    """Extract transcript from Panopto video page using multiple methods"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

        # Extract video ID from URL
        video_id = extract_video_id(url)
        if not video_id:
            return "Error: Could not extract video ID from URL"

        # Extract base URL (e.g., https://louisville.hosted.panopto.com)
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        print(f"Video ID: {video_id}")
        print(f"Base URL: {base_url}")
        print("\nAttempting to download transcript...\n")

        # Method 1: Try GenerateSRT.ashx endpoint with common language codes
        languages = ['English_USA', 'English_GBR', '0', '1', 'en-US', 'en']

        for lang in languages:
            caption_url = f"{base_url}/Panopto/Pages/Transcription/GenerateSRT.ashx?id={video_id}&language={lang}"
            print(f"Trying: {caption_url}")

            try:
                caption_response = requests.get(caption_url, headers=headers, timeout=30)
                if caption_response.status_code == 200 and caption_response.text.strip():
                    print(f"✓ Success with language: {lang}\n")
                    # Parse SRT format and remove timestamps
                    transcript = parse_srt_content(caption_response.text)
                    if transcript:
                        return transcript
            except Exception as e:
                print(f"  Failed: {str(e)}")
                continue

        print("\nDirect caption download failed. Trying page scraping...\n")

        # Method 2: Scrape the page for embedded transcript data
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')

        # Look for caption data in page scripts
        for script in scripts:
            if not script.string:
                continue

            # Try to find caption language codes or URLs
            caption_patterns = [
                r'CaptionDownloadUrl["\']?\s*:\s*["\']([^"\']+)',
                r'captionUrl["\']?\s*:\s*["\']([^"\']+)',
                r'GenerateSRT\.ashx[^"\']*',
                r'language["\']?\s*:\s*["\']([^"\']+)',
            ]

            for pattern in caption_patterns:
                matches = re.findall(pattern, script.string)
                if matches:
                    print(f"Found pattern: {pattern}")
                    print(f"Matches: {matches}\n")

                    for match in matches:
                        if 'GenerateSRT' in match or match.startswith('http'):
                            caption_url = match if match.startswith('http') else base_url + match
                            try:
                                caption_response = requests.get(caption_url, headers=headers, timeout=30)
                                if caption_response.status_code == 200 and caption_response.text.strip():
                                    transcript = parse_srt_content(caption_response.text)
                                    if transcript:
                                        return transcript
                            except:
                                continue

        # Method 3: Look for embedded transcript data in JSON
        for script in scripts:
            if script.string and 'transcript' in script.string.lower():
                try:
                    # Try to extract JSON data containing transcript
                    match = re.search(r'transcript["\']?\s*:\s*(\[.*?\])', script.string, re.DOTALL)
                    if match:
                        transcript_data = json.loads(match.group(1))
                        transcript_text = " ".join([item.get('text', '') for item in transcript_data if isinstance(item, dict)])
                        if transcript_text:
                            return transcript_text
                except:
                    pass

        return "No transcript found. The video may not have captions, or authentication may be required."

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        transcript = extract_panopto_transcript(url)
        print("\n" + "="*80)
        print("TRANSCRIPT")
        print("="*80 + "\n")
        print(transcript)
    else:
        print("Usage: python extract_panopto_transcripts.py <url>")
        print("\nExample:")
        print("  python extract_panopto_transcripts.py 'https://site.panopto.com/Panopto/Pages/Viewer.aspx?id=VIDEO-ID'")
