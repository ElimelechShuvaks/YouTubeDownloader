from tempfile import mktemp 
from flask import Flask, after_this_request, request, render_template, send_file
import yt_dlp

app = Flask(__name__)

def download_youtube_video(url, output_path): 
    ydl_opts = {
        'format': 'best',
        'outtmpl': output_path,
        'nocheckcertificate': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', 'video')  # שם הסרטון
        video_ext = info_dict.get('ext', '')       # סיומת הסרטון
        return f"{video_title}.{video_ext}"


def get_video_list(channel_url):
    options = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
        'extract_flat': True,
        'quiet': True,
        'skip_download': True,
        'nocheckcertificate': True
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        info = ydl.extract_info(channel_url, download=False)
    
    video_list = [
        {
            'title': video.get('title', 'Unknown title'),  # הוספת ערך ברירת מחדל
            'url': f"https://www.youtube.com/watch?v={video.get('id', '#')}",
            'upload_date': video.get('upload_date', 'Unknown date')
        }
        for video in info.get('entries', []) if video  # בדיקה ש- video אינו None
    ]
    return video_list


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['url']
    output_file = mktemp(suffix=".mp4")
    video_name = download_youtube_video(video_url, output_file)
    return send_file(output_file, as_attachment=True, download_name=video_name)

@app.route('/channel_videos', methods=['POST'])
def channel_videos():
    channel_url = request.form['channel_url']
    videos = get_video_list(channel_url)
    return render_template('video_list.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
