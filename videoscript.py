from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_url):
    try:
        # Extract video ID from the URL
        video_id = video_url.split("v=")[-1]
        # Get transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine the transcript text
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
video_url = "https://www.youtube.com/watch?v=1Sh6CJYxuAo&t=112s"
transcript = get_youtube_transcript(video_url)
print(transcript)
