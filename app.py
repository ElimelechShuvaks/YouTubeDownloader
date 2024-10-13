import os
import yt_dlp
import tempfile

from flask import Flask, render_template, request, send_file

app = Flask(__name__)

# פונקציה להורדת הוידאו
def download_youtube_video(url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'nocheckcertificate': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    
    # יצירת קובץ זמני
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        tmp_file_path = tmp_file.name
    
    # הורדת הוידאו לקובץ זמני
    download_youtube_video(video_url, tmp_file_path)
    
    # שליחת הקובץ להורדה למשתמש
    return send_file(tmp_file_path, as_attachment=True, download_name="downloaded_video.mp4")

if __name__ == '__main__':
    app.run(debug=True)
