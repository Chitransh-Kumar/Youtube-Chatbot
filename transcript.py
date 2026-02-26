from youtube_transcript_api import YouTubeTranscriptApi
from utils import get_video_id

def transcript_generation(url):
    """
    Extracts the YouTube transcript from a URL.

    It first gets the video ID and then extracts Transcript via YouTubeTranscriptApi.

    Supports standard watch URLs, embed URLs, shorts URLs and shortened youtu.be links.

    Args:
        url (str): A YouTube video URL.

    Returns:
        str | None: Transcript of the video if it exists, otherwise None.
    
    """


    video_id= get_video_id(url)

    if not video_id:
        print("Invalid Youtube URL")
        return 

    try:
        transcript_list= YouTubeTranscriptApi().fetch(video_id, languages= ['en'])

        transcript= " ".join(chunk.text for chunk in transcript_list)

        return transcript

    except: 

        return "No captions available for this video"
    
