from flask import Flask, request, Response
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

            # Set video file name and path
            video_filename = f"{video_id}.mp4"
            video_path = os.path.join("videos", video_filename)

            # Download the video
            video_stream.download(output_path="videos", filename=video_filename)

            def generate():
                # Open the video file in binary mode
                with open(video_path, "rb") as video_file:
                    # Read the video file in chunks and yield them to the response
                    while True:
                        video_chunk = video_file.read(1024 * 1024)  # Read 1MB at a time
                        if not video_chunk:
                            break
                        yield video_chunk

                # Remove the downloaded video file
                if os.path.exists(video_path):
                    os.remove(video_path)

            # Serve the video as a streaming response
            return Response(generate(), mimetype='video/mp4')

        except Exception as e:
            return f"An error occurred: {str(e)}"
        finally:
            # Remove the downloaded video file if it exists
            if os.path.exists(video_path):
                os.remove(video_path)

    return "No video ID provided."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)
