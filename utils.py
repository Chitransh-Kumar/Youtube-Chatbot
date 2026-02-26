from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """
    Extracts the YouTube video ID from a URL.

    Supports standard watch URLs, embed URLs, shorts URLs and shortened youtu.be links.

    Args:
        url (str): A YouTube video URL.

    Returns:
        str | None: The video ID if extraction succeeds, otherwise None.

    """


    try:
        parsed_url= urlparse(url)

        if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
            
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query).get("v", [None])[0]
            
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            
            if parsed_url.path.startswith("/shorts/"):
                return parsed_url.path.split("/")[2]
            
        if parsed_url.hostname == "youtu.be":
            return parsed_url.path.lstrip("/")
        
        return None
    
    except Exception:
        return None
