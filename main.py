from flask import Flask, request, send_file
from pytube import YouTube
import os
import shutil

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

            # Download the video
            video_filename = f"{video_id}.mp4"
            video_stream.download(output_path=VIDEO_DIR, filename=video_filename)

            # Serve the downloaded video as a static file
            video_path = os.path.join(VIDEO_DIR, video_filename)
            return send_file(video_path, mimetype='video/mp4', as_attachment=False)
        except Exception as e:
            return f"An error occurred: {str(e)}"
        finally:
            # Remove the downloaded video file
            if os.path.exists(video_path):
                os.remove(video_path)

    return "No video ID provided."

if __name__ == "__main__":
    # Create the video directory if it doesn't exist
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    # Run the Flask app
    app.run(debug=False)
