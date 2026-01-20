#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import re
import sys

def extract_panopto_transcript(url):
    """Extract transcript from Panopto video page"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for transcript data in scripts
        scripts = soup.find_all('script')
        transcript_text = ""

        for script in scripts:
            if script.string and 'transcript' in script.string.lower():
                # Try to extract JSON data containing transcript
                try:
                    # Look for transcript data patterns
                    match = re.search(r'transcript["\']?\s*:\s*(\[.*?\])', script.string, re.DOTALL)
                    if match:
                        transcript_data = json.loads(match.group(1))
                        transcript_text = " ".join([item.get('text', '') for item in transcript_data if isinstance(item, dict)])
                        break
                except:
                    pass

        if not transcript_text:
            # Try to find caption/subtitle data
            for script in scripts:
                if script.string:
                    # Look for caption URLs
                    caption_match = re.search(r'caption["\']?\s*:\s*["\']([^"\']+)', script.string)
                    if caption_match:
                        caption_url = caption_match.group(1)
                        if not caption_url.startswith('http'):
                            base_url = '/'.join(url.split('/')[:3])
                            caption_url = base_url + caption_url

                        caption_response = requests.get(caption_url, headers=headers)
                        if caption_response.status_code == 200:
                            transcript_text = caption_response.text
                            break

        return transcript_text if transcript_text else "No transcript found"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        print(extract_panopto_transcript(url))
    else:
        print("Usage: python extract_panopto_transcripts.py <url>")
