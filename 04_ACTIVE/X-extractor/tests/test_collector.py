import pytest
import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collector import extract_tweet_id

def test_extract_tweet_id():
    url = "https://twitter.com/user/status/123456789"
    assert extract_tweet_id(url) == "123456789"
