from flask import Flask, request, send_file
from pytube import YouTube
import os
import shutil

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

            # Download the video
            video_filename = f"{video_id}.mp4"
            video_stream.download(filename=video_filename)

            # Serve the downloaded video as a static file
            return send_file(video_filename, mimetype='video/mp4', as_attachment=False)
        except Exception as e:
            return f"An error occurred: {str(e)}"
        finally:
            # Remove the downloaded video file
            if os.path.exists(video_filename):
                os.remove(video_filename)
                shutil.rmtree('images', ignore_errors=True)

    return "No video ID provided."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
