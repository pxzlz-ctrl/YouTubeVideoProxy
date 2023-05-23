from flask import Flask, request, send_file, Response
from pytube import YouTube
import os

app = Flask(__name__)

# Set the video download directory
VIDEO_DIR = "videos"

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

            # Create the video directory if it doesn't exist
            if not os.path.exists(VIDEO_DIR):
                os.makedirs(VIDEO_DIR)

            # Download the video
            video_filename = f"{video_id}.mp4"
            video_path = os.path.join(VIDEO_DIR, video_filename)
            if not os.path.exists(video_path):
                video_stream.download(output_path=VIDEO_DIR, filename=video_filename)

            # Serve the video as a streamed response
            return stream_video(video_path)
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return "No video ID provided."

def stream_video(video_path):
    def generate():
        with open(video_path, "rb") as video_file:
            while True:
                video_chunk = video_file.read(1024 * 1024)  # Read 1MB of video data
                if not video_chunk:
                    break
                yield video_chunk

    return Response(generate(), mimetype='video/mp4')

if __name__ == "__main__":
    app.run(debug=False)
