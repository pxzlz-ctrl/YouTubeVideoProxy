from flask import Flask, request, Response
from pytube import YouTube
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, please provide a video ID in the URL."

@app.route('/watch', methods=['GET'])
def proxy():
    video_id = request.args.get('v')

    if video_id:
        try:
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            youtube = YouTube(video_url)
            video_stream = youtube.streams.get_highest_resolution()

            # Get the video stream URL
            stream_url = video_stream.url

            # Generate the video stream response
            return Response(stream_video(stream_url), mimetype='video/mp4')
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return "No video ID provided."

def stream_video(url):
    response = requests.get(url, stream=True)
    for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
        yield chunk

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
