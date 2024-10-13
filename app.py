from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

def download_youtube_video(url, output_path):
    # הגדרות להורדה
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'nocheckcertificate': True  # משבית את בדיקת ה-SSL
    }
    
    # הורדת הסרטון
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@app.route('/')
def index():
    return render_template('index.html')  # מציג את דף הבית (פורמט HTML פשוט שיבקש את ה-URL)

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']  # קבלת ה-URL מהמשתמש
    output_file = "downloaded_video.mp4"
    
    # הורדת הסרטון
    download_youtube_video(video_url, output_file)
    
    # שליחת הקובץ חזרה למשתמש כהורדה
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
