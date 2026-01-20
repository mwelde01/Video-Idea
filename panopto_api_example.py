#!/usr/bin/env python3
"""
Example of using Panopto REST API to download transcripts
This requires API credentials from your Panopto administrator

For more information on Panopto API:
https://demo.hosted.panopto.com/Panopto/api/docs/index.html
"""

import requests
import json
from extract_panopto_transcripts import parse_srt_content

class PanoptoAPI:
    """
    Wrapper for Panopto REST API

    Note: This is a basic example. For production use, implement proper
    OAuth2 authentication flow.
    """

    def __init__(self, server_url, api_key=None):
        """
        Initialize Panopto API client

        Args:
            server_url: Your Panopto server URL (e.g., https://yoursite.hosted.panopto.com)
            api_key: API key or access token (optional, required for authenticated endpoints)
        """
        self.server_url = server_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            })

    def get_session_by_id(self, session_id):
        """
        Get session details by ID

        Args:
            session_id: The video/session ID

        Returns:
            dict: Session details including caption download URL
        """
        url = f"{self.server_url}/Panopto/api/v1/sessions/{session_id}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting session: {str(e)}")
            return None

    def get_caption_download_url(self, session_id):
        """
        Get the caption download URL for a session

        Args:
            session_id: The video/session ID

        Returns:
            str: Caption download URL or None if not available
        """
        session_data = self.get_session_by_id(session_id)

        if not session_data:
            return None

        # The caption download URL should be in the session data
        # Note: The exact field name may vary depending on API version
        caption_url = session_data.get('CaptionDownloadUrl')

        if not caption_url:
            # Try alternative field names
            caption_url = session_data.get('captionDownloadUrl')

        return caption_url

    def download_transcript(self, session_id):
        """
        Download and parse transcript for a session

        Args:
            session_id: The video/session ID

        Returns:
            str: Clean transcript text without timestamps
        """
        caption_url = self.get_caption_download_url(session_id)

        if not caption_url:
            return "Error: No caption URL found for this session"

        # Download the caption file
        try:
            response = self.session.get(caption_url, timeout=30)
            response.raise_for_status()

            # Parse SRT format and remove timestamps
            transcript = parse_srt_content(response.text)
            return transcript

        except Exception as e:
            return f"Error downloading captions: {str(e)}"


def example_with_api():
    """
    Example using Panopto REST API

    To use this, you need:
    1. API credentials from your Panopto administrator
    2. The session ID of the video
    """

    # Configuration
    SERVER_URL = "https://yoursite.hosted.panopto.com"
    API_KEY = "your-api-key-here"  # Get this from your Panopto admin
    SESSION_ID = "4335bd73-57a0-4730-b44c-b3d401582ab9"

    # Create API client
    api = PanoptoAPI(SERVER_URL, API_KEY)

    # Get session details
    print("Fetching session details...")
    session_data = api.get_session_by_id(SESSION_ID)

    if session_data:
        print(f"Session Name: {session_data.get('Name', 'Unknown')}")
        print(f"Duration: {session_data.get('Duration', 'Unknown')}")
        print(f"Has Captions: {bool(session_data.get('CaptionDownloadUrl'))}")

    # Download transcript
    print("\nDownloading transcript...")
    transcript = api.download_transcript(SESSION_ID)

    print("\n" + "="*80)
    print("TRANSCRIPT")
    print("="*80 + "\n")
    print(transcript)


def example_direct_caption_url():
    """
    Example of directly accessing caption URL if you already know it

    This works for public videos without authentication
    """

    # If you know the caption download URL from the API or page source
    caption_url = "https://yoursite.hosted.panopto.com/Panopto/Pages/Transcription/GenerateSRT.ashx?id=VIDEO-ID&language=English_USA"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    try:
        response = requests.get(caption_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Parse SRT and remove timestamps
        transcript = parse_srt_content(response.text)

        print("="*80)
        print("TRANSCRIPT")
        print("="*80 + "\n")
        print(transcript)

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    print("Panopto REST API Example")
    print("="*80)
    print("\nThis is a template/example script.")
    print("To use it, you need to:")
    print("1. Get API credentials from your Panopto administrator")
    print("2. Update the SERVER_URL and API_KEY in the example_with_api() function")
    print("3. Uncomment the function call below")
    print("\n" + "="*80)

    # Uncomment to use:
    # example_with_api()

    # Or if you just have a direct caption URL:
    # example_direct_caption_url()
